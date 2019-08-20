# 缺失值的处理
import pandas as pd
pd.set_option('expand_frame_repr', False)
df = pd.read_csv('/home/taodi/文档/学习群/pycharm/51bitqunt-master/binance_api/cvs/1559978820000.csv',
                 )
#print(df)
# index = df[df['open_time'].isin(['1559918880000','1559919060000'])]
# print(index)
# index = df[df['open_time'].isin(['1559918880000','1559919060000'])].index
# print(index)
#删除缺失空值
#df.dropna(how='any') # 删除空值，how=any是只有这行里有一个空值就删除这行，
#df.dropna(subset=['close'],how=any) 在close里有一个空就删掉，其他列不管，、
#补全缺值
#print(df.fillna(value=0)) # 把空值替换生固定值值0 当然其他的可以 value=替换的值

#排序函数


#df.sort_values(by=['volume'], ascending=1)#如果ancending 1从到小 0就从大到小
#print(df.sort_values(by=['volume'], ascending=1))
#多列排
#print(df.sort_values(by=['volume', 'close '], ascending=[1, 1]))
df1 = df.iloc[0:3]  # iloc前三行
#print(df1)
df2 = df.iloc[11:16]
#print(df2)
df3 = df1.append(df2)
#print(df3)
df4 = df1.append(df2, ignore_index=True)  # 是不保留原来的index，重新定义，
print(df4)
#=====对数据进行去重

#=====其他常用重要函数
# df.reset_index(inplace=True) # 重置index
# print(df)
#==== 给列名字修改
#print(df.rename(columns={'close': '收盘价格', 'open': '开盘价格'}))
#print(df.empty) # 判断是不是空的还是有数据的

#====字符串处理
#print(df['symbol'].str[:3])
#print(df['symbol'].str.upper()) #都改成大写

#====时间处理

# print(type(df.at[0,'open_time']))
# #如果是字符串就用to_datetime转变成日期格式
# df['open_time'] = pd.to_datetime(df['open_time'])
#
# #===== rolling, expanding操作
# print(df['close'].mean()) #这是一列数字的均值
# #如何得到每一天的最近3天close的均值呢？ 如何计算常用的移动平均线 rolling是滚动计算
# df['收盘价格3天均值'] = df['close'].rolling(3).mean()
# print(df[['close', '收盘价格3天均值']])
# expanding===== 第一天开始到现在所有行的移动计算
#df['收盘价_到至今均值'] = df['close'].expanding().mean #最后一行是前面所有行的均值



# =====导出本地文件 csv  to_csv
#df.to_csv('name.csv', index=False)  # index=False是重新建立index