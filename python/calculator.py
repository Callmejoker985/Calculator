# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 13:18:10 2021
@author: yuyuy

————实现一个基于Python的建议计算器
————这个计算器是有图形界面的
————一些注释写在最后。

    基于下面这个博主的代码
    如需转发，请注明出处：
        小婷儿的博客python：https://www.cnblogs.com/xxtalhr/
        博客园：https://www.cnblogs.com/xxtalhr/
        CSDN:https://blog.csdn.net/u010986753
"""

import math
from tkinter import *
import tkinter.messagebox

class calculator:
    def __init__(self):
        self.window = Tk()#建立窗口
        #self.window = tkinter.Tk()
        self.window.title("calculator") #计算器名称
        self.window.iconbitmap('D:\\Git_Project\\Calculator\\python\\favicon.ico')#添加图标
        
        self.display = StringVar()#将要在大面板上显示的内容：数字及运算结果
        self.display.set('0')#设置初始内容
        self.display2 = StringVar()#将要在小面板上显示的内容：符号
        self.display3 = StringVar()#将要在小面板上显示存储器的数据
        self.display3_title = StringVar()
        self.display3_title.set ("存储器数字:")
        self.display4 = StringVar()#显示提示
        self.display4.set('来吧!!!')
        
        self.Storage = [] #设置一个存储器
        self.lists = []#设置一个全局变量：运算数字和符号的列表
        self.sign_in = False #添加一个用于判断是否按下运算符号的标志
        
        self.window.minsize(320,454)#计算器最初大小
        self.window.maxsize(680,454)#多出来的部分放历史记录
        
        self.menus()
        self.layout()
        self.window.mainloop()
        
    #计算器菜单界面摆放   
    def menus(self):
        
        # 添加菜单
        # 创建总菜单
        AllMenu = Menu(self.window)
        # 添加子菜单
        FileMenu = Menu(AllMenu, tearoff = 0)
        # 添加选项卡
        FileMenu.add_command(label = '标准型(T)            Alt+1', command = self.myfunc)
        FileMenu.add_command(label = '科学型(S)            Alt+2', command = self.myfunc)
        FileMenu.add_command(label = '程序员(P)            Alt+3', command = self.myfunc)
        FileMenu.add_command(label = '金融计算器(F)        Alt+4', command = self.myfunc)
        # 添加分割线
        FileMenu.add_separator()
        # 添加选项卡
        FileMenu.add_command(label = '历史记录(Y)      Ctrl+H', command = self.myfunc)
        FileMenu.add_command(label = '数字分组(I)', command = self.myfunc)
        # 添加分割线
        FileMenu.add_separator()
        # 添加选项卡
        FileMenu.add_command(label = '基本(B)             Ctrl+F4', command = self.myfunc)
        FileMenu.add_command(label = '单位转换(U)          Ctrl+U', command = self.myfunc)
        FileMenu.add_command(label = '日期计算(D)          Ctrl+E', command = self.myfunc)
        Menu_Work = Menu(FileMenu, tearoff = 0)
        Menu_Work.add_command(label = '抵押(M)', command = self.myfunc)
        Menu_Work.add_command(label = '汽车租赁(V)', command = self.myfunc)
        Menu_Work.add_command(label = '油耗(mpg)(F)', command = self.myfunc)
        Menu_Work.add_command(label = '油耗(l/100km)(U)', command = self.myfunc)
        FileMenu.add_cascade(label = '工作表(W)', menu = Menu_Work)
        AllMenu.add_cascade(label = '查看(V)', menu = FileMenu)
        # 添加子菜单2
        EditMenu = Menu(AllMenu, tearoff = 0)
        # 添加选项卡
        EditMenu.add_command(label='复制(C)         Ctrl+C', command = self.myfunc)
        EditMenu.add_command(label='粘贴(V)         Ctrl+V', command = self.myfunc)
        # 添加分割线
        EditMenu.add_separator()
        # 添加选项卡
        Menu_His = Menu(EditMenu, tearoff = 0)
        Menu_His.add_command(label = '复制历史记录(I)', command = self.myfunc)
        Menu_His.add_command(label = '编辑(E)                      F2', command = self.myfunc)
        Menu_His.add_command(label = '取消编辑(N)               Esc', command = self.myfunc)
        Menu_His.add_command(label = '清除(L)       Ctrl+Shift+D', command = self.myfunc)
        EditMenu.add_cascade(label = '历史记录(H)', menu = Menu_His)
        AllMenu.add_cascade(label = '编辑(E)', menu = EditMenu)

        # 添加子菜单3
        HelpMenu = Menu(AllMenu, tearoff=0)
        # 添加选项卡
        HelpMenu.add_command(label = '查看帮助(V)       F1', command = self.myfunc)
        # 添加分割线
        HelpMenu.add_separator()
        # 添加选项卡
        HelpMenu.add_command(label = '关于计算器(A)', command = self.myfunc)
        AllMenu.add_cascade(label = '帮助(H)', menu = HelpMenu)
        self.window.config(menu = AllMenu)

    #计算器主界面摆放
    def layout(self):

        show_label = Label(self.window, bd=3, bg='black', font=('楷体', 30), fg= 'white', anchor='e', textvariable=self.display)
        show_label.place(x=25, y=20, width=270, height=70)
        # 功能按钮MC
        button_mc = Button(self.window, text='MC', bg = '#666', bd=2, command=self.wait)
        button_mc.place(x=25, y=95, width=50, height=50)
        # 功能按钮MR
        button_mr = Button(self.window, text='MR', bg = '#666', bd=2, command=self.wait)
        button_mr.place(x=80, y=95, width=50, height=50)
        # 功能按钮MS
        button_ms = Button(self.window, text='MS', bg = '#666', bd=2, command=self.wait)
        button_ms.place(x=135, y=95, width=50, height=50)
        # 功能按钮M+
        button_mjia = Button(self.window, text='M+', bg = '#666', bd=2, command=self.wait)
        button_mjia.place(x=190, y=95, width=50, height=50)
        # 功能按钮M-
        button_mjian = Button(self.window, text='M-', bg = '#666', bd=2, command=self.wait)
        button_mjian.place(x=245, y=95, width=50, height=50)
        # 功能按钮←
        button_zuo = Button(self.window, text='←', bg = '#666', bd=2, command=self.dele_one)
        button_zuo.place(x=25, y=150, width=50, height=50)
        # 功能按钮CE
        button_ce = Button(self.window, text='CE', bg = '#666', bd=2, command= self.ce)
        button_ce.place(x=80, y=150, width=50, height=50)
        # 功能按钮C
        button_c = Button(self.window, text='C', bg = '#666', bd=2, command=self.sweeppress)
        button_c.place(x=135, y=150, width=50, height=50)
        # 功能按钮±
        button_zf = Button(self.window, text='±', bg = '#666', bd=2, command=self.zf)
        button_zf.place(x=190, y=150, width=50, height=50)
        # 功能按钮√
        button_kpf = Button(self.window, text='√', bg = '#666', bd=2, command=self.kpf)
        button_kpf.place(x=245, y=150, width=50, height=50)
        # 数字按钮7
        button_7 = Button(self.window, text='7', bg='#bbbbbb', bd=2, command=lambda: self.pressnum('7'))
        button_7.place(x=25, y=205, width=50, height=50)
        # 数字按钮8
        button_8 = Button(self.window, text='8', bg='#bbbbbb', bd=2, command=lambda: self.pressnum('8'))
        button_8.place(x=80, y=205, width=50, height=50)
        # 数字按钮9
        button_9 = Button(self.window, text='9', bg='#bbbbbb', bd=2, command=lambda: self.pressnum('9'))
        button_9.place(x=135, y=205, width=50, height=50)
        # 功能按钮/
        button_division = Button(self.window, text='/', bg='#708069', bd=2, command=lambda: self.presscalculate('/'))
        button_division.place(x=190, y=205, width=50, height=50)
        # 功能按钮%
        button_remainder = Button(self.window, text='//', bg='#708069', bd=2, command=lambda:self.presscalculate('//'))
        button_remainder.place(x=245, y=205, width=50, height=50)
        # 数字按钮4
        button_4 = Button(self.window, text='4', bg='#bbbbbb', bd=2, command=lambda: self.pressnum('4'))
        button_4.place(x=25, y=260, width=50, height=50)
        # 数字按钮5
        button_5 = Button(self.window, text='5', bg='#bbbbbb', bd=2, command=lambda: self.pressnum('5'))
        button_5.place(x=80, y=260, width=50, height=50)
        # 数字按钮6
        button_6 = Button(self.window, text='6', bg='#bbbbbb', bd=2, command=lambda: self.pressnum('6'))
        button_6.place(x=135, y=260, width=50, height=50)
        # 功能按钮*
        button_multiplication = Button(self.window, text='*', bg='#708069', bd=2, command=lambda: self.presscalculate('*'))
        button_multiplication.place(x=190, y=260, width=50, height=50)
        # 功能按钮1/x
        button_reciprocal = Button(self.window, text='1/x', bg='#708069', bd=2, command=self.ds)
        button_reciprocal.place(x=245, y=260, width=50, height=50)
        # 数字按钮1
        button_1 = Button(self.window, text='1', bg='#bbbbbb', bd=2, command=lambda: self.pressnum('1'))
        button_1.place(x=25, y=315, width=50, height=50)
        # 数字按钮2
        button_2 = Button(self.window, text='2', bg='#bbbbbb', bd=2, command=lambda: self.pressnum('2'))
        button_2.place(x=80, y=315, width=50, height=50)
        # 数字按钮3
        button_3 = Button(self.window, text='3', bg='#bbbbbb', bd=2, command=lambda: self.pressnum('3'))
        button_3.place(x=135, y=315, width=50, height=50)
        # 功能按钮-
        button_subtraction = Button(self.window, text='-', bg='#708069', bd=2, command=lambda: self.presscalculate('-'))
        button_subtraction.place(x=190, y=315, width=50, height=50)
        # 功能按钮=
        button_equal = Button(self.window, text='=', bg='#708069', bd=2, command=lambda: self.pressequal())
        button_equal.place(x=245, y=315, width=50, height=105)
        # 数字按钮0
        button_0 = Button(self.window, text='0', bg='#bbbbbb', bd=2, command=lambda: self.pressnum('0'))
        button_0.place(x=25, y=370, width=105, height=50)
        # 功能按钮.
        button_point = Button(self.window, text='.', bg='#bbbbbb', bd=2, command=lambda: self.pressnum('.'))
        button_point.place(x=135, y=370, width=50, height=50)
        # 功能按钮+
        button_plus = Button(self.window, text='+', bg='#708069', bd=2, command=lambda: self.presscalculate('+'))
        button_plus.place(x=190, y=370, width=50, height=50)
        #左下角显示输入的符号
        show_label2 = Label(self.window, bd=3, bg='white', font=('宋体', 8), anchor='e', textvariable=self.display2)
        show_label2.place(x=130, y=425)
        self.change_color()
        #右上角显示存储器数字
        show_label3 = Label(self.window, bd=3, bg='white', font=('宋体', 8), anchor='e', textvariable=self.display3)
        show_label3.place(x=220, y=0)
        
        show_label3_title = Label(self.window, bd=3, font=('宋体', 8), anchor='e', textvariable=self.display3_title)
        show_label3_title.place(x=150, y=0)
        #左上角显示状态
        show_label4 = Label(self.window, bd=3,  font=('宋体', 8), anchor='e', textvariable=self.display4)
        show_label4.place(x=25, y=0)

    #左下颜色变换
    def change_color(self):
        if self.sign_in == False:
            l_show1 = Label(self.window, 
                        text='输入符号后变为红色',    # 标签的文字
                        bg='green',     # 标签背景颜色
                        font=('Arial', 8),     # 字体和字体大小
                        #width=5, height=2  # 标签长宽（以字符长度计算）
                        )
            l_show1.place(x=25, y=425)

        else:
            l_show1 = Label(self.window, 
                        text='输入符号后变为红色',    # 标签的文字
                        bg='red',     # 标签背景颜色
                        font=('Arial', 8),     # 字体和字体大小
                        #width=5, height=2  # 标签长宽（以字符长度计算）
                        )
            l_show1.place(x=25, y=425)
            
    #计算器菜单功能
    def myfunc(self):
        messagebox.showinfo('','程序员懒死在电脑前，打死也做不出的功能，只是装饰而已～')
'''    
    def Mx(self,operator):

        if operator == 'MC':
            self.Storage.clear()
            self.Storage.append('0')
        elif operator == 'MR':
            if self.sign_in:
                self.display.set('0')
            self.Storage.append(self.display.get())
            expression = ''.join(self.Storage)
            try:
                result = eval(expression)
            except:
                result = '输入错误'
            self.display.set(result)
            sign_in = True
        elif operator == 'MS':
            self.Storage.clear()
            self.Storage.append(self.display.get())
        elif operator == 'M+':
            self.Storage.append(self.display.get())
        elif operator == 'M-':
            if self.display.get().startswith('-'):
                self.Storage.append(self.display.get())
            else:
                self.Storage.append('-' + self.display.get())
        expression1 = ''.join(self.Storage)
        res = eval(expression1)
        self.display3.set(str(res)[:4])
        self.display4.set("正在输入")
'''        
    #数字方法
    def pressnum(self,num):
        # 全局化变量
        # 判断是否按下了运算符号
        if self.sign_in == False:
            pass
        else:
            self.display.set(0)
            # 重置运算符号的状态
            self.sign_in = False
        if num == '.':
            num = '0.'
        # 获取面板中的原有数字
        oldnum = self.display.get()
        # 判断界面数字是否为0
        if oldnum == '0':
            self.display.set(num)
        else:
            # 连接上新按下的数字
            newnum = oldnum + num

            # 将按下的数字写到面板中
            self.display.set(newnum)
        self.change_color()
        self.display4.set("正在输入")

    #运算函数
    def presscalculate(self,sign):
        # 保存已经按下的数字和运算符号
        # 获取界面数字
        self.display2.set(sign)
        num = self.display.get()
        self.lists.append(num)
        # 保存按下的操作符号
        self.lists.append(sign)
        # 设置运算符号为按下状态
        self.sign_in = True
        self.change_color()
        self.display4.set("正在输入")
        


    #获取运算结果
    def pressequal(self):
        # 获取所有的列表中的内容（之前的数字和操作）
        # 获取当前界面上的数字
        curnum = self.display.get()
        # 将当前界面的数字存入列表
        self.lists.append(curnum)
        # 将列表转化为字符串
        calculatestr = ''.join(self.lists)
        # 使用eval执行字符串中的运算即可
        endnum = eval(calculatestr)
        # 将运算结果显示在界面中
        self.display.set(str(endnum)[:10])
        if self.lists != 0:
            self.sign_in = True
        # 清空运算列表
        self.lists.clear()
        self.display4.set("计算完成")

    #暂未开发说明
    def wait(self):
        messagebox.showinfo('','功能在努力的实现，请期待2.0版本的更新')

    #CE案件功能
    def ce(self):
        self.display.set('0')
        self.display4.set("重新输入")
        
    #←按键功能
    def dele_one(self):
        if self.display.get() == '' or self.display.get() == '0':
            self.display.set('0')
            return
        else:
            num = len(self.display.get())
            if num > 1:
                strnum = self.display.get()
                strnum = strnum[0:num - 1]
                self.display.set(strnum)
            else:
                self.display.set('0')
        self.display4.set("删除一位")

    #±按键功能
    def zf(self):
        strnum = self.display.get()
        if strnum[0] == '-':
            self.display.set(strnum[1:])
        elif strnum[0] != '-' and strnum != '0':
            self.display.set('-' + strnum)
        self.display4.set("正负号")

    #1/x按键功能
    def ds(self):
        try:
            dsnum = 1 / int(self.display.get())
        except:
            dsnum = '输入错误'
        self.display.set(str(dsnum)[:10])
        if self.lists != 0:
            self.ispresssign = True
        # 清空运算列表
        self.lists.clear()
        self.display4.set("倒数完成")

    #C按键功能
    def sweeppress(self):
        self.lists.clear()
        self.display.set('0')
        self.display4.set("来吧!!!")
        self.display4.set("再算一次")

    #√按键功能
    def kpf(self):
        strnum = float(self.display.get())
        endnum = math.sqrt(strnum)
        if str(endnum)[-1] == '0':
            self.display.set(str(endnum)[:-2])
        else:
            self.display.set(str(endnum)[:10])
        if self.lists != 0:
            self.ispresssign = True
        # 清空运算列表
        self.lists.clear()
        self.display4.set("开平方完成")

#实例化对象
mycalculator = calculator()        
        
        


'''
————————————————用from tkinter import *—————————————————
import tkinter 使用这个语句时，对应下面1的句式
这么做相当于在全局使用了tkinter.xxx,
也就是直接写xxx就好,不必在前面加tkinter.。
————————————————————————————————————————————————————————
———————————————————tkinter.stringvar————————————————————
tkinter.stringvar可以理解为识别输入的字符。
intVar是对“整数”类型的包装，stringVar是对“字符串”类型的包装。
在实际操作中只用tkinter.stringvar就好，
因为可以做到类型转换。
————————————————————————————————————————————————————————
'''
