import pandas as pd
import os
# print(os.path.dirname(__file__))
# print(os.path.dirname(os.path.dirname(__file__)))
# current_dir = os.path.dirname((os.path.dirname(__file__)))
# print(current_dir)
# file_name = '1566920340000.csv'
# path = current_dir + '' + file_name
# print(path)
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max.rows', 1000)
pd.set_option('precision', 7)
df = pd.read_csv(filepath_or_buffer='/home/taodi/文档/学习群/pycharm/pytohn1/program/1566920340000.csv',

                 )
df = df[['open_time', 'open', 'high', 'low', 'close', 'volume']]
#print(df)

# shift函数
#df['下一个close'] = df['close'].shift(-1) #　向上移动　，正数向下移动
#print(df)
#删除　del
#del df['下一个close'] # 删除一个列
#print(df)
#df.drop(['下一个close'], axis=1, inplace=True) #删除一列的另外一种方式，inplace是否带原来的df

#　　diff计算价格涨跌
#df['涨跌'] = df['close'].diff(0) #　跟自己比较
df['涨跌'] = df['close'].diff(-1) #　当前close　减去shift(-1)
#   df['涨跌'] = df['close'] - 上一个close价格
print(df)

#　涨跌幅度　
df['涨跌幅度'] = df['close'].pct_change(1)  #
print(df)

# 累计增加
df['volume_cum'] = df['volume'].cumsum()
print(df)
df['从头到位总共涨了多少'] = (df['涨跌幅度'] + 1.0).cumprod()
print(df)
#   排序
print(df.sort_values(by=['open_time'], ascending=1)) #从小到大排序，参数０从大到小
print(df.sort_values(by=['open_time', 'low'],ascending=[1, 1]))

#　合并　append
df1 = pd.read_csv('/home/taodi/文档/学习群/pycharm/pytohn1/program/1566920340000.csv')
df2 = pd.read_csv('/home/taodi/文档/学习群/pycharm/pytohn1/program/1566920400000.csv')
df3 = df1.append(df2)
print(df3)
#  去重复
df3 = df1.append(df2, ignore_index=True)  #重新定制index
df3.drop_duplicates(subset=['open_time'],
                    keep='first',
                    inplace=True)
# subset参数是　如果时间有重复的话，　keep是（first,last）first是保留第一行，last保留下行
# inplace True是时候保存保留的意思

# index 设置
df3.reset_index(inplace=True, drop=False) # 重置index　是否保留之前的index
df3.reset_index(inplace=True, drop=True)  # 重置index  是否保留事前的index
df3.reset_index('open_time', inplace=True) # 把open_time时间变成index

#替换　cloumns也就是列名字　
print(df3.rename(columns={'close':'收盘价格', 'open':'开盘价格'}))
