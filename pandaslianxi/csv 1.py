'''
read_csv 就是导入数据
'''
import pandas as pd

df = pd.read_csv('/home/taodi/文档/学习群/pycharm/51bitqunt-master/pandas_basic/binance_btc_1min.csv',
                 skiprows=0,
                 #是打印前几行
                 #nrows=20,
                 #改成日期格式
                 parse_dates=['open_time'],
                 #指定列设置为index,默认0,1,2,3,...
                 index_col=['open_time'],
                 #指定打印的列名
                 #usecols=['open_time', 'open', 'high'],
                 #当冒行数据有问题时，报错，设定为False及时报错 ，
                 #error_bad_lines=False,
                 #讲数据中的null识别为空值
                 #na_values='NULL',
                 )
#print(df)
# 看数据
#输出多少行多少列
#print(df.shape)
#顺序输出每一个列的名字
#print(df.columns)
#顺序输出每一行的名字
#print(df.index)
#输出每一列的 类型
#print(df.dtypes)
#看前3行数据 默认是5行
#print(df.head(3))
#看后3行 默认5
#print(df.tail(3))
#随机抽取，想要固定比例的话用frac参数
#print(df.sample(n=3))  #把 n 改成frac=0.5这样的
#非常方便的函数，对每一列数据有直观感受
#print(df.describe()) # count（总共这列有多少数字）mean(列的平均值）std（标准差）min,max最小和最大
# 列多的时候都显示
pd.set_option('expand_frame_repr', False)

#如何选取指定的行，列
#print(df['open']) #取一个列
# print(df)
# #取一行数据
# print(df.loc['2019-06-07 14:47:00'])
# # 取指定的那个行那个列的数字
# print(df.at['2019-06-07 14:47:00', 'open'])

# 行，列加减乘除

#统计函数
# print(df['open'].mean())  #这个一列的平均值
# print(df[['open', 'high']].mean())  # 两列的平均值
# print(df[['open', 'high']].mean(axis=1)) # 两个加起来平均值
# print(df['high'].max()) #最大值 min
# print(df['close'].std) # 标准差
# print(df['close'].count()) #非空的数据的数量 有多少空的数量
# print(df['close'].median()) # 中位数
# print(df['close'].quantile(0.25))  #25%分位数
# # shift函数 删除列的方式
# df['下周期close'] = df['close'].shift(-1)
# print(df[['close', '下周期close']]) # 下一分中的收盘价格,下周期的
# del df['下周期close']  # 删除这列
# df['涨跌'] = df['close'].diff(1) #上根K线价格和下根线的差价，1改成3就是中间三个线累计的
# print(df[['close', '涨跌']])
# df.drop(['涨跌'], axis=1,inplace=True) # 删除，axis=1是把一列都删的意思，inplace=False意思是不重新复制df的时候不替换原来数据
# df['涨跌幅'] = df['close'].pct_change(1) #若果1改3就是下上3个K线涨跌幅，
# print(df[['涨跌幅','close']])
# =====cum（cumulative)函数， 该列的累加值，用在资金流向
#df['volume_cum'] = df['volume'].cumsum()
#print(df[['colume','volume_cum']]) #本DF里没有volume所以不能打印
#资金曲线 ，涨跌幅+（1元）.cumprod()
# df['涨跌幅'] = df['close'].pct_change(1)
# print((df['涨跌幅']+1.0).cumprod()) #涨跌幅上加投资的一元看最后能转多少钱，资金曲线
#=====其他列函数
df['close_排名'] = df['close'].rank(ascending=True, pct=False)
# rank是在这列里的数字大小排名，ascending是True是从大往小排名，pct=True是变成百分比大小
print(df['close'].value_counts())  #是在这列里每个数字出现了几次
