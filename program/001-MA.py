import pandas as pd
import numpy as np
from time import sleep
from datetime import datetime, timedelta
import json
import requests
import ccxt
from tabulate import tabulate  #是一个帮助你打印标准化表单的库
import threading  # 多线程

tabulate.PRESERVE_WHITESPACE = True
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# 参数
time_interval = '5m'

# =====symbol_para这个dict变量，记录好针对某一策略，不同品种交易对的的参数
symbol_para = {
    'btc/usd': {'para': [80, 310, 9, 13]},
    'eth/usd': {'para': [80, 120, 10, 15]},
    'ltc/usd': {'para': [80, 120, 10, 6]},
    'eos/usd': {'para': [80, 120, 10, 8]},
    'xrp/usd': {'para': [80, 110, 9, 11]},  # 注意，此处只是案例，每个币的参数是不一样的。
}
# =====account_info这个dict变量，存储各个账户信息，包括：该账户的api、secret，该账户准备交易的币种，每个币种分配的仓位等。
account_info = {
    # 第一个账号
    '账号': {
        # 该账户的api、secret'
        # bfx交易所有两个版本的api，第一代和第二代，能用2的时候尽量用2，下单操作用1
        'exchange': ccxt.bitfinex(
            {
                'apiKey': '4MHDdkaXcwZid3yr',
                'secret': 'Aj649NHnbeeDa8Wx',
            }),
        'exchange2': ccxt.bitfinex2(
            {
                'apiKey': '4MHDdkaXcwZid3yrO',
                'secret': 'Aj649NHnbeeDa8Wxa',
            }),

        'dingding_id': '',
        # 该账户交易的币种，以及每个币种分配的仓位等。
        'symbol_info': pd.DataFrame(
            {
                'btc/usd': {'分配仓位': 0.2},
                'eth/usd': {'分配仓位': 0.2},
                'ltc/usd': {'分配仓位': 0.2},
                'eos/usd': {'分配仓位': 0.2},
                'xrp/usd': {'分配仓位': 0.2}
            }
        ).T,
        '现金比率': 0.2,  # 该账户分配现金仓位的比例。分配给现金的仓位和每个币种的仓位，加起来得等于1
        # 该账号下单的杠杆数量
        '杠杆': 3,
    },
    # 第二个账号，大家如果只有一个账号，那么此处可以删除。
    # '李四的账号': {
    #     # 该账户的api、secret'
    #     # bfx交易所有两个版本的api，第一代和第二代，能用2的时候尽量用2，下单操作用1
    #     'exchange': ccxt.bitfinex(
    #         {
    #             'apiKey': '',
    #             'secret': '',
    #         }),
    #     'exchange2': ccxt.bitfinex2(
    #         {
    #             'apiKey': '',
    #             'secret': '',
    #         }),
    #
    #     'dingding_id': '',
    #     # 该账户交易的币种，以及每个币种分配的仓位等。
    #     'symbol_info': pd.DataFrame(
    #         {
    #             'btc/usd': {'分配仓位': 0.1},
    #             'eth/usd': {'分配仓位': 0.1},
    #             'ltc/usd': {'分配仓位': 0.1},
    #             'eos/usd': {'分配仓位': 0.09},
    #             'xrp/usd': {'分配仓位': 0.11}
    #         }
    #     ).T,
    #     '现金比率': 0.2,  # 该账户分配现金仓位的比例。分配给现金的仓位和每个币种的仓位，加起来得等于1
    #     # 该账号下单的杠杆数量
    #     '杠杆': 3,
    # },
    # # 大家如果还有账号，顺序添加即可。

}

# =====均线收缩策略


# =====通过ccxt获取margin的usd余额
def ccxt_fetch_margin_usd_amount(bitfinex2):
    # =====获取当前资金数量
    while True:
        try:
            margin_info = bitfinex2.private_post_auth_r_wallets()
            break
        except Exception as e:
            print(e)
    account = pd.DataFrame(margin_info, columns=['交易账户', '币种', '数量', 'unknow', 'unknow2'])  # 将数据转化为df格式
    condition1 = account['交易账户'] == 'margin'
    condition2 = account['币种'] == 'USD'
    usd_amount = float(account.loc[condition1 & condition2, '数量'])
    return usd_amount


# =====通过ccxt获取margin的仓位
def ccxt_fetch_margin_position(bitfinex2):
    # 获取账户的margin持仓信息
    while True:
        try:
            position_info = bitfinex2.private_post_auth_r_positions()  # 从bfx交易所获取账户的持仓信息
            break
        except Exception as e:
            send_dingding_msg('获取持仓信息失败')
            print(e)
            continue
    position_info = pd.DataFrame(position_info, columns=['交易对', '状态', '持仓量', '成本价格', '借币利息',
                                                         'unknow1', '损益', 'unknow2', '爆仓价格',
                                                         'unknow3'])  # 将数据转化为df格式
    position_info.drop(['状态', 'unknow1', 'unknow2', 'unknow3'], axis=1, inplace=True)  # 去除不必要的列
    return position_info


# =====更新所有交易对的信息
def update_symbol_info(bitfinex, bitfinex2, symbol_info, act_name, if_print=True):
    """
        :param bitfinex2 通过bitfinex2的ccxt接口获取账户信息
        :param symbol_info为Dataframe，更新在account_info.symbol_info当中的币种信息
        :param act_name 账户名称
        :param if_print在调试时使用 等于True会输出调试信息
        :return:
        """
    # ====获取当前账户美元
    usd_amount = ccxt_fetch_margin_usd_amount(bitfinex2)  # usd_amount是margin账户中美元的数量

    # =====获取监测品种的相关信息
    # 从服务器获取当前持仓信息
    server_margin_position = ccxt_fetch_margin_position(bitfinex2)
    position_info = bitfinex.private_post_positions()
    position_info = pd.DataFrame(position_info)
    # 更新本地symbol_info中的数据
    for symbol in symbol_info.index:
        # 什么仓位都没有的情况
        if server_margin_position.empty:
            _temp = pd.DataFrame()
        else:
            _temp = server_margin_position[
                server_margin_position['交易对'] == 't' + str((symbol.split('/')[0] + symbol.split('/')[1]).upper())]
        # 如果position里面没有该交易对的持仓，就把前面的交易信息都进行初始化
        if _temp.empty:
            symbol_info.at[symbol, '当前持仓'] = 0
            symbol_info.at[symbol, '当前持仓量'] = None
            symbol_info.at[symbol, '成本价格'] = None
            symbol_info.at[symbol, '止损价'] = None
            symbol_info.at[symbol, '损益'] = None
            symbol_info.at[symbol, '保证金'] = None
            # symbol_info.at[symbol, '信号时间'] = None
        else:
            condition1 = position_info['symbol'] == str(symbol.split('/')[0] + symbol.split('/')[1])
            symbol_info.at[symbol, 'position_id'] = int(position_info.loc[condition1, 'id'])
            symbol_info.at[symbol, '当前持仓量'] = float(_temp.iloc[0]['持仓量'])  # 持仓数量
            symbol_info.at[symbol, '当前持仓'] = 1 if symbol_info.at[symbol, '当前持仓量'] > 0 else -1
            symbol_info.at[symbol, '成本价格'] = float(_temp.iloc[0]['成本价格'])  # 成本价格
            symbol_info.at[symbol, '止损价'] = symbol_info.at[symbol, '成本价格'] * (
                    1 - symbol_para[symbol]['para'][-1] / 100 * symbol_info.at[symbol, '当前持仓'])  # 根据当前持仓的正负，确定止损价
            symbol_info.at[symbol, '损益'] = float(_temp.iloc[0]['损益'])  # 这个交易对的盈利与亏损
            symbol_info.at[symbol, '保证金'] = symbol_info.at[symbol, '成本价格'] * abs(symbol_info.at[symbol, '当前持仓量']) * 0.3

    # =====计算空仓的品种需要投入的资金
    # 理论资金
    net_value = usd_amount + symbol_info['损益'].sum()  # 账户净值，即初始投入资金+所有仓位的收益
    symbol_info['理论分配资金'] = symbol_info['分配仓位'] / (symbol_info['分配仓位'].sum() + account_info[act_name]['现金比率']) * (
        usd_amount)
    symbol_info['备用保证金'] = symbol_info['理论分配资金'] - symbol_info['保证金']  # 此处可能出现负数。当实际买入之后，调整了杠杆或者比例。
    symbol_info.loc[symbol_info['备用保证金'] < 0, '备用保证金'] = 0  # 将备用保证金为负数的改成0

    # 计算已经使用的资金，以及可以使用的资金
    if len(symbol_info[symbol_info['当前持仓'] != 0]) > 0:
        used_money = symbol_info['保证金'].sum() + symbol_info['备用保证金'].sum()
        can_use_money = usd_amount - used_money
    else:
        used_money = 0
        can_use_money = net_value
    if if_print:
        print('初始资金', usd_amount, '已用资金', used_money, '可用资金', can_use_money)

    # 计算用于为开仓品种的资金
    _index = symbol_info[symbol_info['当前持仓'] == 0].index
    symbol_info.loc[_index, '买入资金'] = symbol_info['分配仓位'] / (
            symbol_info.loc[_index, '分配仓位'].sum() + account_info[act_name]['现金比率']) * (can_use_money)
    if if_print:
        print(tabulate(symbol_info, headers='keys', tablefmt='presto'))

    return symbol_info, net_value


# =====下次运行时间，和课程里面讲的函数是一样的
def next_run_time(time_interval, ahead_time=1):
    """
        :param time_interval 运行周期时间 建议不要小于5min
        :param ahead_time 当小于1s时 自动进入下个周期
        :return:
        """
    if time_interval.endswith('m'):
        now_time = datetime.now()
        time_interval = int(time_interval.strip('m'))

        target_min = (int(now_time.minute / time_interval) + 1) * time_interval
        if target_min < 60:
            target_time = now_time.replace(minute=target_min, second=0, microsecond=0)
        else:
            if now_time.hour == 23:
                target_time = now_time.replace(hour=0, minute=0, second=0, microsecond=0)
                target_time += timedelta(days=1)
            else:
                target_time = now_time.replace(hour=now_time.hour + 1, minute=0, second=0, microsecond=0)

        # sleep直到靠近目标时间之前
        if (target_time - datetime.now()).seconds < ahead_time + 1:
            print('距离target_time不足', ahead_time, '秒，下下个周期再运行')
            target_time += timedelta(minutes=time_interval)
        print('下次运行时间', target_time)
        return target_time
    else:
        exit('time_interval doesn\'t end with m')


# =====获取bitfinex交易所k线
def get_bitfinex_candle_data(exchange, symbol, time_interval, limit):
    while True:

        try:
            content = exchange.fetch_ohlcv(symbol=symbol, timeframe=time_interval, limit=limit)
            break
        except Exception as e:
            send_dingding_msg(content='抓不到k线，稍等重试')
            print(e)
            sleep(5 * 1)

    df = pd.DataFrame(content, dtype=float)
    df.rename(columns={0: 'MTS', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace=True)
    df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms')
    df['candle_begin_time_GMT8'] = df['candle_begin_time'] + timedelta(hours=8)
    df = df[['candle_begin_time_GMT8', 'open', 'high', 'low', 'close', 'volume']]
    # 在这里使用的是中国本地时间 所以需要GMT8 如果在服务器上跑直接使用candle_begin_time这一列就可以了
    # df = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]

    return df


# =====发送钉钉消息，id填上使用的机器人的id
def send_dingding_msg(content, robot_id=''):
    try:
        msg = {
            "msgtype": "text",
            "text": {"content": content + '\n' + datetime.now().strftime("%m-%d %H:%M:%S")}}
        headers = {"Content-Type": "application/json;charset=utf-8"}
        url = 'https://oapi.dingtalk.com/robot/send?access_token=' + robot_id
        body = json.dumps(msg)
        requests.post(url, data=body, headers=headers)
        print('成功发送钉钉')
    except Exception as e:
        print("发送钉钉失败:", e)


# =====下单操作
def place_order(exchange, order_type, buy_or_sell, symbol, price, amount, symbol_info):
    """
    下单
    :param exchange: 交易所
    :param order_type: limit, market
    :param buy_or_sell: buy, sell
    :param symbol: 买卖品种
    :param price: 当market订单的时候，price无效
    :param amount: 买卖量
    :return:
    """
    for i in range(5):
        try:
            # 限价单
            if order_type == 'limit':
                # 买
                if buy_or_sell == 'buy':
                    order_info = exchange.create_limit_buy_order(symbol, amount, price, {'type': 'limit'})  # 买单
                # 卖
                elif buy_or_sell == 'sell':
                    order_info = exchange.create_limit_sell_order(symbol, amount, price, {'type': 'limit'})  # 卖单
            # 市价单
            elif order_type == 'market':
                # 买
                if buy_or_sell == 'buy':
                    order_info = exchange.create_market_buy_order(symbol, amount, {'type': 'market'})  # 买单
                # 卖
                elif buy_or_sell == 'sell':
                    order_info = exchange.create_market_sell_order(symbol, amount, {'type': 'market'})  # 卖单
            else:
                pass

            print('下单成功：', order_type, buy_or_sell, symbol, price, amount)
            print('下单信息：', order_info, '\n')
            # 执行时间、价格
            symbol_info.at[symbol.lower(), '当前持仓量'] = amount
            symbol_info.at[symbol.lower(), '执行时间'] = datetime.now().strftime('%H:%M:%S')

            return order_info

        except Exception as e:
            print('下单报错，3s后重试', e)
            sleep(3)

    print('下单报错次数过多，下单线程终止')
    exit()


# =====多线程框架
def multi_threading_frame(exchange, order_info, symbol_info):
    threads = []  # 全部线程

    for order in order_info:
        # 将每个订单加入子线程
        t = threading.Thread(target=place_order, args=(exchange,
                                                       order['order_type'],
                                                       order['buy_or_sell'],
                                                       order['symbol'],
                                                       order['price'],
                                                       order['amount'],
                                                       symbol_info))
        threads.append(t)

    # 开始线程
    for i in range(len(threads)):
        threads[i].start()

    # 等待所有子线程结束后才继续执行主线程
    for i in range(len(threads)):
        threads[i].join()


# =====主函数
def main():
    # ===将变量初始化、从服务器更新各个账户的信息
    for act_name in account_info.keys():
        print('=' * 5, '运行账户：', act_name)
        # 将一些变量初始化
        account_info[act_name]['msg_content'] = str(act_name) + '_margin策略:\n'
        account_info[act_name]['不交易的品种'] = []
        account_info[act_name]['平仓的品种'] = []
        account_info[act_name]['开仓的品种'] = []
        # 更新账户信息
        account_info[act_name]['exchange2'].load_markets()
        update_symbol_info(account_info[act_name]['exchange'], account_info[act_name]['exchange2'],
                           account_info[act_name]['symbol_info'], act_name)

    # =====sleep到下个运行周期
    run_time = next_run_time(time_interval)
    sleep(max(0, (run_time - datetime.now()).seconds))
    while True:  # 在靠近目标时间时
        if datetime.now() < run_time:
            continue
        else:
            break

    # =====遍历获取交易品种的数据、遍历各个账信号，产生每个账号下面每个交易对的目标信号。（所有账户数据只获取一次数据）
    for symbol in symbol_para.keys():
        print('=' * 3, '计算信号', symbol, '参数', symbol_para[symbol]['para'])
        max_try_amount = 5
        # 获取数据
        for i in range(max_try_amount):
            # 获取symbol该品种最新的K线数据
            df = get_bitfinex_candle_data(account_info[act_name]['exchange2'], str(symbol.upper()), time_interval,
                                          limit=(max(symbol_para[symbol]['para']) + 5))
            # 判断是否包含最新的数据
            _temp = df[df['candle_begin_time_GMT8'] == (run_time - timedelta(minutes=int(time_interval.strip('m'))))]
            if _temp.empty:
                print('获取数据不包含最新的数据，重新获取')
                send_dingding_msg('获取不到最新数据，重新获取')
                sleep(3 * 1)
                if i == (max_try_amount - 1):
                    df = pd.DataFrame()
                    send_dingding_msg('没有获取到' + str(symbol) + '的数据，该货币跳过本周期')
            else:
                current_price = df.iloc[-1]['close']  # 记录symbol该品种的最新价格
                df = df[df['candle_begin_time_GMT8'] < pd.to_datetime(run_time)]  # 去除target_time周期的数据
                break

        # 遍历交易账户，计算每个账户、每个symbol的目标仓位
        for account in account_info.keys():
            symbol_info = account_info[account]['symbol_info']  # 获取该账户下面的symbol_info变量
            # 计算目标仓位，并记录下产生目标仓位的时间
            if df.empty:
                symbol_info.at[symbol, '目标仓位'] = None
            else:
                symbol_info.at[symbol, '目标仓位'] = signal_ma_converge_with_stop_lose(
                    df, symbol_info.at[symbol, '当前持仓'],
                    symbol_info.at[symbol, '止损价'],
                    symbol_para[symbol][
                        'para'])  # 根据策略计算出目标交易信号。
                symbol_info.at[symbol, '信号时间'] = run_time
                symbol_info.at[symbol, '现价'] = current_price
                print(account, '当前持仓', symbol_info.at[symbol, '当前持仓'], '目标仓位', symbol_info.at[symbol, '目标仓位'])

    # =====判断是否交易 遍历账户，判断是否要进行买卖
    for act_name in account_info.keys():
        symbol_info = account_info[act_name]['symbol_info']
        # 遍历该账户的交易对
        for symbol in symbol_info.index:
            # 读取当前仓位和目标仓位
            now_pos = symbol_info.at[symbol, '当前持仓']
            target_pos = symbol_info.at[symbol, '目标仓位']
            # 判断是否操作
            if now_pos == target_pos or (target_pos != target_pos):  # 后面这个是判断是否为nan值
                account_info[act_name]['不交易的品种'].append(symbol)
            # 把需要平仓跟开仓的品种加入['平仓的品种']和['开仓的品种']这两个list
            else:
                if now_pos == 1 and target_pos == 0:  # 平多
                    account_info[act_name]['平仓的品种'].append(symbol)
                elif now_pos == -1 and target_pos == 0:  # 平空
                    account_info[act_name]['平仓的品种'].append(symbol)
                elif now_pos == 0 and target_pos == 1:  # 开多
                    account_info[act_name]['开仓的品种'].append(symbol)
                elif now_pos == 0 and target_pos == -1:  # 开空
                    account_info[act_name]['开仓的品种'].append(symbol)
                elif now_pos == 1 and target_pos == -1:  # 平多，开空
                    account_info[act_name]['平仓的品种'].append(symbol)
                    account_info[act_name]['开仓的品种'].append(symbol)
                elif now_pos == -1 and target_pos == 1:  # 平空，开多
                    account_info[act_name]['平仓的品种'].append(symbol)
                    account_info[act_name]['开仓的品种'].append(symbol)

        # 输出
        account_info[act_name]['msg_content'] += '无交易symbol：' + str(account_info[act_name]['不交易的品种']) + '\n'
        account_info[act_name]['msg_content'] += '平仓symbol：' + str(account_info[act_name]['平仓的品种']) + '\n'
        account_info[act_name]['msg_content'] += '开仓symbol：' + str(account_info[act_name]['开仓的品种']) + '\n'
        print(account_info[act_name]['msg_content'])

    # =====交易平仓的品种
    for act_name in sorted(account_info.keys()):
        # 获取本地信息
        close_pos_symbol = account_info[act_name]['平仓的品种']
        symbol_info = account_info[act_name]['symbol_info']
        # 有需要平仓的品种
        if close_pos_symbol:
            print('=====平仓相关品种')
            # 批量买入
            for symbol in close_pos_symbol:
                # 执行平仓
                account_info[act_name]['exchange'].private_post_position_close(
                    params={'position_id': int(symbol_info.at[symbol, 'position_id'])})
                # 执行时间、价格
                symbol_info.at[symbol, '执行时间'] = datetime.now().strftime('%H:%M:%S')  # 记录下执行该仓位的时间
                # 邮件内容
                account_info[act_name]['msg_content'] += '_' + symbol + '平仓'
            # 邮件内容
            account_info[act_name]['msg_content'] += '平仓信息：\n'
            account_info[act_name]['msg_content'] += str(symbol_info[['分配仓位', '现价', '信号时间', '执行时间']].T[
                                                             close_pos_symbol]) + '\n'
    print('=============平仓完成=============')
    # =====交易建仓的品种
    for act_name in sorted(account_info.keys()):
        # 获取本地信息
        open_pos_symbol = account_info[act_name]['开仓的品种']

        # 有需要开仓的交易
        if open_pos_symbol:
            print('=====建仓相关品种')
            # 更新账户信息：此时如果之前发生平仓，从服务器获取到的账户信息不一定是最新的。
            # 比如会出现之前已经平仓的品种仍然在balalce中。导致下方的buy_money = symbol_info.at[symbol, '买入资金']为None。所以需要判断一下。
            while True:
                symbol_info, net_value = update_symbol_info(account_info[act_name]['exchange'],
                                                            account_info[act_name]['exchange2'],
                                                            account_info[act_name]['symbol_info'], act_name)
                all_true = True
                for symbol in open_pos_symbol:
                    all_true = all_true & pd.notnull(symbol_info.at[symbol, '买入资金'])
                if all_true:  # 全都不为空
                    break
                else:  # 有品种买入资金为空
                    print('\n有品种的买入资金为空，说明balance信息不是最新的，重新更新')
                    sleep(1)
            # 批量买入
            order_info = []
            for symbol in open_pos_symbol:
                # 加载数据
                target_pos = symbol_info.at[symbol, '目标仓位']
                buy_money = symbol_info.at[symbol, '买入资金']
                trade_value = buy_money * account_info[act_name]['杠杆']
                current_price = float(symbol_info.at[symbol, '现价'])
                # 计算买卖方向
                buy_or_sell = 'buy' if target_pos > 0 else 'sell'
                trade_amount = abs(float(str(trade_value / current_price)))
                print('买入资金', buy_money, 'trade_value', trade_value, 'trade_amount', trade_amount, 'current_price',
                      current_price)
                # 构造下单信息
                order_info.append({'order_type': 'limit',
                                   'buy_or_sell': buy_or_sell,
                                   'symbol': symbol.upper(),
                                   'price': symbol_info.at[symbol, '现价'] * (1 + 0.02 * target_pos),
                                   'amount': trade_amount})

                # 邮件内容
                account_info[act_name]['msg_content'] += '_' + symbol + '开仓'

            # 执行多线程下单
            multi_threading_frame(account_info[act_name]['exchange'], order_info, symbol_info)
            # 邮件内容
            account_info[act_name]['msg_content'] += '建仓信息：\n'
            account_info[act_name]['msg_content'] += str(symbol_info[['当前持仓量', '现价', '信号时间', '执行时间']].T[
                                                             open_pos_symbol]) + '\n'
    print('=============建仓完成=============')
    sleep(5)
    # =====遍历账户发送钉钉
    for act_name in account_info.keys():
        symbol_info, net_value = update_symbol_info(account_info[act_name]['exchange'],
                                                    account_info[act_name]['exchange2'],
                                                    account_info[act_name]['symbol_info'], act_name)
        account_info[act_name]['msg_content'] += '账户总资产：' + str(net_value) + '$\n'
        for symbol in symbol_para.keys():
            account_info[act_name]['msg_content'] += str(symbol) + ':\n' + '开仓数量:' + str(
                symbol_info.at[symbol, '当前持仓量']) + '\n'
            account_info[act_name]['msg_content'] += '成本价格:' + str(symbol_info.at[symbol, '成本价格']) + '\n'
            account_info[act_name]['msg_content'] += '当前盈亏:' + str(symbol_info.at[symbol, '损益']) + '\n'
        while True:
            try:
                send_dingding_msg(account_info[act_name]['msg_content'], robot_id=account_info[act_name]['dingding_id'])
                break
            except Exception as e:
                print(e)
                sleep(5)
                continue


# =====运行主体
while True:
    try:
        main()
        sleep(10)
    except Exception as e:
        send_dingding_msg('系统出错，10s之后重新运行')
        print(e)
        sleep(10)
