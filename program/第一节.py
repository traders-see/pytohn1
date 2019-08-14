'''
火币的币种有多少api
'''
import requests
import json
import pandas as pd

pd.set_option('expand_frame_repr', False)  # 当列太多的时候不换行
# 获取交易对的symbol
symbol = 'ltc_usdt'
# 构建url
url = 'https://api.huobi.pro'
url2 = '/v1/common/currencys'
url3 = url+url2
resp = requests.get(url3)
print(resp)
#print(resp.json())  # 打印出来内容
r_json = resp.json() #用一个变量接受这个字典
data = r_json['data']  #data是key 把字典的data的value打出来
#print(data)
for i in data:  #打印里面的每个币种
    pass
print(len(data))  #总共有多少币
print("eos" in data)  #判断里面有没有eos
print(data.index('eos')) # 判断EOS在第几个下标

