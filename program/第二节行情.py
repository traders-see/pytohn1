'''
火币行情
'''
import requests
import pandas as pd
pd.set_option('expand_frame_repr', False) #不换行
url1 = 'https://api.huobi.pro'
#url "https://api.huobi.pro/market/history/kline?period=1day&size=200&symbol=btcusdt"
#period=是时间 &size=返回K线数据条数 &symbol=是币种类
url2 = '/market/history/kline?period=1min&size=50&symbol=eosusdt'
url3 = url1+url2
kline = requests.get(url3)  #用requests读取数据
kline = (kline.json())   #用json显示出来数据
data = (kline['data'])   #获取data字典的key
#print(data)

#print(kline)  # 是字典类型的
df = pd.DataFrame(data)
print(df)