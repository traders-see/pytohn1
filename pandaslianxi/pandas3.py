import pandas as pd
import os
pd.set_option('expand_frame_repr', False)

# df = pd.read_csv('/home/taodi/文档/学习群/pycharm/51bitqunt-master/binance_api/1560038820000.csv',
#                  skiprows=0,
#                  parse_dates=['open_time'])
# print(df)
#批量导入数据，上面是导入一个文件 如果一下导入很多文件 os.walk
# for root, dirs, files, in os.walk('/home/taodi/文档/学习群/pycharm/51bitqunt-master/binance_api'):
#     print('root:', root)
#     print('dirs:', dirs)
#     print('files:', files)
#     print()
file_list = []
for root, dirs, files in os.walk('/home/taodi/文档/学习群/pycharm/51bitqunt-master/binance_api'):
    if files: # 如果files下空的时候执行下面
        for f in files:
            if f.endswith('.csv'):
                file_list.append(f)
print(file_list)
data = pd.DataFrame()
for i in sorted(file_list): # sorted是对list排序用的
    print(i)
    df = pd.read_csv('/home/taodi/文档/学习群/pycharm/51bitqunt-master/binance_api/' + i,
                     parse_dates=['open_time'])
    #print(df) # 一个一个打印出来
    #合并数据
    data = data.append(df, ignore_index=True)

#对数据排序
data.sort_values(by=['open_time'], inplace=True)
print(data)

# 然后存到本地 hdf文件
#data.to_hdf('/home/taodi/文档/学习群/pycharm/' + 'hdf.h5',)
# data.to_csv('/home/taodi/文档/学习群/pycharm/' + 'hdf.csv',
#             index=False,
#             mode='w')
#data.to_csv('data1.csv',index=False)