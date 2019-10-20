"""
把一个目录的所有csv文件合并成一个文件里
"""

import pandas as pd
import os
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 10000)
mu_lu = os.path.dirname(os.path.dirname(__file__))
mu_lu1 = '/home/taodi/文档/学习群/pycharm/51bitqunt-master/binance_api'
print(mu_lu1)
# for root, dirs ,files in os.walk(mu_lu1):
#     print('root:', root)
#     print('dirs:', dirs)
#     print('files:', files)
# print('-----------------')
csv_file_paths = []  # 空列表准备放所有路径文件
for root, dirs, files in os.walk(mu_lu1):
    if files:  # 如果有文件下句循环
        for f in files:
            if f.endswith(".csv"):  # 最后csv的文件都识别
                files_path = os.path.join(root, f)  #将多个路径组合后返回
                #print(files_path)
                csv_file_paths.append(files_path)  # 把所有文件都放在列表里
all_df = pd.DataFrame()  #　空的df
for file in sorted(csv_file_paths):  #sorted是排序
    #print(file)
    df = pd.read_csv(file)  #
    #print(df)
    all_df = all_df.append(df, ignore_index=True)
#print(all_df)
#删除重复数据
all_df.drop_duplicates(subset=['open_time'], inplace=True, keep='first')
#print(all_df)
all_df.sort_values(by=['open_time'], ascending=1, inplace=True)  # 从小大排序
all_df['open_time'] = pd.to_datetime(all_df['open_time'], unit='ms')
all_df['open_time'] = all_df['open_time'] + pd.Timedelta(hours=8)
all_df = all_df[['open_time','open','high','low','close','volume']]
all_df.set_index('open_time', inplace=True)
all_df.to_csv('binance_btc_imin.csv')  # 起名字保存在当下目录
print(all_df)