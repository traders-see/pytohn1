from urllib.request import urlopen
import json
import pandas as pd
pd.set_option('expand_frame_repr',False)
#  抓取数据(自己写的函数后面调用）
def get_url_content(url, maxz_try_number):
    try_num = 0
    while True:
        try:
            return urlopen(url,timeout=15).read().strip()
        except Exception as http_err:
            print(url,'抓取报错',http_err)
            try_num += 1
            if try_num >= maxz_try_number:
                print('尝试失败次数过多，放弃尝试')
                return None
# huobi抓取ticker数据
def get_list_ticker_from_hobi(symbol_list=['btcusdt', 'ethusdt']):
    #创建一个空的ＤＦ
    df = pd.DataFrame()
    #遍历每个symbol
    for symbol in symbol_list:
        #建url
        url = 'https://api.huobi.pro/market/detail/merged?symbol=%s' % symbol
        #抓取数据 调用上面函数
        content = get_url_content(url, 5)
        print(content)
        exit()
        if content is None:  #当返回内容为空的时候，跳过本次循环
            continue

        #将数据转化dataframe
        json_data = json.loads(content.decode('utf-8')) #获取的数据转换成字符串（str)
        _df = pd.DataFrame(json_data, dtype='float')  #把字符串转换成字典　
        _df = _df[['ticker']].T
        _df['symbol'] = symbol

        # 合并数据到D中
        df = df.append(_df, ignore_index=True)
        #对df进行最后整理
        df = df[['symbol','last','buy','sell','high','low','vol']]
        print(df)
        return df
get_list_ticker_from_hobi(symbol_list=['btcusdt', 'ethusdt'])

'''
这些是基础代码原理
symbol = 'btcusdt'
url = 'https://api.huobi.pro/market/detail/merged?symbol=%s' % symbol


#  抓取数据      # urllib 这个python自带的库，是用来网上抓取数据的
content = urlopen(url, timeout=15).read()
#timeout是联网时间消耗，链接请求中最多等待１５秒，如果15没有链接就报错，read是抓取数据
print(content)
#转换为dataframe
json_data = json.loads(content.decode('utf-8'))
df = pd.DataFrame(json_data, dtype='float')
df = df[['ticker']].T
print(df)

'''