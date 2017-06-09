# coding=utf-8

from Tkinter import *
from Config import *
from ttk import *

class Modify(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        self.top = Frame(self)
        self.bottom = Frame(self)
        self.top.pack()
        self.bottom.pack()

        Label(self.top,text='id').pack(side=LEFT)
        self.socid = Entry(self.top)
        self.socid.pack(side=RIGHT)
        self.chooseList = Combobox(self.bottom, values=['管脚数', '型号', '名称','管脚定义','简介'])
        self.chooseList.pack()
        self.changedata = Entry(self.bottom)
        self.changedata.pack()

        Button(self,text='modify',command=lambda:self.modify()).pack()

    def modify(self):
        choosedict = {
            '名称': 'name',
            '型号': 'typename',
            '管脚数': 'number',
            '管脚定义':'definition',
            '简介':'information'
        }
        name_choose = choosedict.get(self.chooseList.get().encode('utf-8'))
        data = self.changedata.get()
        socid = self.socid.get()
        updateString = "UPDATE test SET {}='{}' WHERE Id='{}'".format(name_choose,data,socid)
        cursor.execute(updateString)
        self.destroy()