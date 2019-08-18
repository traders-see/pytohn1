# #list
# list_var = []
# print(list_var, type(list_var))
# list_var1 = [1, '2', 3, 5.0, 'seven', [8]]
# print(list_var1)
# print(len(list_var1))
# #print(max(list_var1)) #会报错 因为里面不是同一个类
# del (list_var1[4])
# print(list_var1)
# print(list_var1.index(5.0))
# # append和extend区别
# list_var1.append([1,2,3,4,5,'sq'])
# print(list_var1)
# list_var1.extend([1,2,3,4,5,'sq'])     #不分开直接加进来
# print(list_var1)
# list_var1.reverse()
# print(list_var1)
# #list_var1.sort()  # 从小排到大 必须同类才可以
# list_var_2 = [6,4,3,7,8,5,]
# list_var_2.sort()
# print(list_var_2)
# list_var_2.sort(reverse=True)
# print(list_var_2)
# list_var_2[1] = 50  #修改
# print(list_var_2)

# # dict 字典 1（没有顺序）2（key,value)key不能重复，value可以重复
# dict_var = {'btc': '比特币',
#             'eth': '以太坊',
#             'XRP': '瑞波币'}
# print(dict_var)
# a = dict_var['btc'] #取 btc key的value
# print(a)
# # 增加 一对 key value
# dict_var['bch'] = '比特币现金'
# print(dict_var)
# # 更改 value
# dict_var['bch'] = 'btc现金'
# print(dict_var)
# # 判断一个key 在这个dict里面
# print('bch' in dict_var)
# #输入所有的key 和 value
# b = dict_var.keys()
# print(b)
# c = dict_var.values()
# print(c)

# 字符串转移  \   ,  \t ,  r
# startswinth endswith startswinth是否用什么什么开头的 endswith是否用什么结尾的
# symbol = 'btcusdt'
# print(symbol.startswith('bt'))
# print(symbol.endswith('dt'))
# print(symbol.startswith('dt'))
# #是否包含这个字符在里面
# print('btc' in symbol)
# # 替换 replace是替换冒一个字符串的
# symbol_1 = symbol.replace('btc', 'eth')
# print(symbol_1)
# # 分割 split , 字符串用它后变成列表， join逆操作 把列表转换成字符串
# symbol_2 = 'btcusd, ethusd, xrpusd'
# print(symbol_2.split(', '))
# print(symbol_2.split(', ')[0]) # 可以这样取第一段
# symbol_3 = symbol_2.split(', ')
# print(symbol_3)
# #逆操作
# print(', '.join(symbol_3)) # 用join转换回来字符串
# # 字符中两边的空格是乱起去掉 ， strip
# symbol_4 = ' btcusd '
# print(symbol_4.strip())
