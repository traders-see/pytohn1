'''
函数是编程当中最常用的概念，一段功能完成的代码封装起来，方便之后反复使用
'''
def def_var(str_var1, str_var2='hello world'):  #def的全名define
    #以下是函数内容，函数的功能 将str_var1,str_var2变量的内容打印出来
    print(str_var1)
    print(str_var2)
    return "打印完成"   # 有了return时候 下面的都不执行了，而且这个是有输出的 也可以没有
def_var([1])
def_var('你好')
def_var('hell', '你好')  # 有默认参数的可以不填 ，添了就代替了
temp = def_var('你好')   # 复制函数 return就会输出
print(temp)