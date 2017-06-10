# coding=utf-8

from Tkinter import *
from ttk import *
from Config import *

class combination(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.top = Frame(self)
        self.bottom = Frame(self)
        self.top.pack(side=TOP)
        self.searchbutton = Frame(self)
        self.searchbutton.pack(side=BOTTOM)
        self.bottom.pack(side=BOTTOM)


        self.chooseList = Combobox(self.top, values=['管脚数', '型号', '名称', '管脚定义', '简介','功能'])
        self.chooseList.pack(side=LEFT)
        self.data1 = Entry(self.top)
        self.data1.pack(side=RIGHT)
        self.logic = Combobox(self,values=['与', '或', '非'])
        self.logic.pack()

        self.chooseList2 = Combobox(self.bottom, values=['管脚数', '型号', '名称', '管脚定义', '简介','功能'])
        self.chooseList2.pack(side=LEFT)
        self.data2 = Entry(self.bottom)
        self.data2.pack(side=RIGHT)

        Button(self.searchbutton,text='search',command=lambda:self.search()).pack(side=BOTTOM)
        self.returndata = []

    def search(self):
        choosedict = {
            '名称': 'name',
            '型号': 'typename',
            '管脚数': 'number',
            '管脚定义':'definition',
            '简介':'information',
            '功能':'function'
        }
        condition1 = choosedict.get(self.chooseList.get().encode('utf-8'))
        condition2 = choosedict.get(self.chooseList2.get().encode('utf-8'))

        data1 = self.data1.get()
        data2 = self.data2.get()
        logicdic = {
            '与':'AND',
            '或':'OR',
            '非':'NOT'
        }
        logic = logicdic.get(self.logic.get().encode('utf-8'))
        searchString = "SELECT * FROM test WHERE {}='{}' {} {}='{}'".format(condition1,data1,logic,condition2,data2)
        cursor.execute(searchString)
        self.returndata = cursor.fetchall()
        self.destroy()