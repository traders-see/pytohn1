import pandas as pd
import os

print(pd.__version__)
pd.set_option('expand_frame_repr' ,False) #当列太多时候显示
pd.set_option('display.max_rows', 1000) #  最多显示行
pd.set_option('precision', 6)   #浮点数



print(os.path.dirname(__file__))
print(os.path.dirname(os.path.dirname(__file__)))

df = pd.read_csv(filepath_or_buffer='/home/taodi/文档/学习群/pycharm/pytohn1/program/1566920340000.csv',
                 skiprows=0,
                 usecols=['open_time', 'open', 'high', 'low', 'close', 'volume'],
                 nrows=10)
print(df)
a = df.dtypes  #输出每一列变量类型
print(a)
print(df.columns)  # 输出列名字
for col in df.columns:
    print(col)
print(df.head(7)) # 默认５行　
print(df.tail())    # 看最后行　默认５
print(df.sample(n=3))  #随机抽出３行
print(df.sample(frac=0.2)) #百分比例输出
print(df.describe())  # 对每一列数据直观感受

# 对数据的访问和操作
print(df['open'])  #　列名取，读取数据是Series类型
print(df[['open', 'open_time']])

df['mark'] = '北京时间' #mark是列名字，北京时间是列数据
print(df)
df['开盘价_+收盘价'] = (df['open'] + df['high'])
df['rmb_price'] = df['close'] * 7.1
print(df)
df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
df['open_time'] = df['open_time'] + pd.Timedelta(hours=8)
print(df)
# iloc 操作：通过　position来读取数据　loc
print(df.iloc[0])  #以index读取一行，读取数据是Series类型
print(df.iloc[1]['open'])  #index 1行的open 数据
print(df.iloc[1:4])
print(df.iloc[:, :]) #读取所有行，所有列
print(df.iloc[-1])   #获取最后一行数据

# 统计函数　
print(df['close'].mean())  # 求一整类的均值，返回一个数，会自动排除空值
print(df[['close', 'volume']].mean()) # 求两列的均值，返回两个数
df['close_v'] = df[['close', 'volume']].mean(axis=1)
# axis=1 ,axis=0  代表对整几列进行操作，或者代表对几行进行操作
print(df)

print(df['high'].max())
print(df['low'].min())
print(df['close'].std()) #标准差　
print(df['close'].count()) # 非空的数据的数量
print(df['close'].median()) # 中位数
print(df['close'].quantile(0.25))  #25%分为数