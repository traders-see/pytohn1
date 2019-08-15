import ccxt
import pandas as pd
pd.set_option('expand_frame_repr', False)
print(ccxt.exchanges)  # 支持的交易所的ID
huobipro= ccxt.huobipro()
huobipro.apiKey = '3bb14748-9fea2f0b-dqnh6tvdf3-8868c'
huobipro.secret = 'a3a15718-227ec617-38b6cf4c-c22a7'

balance = huobipro.fetch_balance()
#print(balance['info'])
#print(balance)
#print(balance['free'])  # 每个币的资产
#print(balance['EOS'])
# print(balance['USDT'])
# print(balance['total'])

#========下单
#下单参数
symbol = 'EOS/USDT'  #这是制定交易哪个币
pirce = 3.10       #交易价格
amount = 1     #交易数量
# 限价单
#order_info = huobipro.create_limit_buy_order(symbol, amount , pirce ) #买单
#order_info = huobipro.create_limit_sell_order(symbol, amount, pirce)  #卖单
#print(order_info['id'])  #这比交易的ID
#print(order_info['info']) # 交易信息

# 市价单 市价格不需要填写价格
#买单 order_info = huobipro.create_market_buy_order(symbol=symbol, amount=amount)
#卖单order_info = huobipro.create_market_sell_order(symbol=symbol, amount=amount)
# 查询订单
# order_info = huobipro.fetch_order(id='44546648652',symbol='EOS/USDT')
# print(order_info)
# #https://github.com/ccxt/ccxt/wiki/Manua|#order-structure 看很多信息
# print(order_info['status']) #这个订单活跃还是
# print(order_info['remaining']) # 这笔订单买币数量


#获取全部订单
order_info = huobipro.fetch_orders(symbol='EOS/USDT', limit=10)#limit是查询最近几笔交易
for i in order_info:  # 给order_info复制的所有订单变成list复制给他 所以我们循环全部打印出来
    print(i['datetime'], i['status'])
#返回未成交的订单
order_info = huobipro.fetch_open_orders(symbol='EOS/USDT', limit=10)
for i in order_info:
    print(i['datetime'], i['status'])
# 撤单
# order_info = huobipro.cancel_order(id='这里输入ID',symbol='EOS/USDT')
# print(order_info['status']) # status=canceled就是撤单了 canceled是已经撤单的意思