import pandas as pd
import time
import requests
pd.set_option('expand_frame_repr', False)
BASE_URL = 'https://api.binance.com'
kline = '/api/v1/klines'
#kline_url = BASE_URL + kline + '?' + 'symbol=BTCUSDT&interval=1h&limit=1000'
limit = 1000
end_time = int(time.time() // 60 * 60 * 1000)
start_time = int(end_time -limit*60*1000)
while True:
    url = BASE_URL + kline + '?symbol=BTCUSDT&interval=1m&limit=' + str(limit) +'&startTime=' + str(start_time) + '&endTime=' +str(end_time)
    resp = requests.get(url)
    data = resp.json()
    df = pd.DataFrame(data, columns={'open_time': 0, 'open': 1, 'high': 2, 'low': 3,
                                     'close': 4, 'volume': 5, 'close_time': 6,
                                     'quote_volume': 7, 'trades': 8, 'taker_base_volue': 9,
                                     'taker_quote_volume': 10, 'ignore': 11})
    # columns函数来给DF文件第一行的列表名字改

    df.set_index('open_time', inplace=True) #inplace是前面原来的0,1,2,index内容替换了
    #df.to_csv('/home/taodi/文档/学习群/数据/' + str(end_time) + '.csv')
    if len(df) < 1000:
        print(df)
        break
    end_time = start_time
    start_time = int(end_time - limit * 60 *1000)