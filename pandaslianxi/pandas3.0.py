import pandas as pd
import os
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max.rows', 1000)

# for root, dirs, files in  os.walk('/home/taodi/文档/学习群/pycharm/51bitqunt-master/binance_api'):
#     print('root:',root)
#     print('dirs:',dirs)
#     print('files:',files)
#批量读取文件名称
file_list = []
for root, dirs, files in os.walk('/home/taodi/文档/学习群/pycharm/51bitqunt-master/binance_api'):
    if files:
        for f in files:
            if f.endswith('.csv'):
                file_list.append(f)
#print(file_list)
#　　创建空的df
all_data = pd.DataFrame()
#从file_list 便利文件　用sorted排序，起名字fil
for file in sorted(file_list):
    #print(file)

    df = pd.read_csv('/home/taodi/文档/学习群/pycharm/51bitqunt-master/binance_api/' + file,
                     parse_dates=['open_time'])

    all_data = all_data.append(df,ignore_index=True)
#print(all_data)

all_data.sort_values(by=['open_time'], inplace=True)
print(all_data)

#　把all_data存到本地
all_data.to_csv('/home/taodi/文档/学习群/数据1/all_data.csv', index=False)
#  数据存入hdf
all_data.to_hdf('/home/taodi/文档/学习群/数据1/all_data.h5',
                key='all_data',
                mode='w')
# key是这个表的名字　，mode是如果之前已经存在　把原来的文件删掉

#读取　hdf
a = pd.read_hdf('/home/taodi/文档/学习群/数据1/all_data.h5',key='all_data')
print(a)