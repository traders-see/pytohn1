import requests
import pandas as pd
import json
pd.set_option('expand_frame_repr',False)
pd.set_option('display.max_rows',1000)
#抓数据函数
def get_url(url,max_try_number):
    try_num = 0
    while True:
        try:
            return requests.get(url).json()
        except Exception as http_err:
            print(url,'抓取有错误',http_err)
            try_num += 1
            if try_num >= max_try_number:
                print('次数太多放弃请查询网络')
                return None
#  ===============================================
# https://api.huobi.pro/market/history/kline?period=1day&size=200&symbol=btcusdt
def candle_hobi(period='1day',size='200',symbol='btcusdt'):
    url = 'https://api.huobi.pro/market/history/kline?period=%s&size=%s&symbol=%s' % (period, size, symbol)
    #print(url)
    content = get_url(url, 5)
    #print(content)
    data = content['data'] #　把数据里面的字典data：里面数据单独读出来，顺便起名data
    #print(data)
    print(type(data))
    df = pd.DataFrame(data)
    #  秒时间改一下
    df['id'] = pd.to_datetime(df['id'], unit='ms')
    # 改列名字　
    #df1 = df.rename(columns={'open':'开盘价', 'close':'收盘价','low':'最低价',
    #                   'high':'最高价','amount':'交易量'})
    print(df)

"""
symbol	string	true	NA	交易对	btcusdt, ethbtc...
period	string	true	NA	返回数据时间粒度，也就是每根蜡烛的时间区间	1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
size	integer	false	150	返回 K 线数据条数	[1, 2000]
id	integer	调整为北京时间的时间戳，单位秒，并以此作为此K线柱的id
amount	float	以基础币种计量的交易量
count	integer	交易次数
open	float	本阶段开盘价
close	float	本阶段收盘价
low	float	本阶段最低价
high	float	本阶段最高价
vol	float	以报价币种计量的交易量
"""

candle_hobi(period='15min', size='100',symbol='btcusdt')