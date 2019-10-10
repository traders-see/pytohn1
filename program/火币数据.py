'''
获取火币的聚合行情（Ticker）
此接口获取ticker信息同时提供最近24小时的交易聚合信息。
'''

import requests
import json
import pandas as pd
pd.set_option('expand_frame_repr',False)
#  抓取数据(自己写的函数后面调用）
def get_url_content(url, maxz_try_number):
    try_num = 0
    while True:
        try:
            return requests.get(url).json()
        except Exception as http_err:
            print(url,'抓取报错',http_err)
            try_num += 1
            if try_num >= maxz_try_number:
                print('尝试失败次数过多，放弃尝试')
                return None
# huobi抓取ticker数据
def get_list_ticker_from_hobi (symbol_list1 = ['ethusdt','btcusdt']):
    for symbol1 in symbol_list1:
        print(symbol1)
        #建url
        url = 'https://api.huobi.pro/market/detail/merged?symbol=%s' % symbol1
        #抓取数据 调用上面函数
        content = get_url_content(url, 5)

        if content is None:  #当返回内容为空的时候，跳过本次循环
            continue

        #将数据转化dataframe
        df = pd.DataFrame(content)
        df = df[['tick']]
        df = df[['tick']].T
        #print(df)
        df['symbol'] = symbol1

        # 合并数据到D中
        df = df.append(df, ignore_index=True)
        #对df进行最后整理
        df = df[['symbol','amount','count','open','close','low','high','bid','ask']]
        print(df)

'''
d	integer	NA
amount	float	以基础币种计量的交易量
count	integer	交易次数
open	float	本阶段开盘价
close	float	本阶段最新价
low	float	本阶段最低价
high	float	本阶段最高价
vol	float	以报价币种计量的交易量
bid	object	当前的最高买价 [price, quote volume]
ask	object	当前的最低卖价 [price, quote volume]
'''
get_list_ticker_from_hobi()