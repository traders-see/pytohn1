# if的意思（如果）的意思， 他的输出必须是布尔值，
'''
if 条件A满足布尔值
elif 条件B满足布尔值
elif 条件C满足布尔值
else 以上所有条件都不满足的时候执行
'''
# symbol = 'btcusd'
# if symbol.endswith('usd'):     # a条件
#     print(symbol, '美元计价')
# elif symbol.endswith('btc'):   # b条件
#     print(symbol, '比特币计价')
# elif symbol.endswith('eth'):    # c条件
#     print(symbol, '以太坊计价')
# else:                            # 都不满足
#     print(symbol, '都不满足')
#满足中间任何一个条件后 下面条件满足的时候也不执行了。

'''
for 循环语句 就是重复事情， 不用复制好几次
'''
# list_var = ['btc', 'usd' , 'eth']
# print(list_var[0])
# print(list_var[1])
# print(list_var[2])
# #for
# for i in list_var:
#     print(i)
#     print('打印了')
# for i in range(1, 10):
#     print('打印')
#
# sum_num = 0
# for i in [1,2,3,4,5,6,7,8,9,10]:  # range(10+1)一样的
#     sum_num +=i
#     print(i, sum_num)
# # 案例
# symbol_list = ['btcusd', 'xrpbtc', 'xrpusd', 'ethusd','xrpeth']
# for symbol in symbol_list:
#     if symbol.endswith('usd'):
#         print(symbol, '美元计价')
#         continue # 有这个就是找了这个条件下面不执行，在回去下轮语句循环
#     if symbol.endswith('btc'):
#         print(symbol, 'btc计价')
#         continue
#     if symbol.endswith('eth'):
#         print(symbol, '以太坊计价')
#         continue
#     print(symbol, '不知道以什么价格')

# while 条件 死循环  只有当条件不满足的时候才会退出
num = 1
max_num = 10
sum_num = 0
while True:
    sum_num += num
    num += 1
    print(sum_num, num)
    if num == max_num+1:
        break  # IF这条满足的时候跳出所有循环语句