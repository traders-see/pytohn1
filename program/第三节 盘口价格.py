'''
火币 盘口价格
'''
import requests
import pandas as pd
import time
pd.set_option('expand_frame_repr', False)
while True:
    symbol = 'symbol=eosusdt'
    url1 = 'https://api.huobi.pro/market/detail/merged?' + symbol
    url2 = requests.get(url1)
    print(url2) #打印200就是正常
    Handicap = (url2.json())
    #print(Handicap)
    tick = (Handicap['tick']) #这个数据在tick里面 所有先获取
    #print(tick)
    df = pd.DataFrame(tick)
    print(df)
    mai_mai = (df[['ask','bid']])
    print(mai_mai)
    print('卖价:',mai_mai['ask'][0])
    print('买价:',mai_mai['bid'][0])
    time.sleep(5)