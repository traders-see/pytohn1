'''
代码没有问题的时候出现错误，
try: #尝试的意思
     执行相关语句这一部分代码，如果执行中间错误，不会停止执行except下语句 ，如果没有错，执行else语句

except:  # 执行相关语句
else
'''
import random  # 随机数
import time  #时间相关
def buy_btc():
    random_num = random.random()  # 随机0-1之间的随机数
    print(random_num)
    if random_num <= 0.2:
        print('买入成功')
        return  # 如果条件符合 不执行下行代码
    else:
        raise ValueError('程序报错 买入失败')
#
# while True:
#     try:
#         buy_btc()
#     except:
#         print('警告！下单出错，在次尝试')
#     else:
#         break
#

tyr_num = 0
while True:
    try:
        buy_btc()  #这个函数 如果报错 就会下行 except
    except:
        print('停止3秒后在次尝试')
        tyr_num += 1
        time.sleep(3)  #3秒后
        if tyr_num >= 5:
            print('超过5次 通知你')
            break  #结束整个循环
        else:
            continue # 如果没有五次继续回去循环
    else:
        break