# coding=utf-8
__author__ = ""

from Tkinter import *
import time
import datetime
from ttk import *
import tkFileDialog
import xlrd,xlwt
import tkMessageBox
from Config import *
from Delete import *
from AddSoc import *
from Modify import *
from combination import *

class app:
    def __init__(self):
        self.root = Tk()
        self.root.title("芯片查询软件")
        self.InitTime = time.time()
        self.frm_T = Frame(self.root)
        self.frm_T2 = Frame(self.root)
        self.root.geometry()
        Button(self.root, text="帮助", command=lambda: self.helpMessage()).pack(side=TOP)  # help
        Button(self.frm_T2, text="导出 excel", command=lambda: self.outputExcel()).pack(side=RIGHT)  # 导出数据按钮
        Button(self.frm_T2, text="导入 excel", command=lambda: self.importdata()).pack(side=RIGHT)  # 导入数据按钮
        Button(self.frm_T2,text="删除芯片",command=lambda:self.deleteSoc()).pack(side=LEFT)
        Button(self.frm_T2, text="增加芯片", command=lambda: self.addSoc()).pack(side=LEFT)
        Button(self.frm_T2, text="修改芯片信息", command=lambda: self.modify()).pack(side=LEFT)
        Button(self.frm_T2, text="组合查询", command=lambda: self.combination()).pack(side=LEFT)

        self.test_in = Entry(self.frm_T)
        self.chooseList = Combobox(self.frm_T, values=['功能','管脚数','型号','名称'])
        self.chooseList.pack(side=LEFT)
        self.test_in.pack(side=LEFT)
        self.frm_T.pack()
        self.frm_T2.pack()
        Button(self.frm_T, text="搜索", command=lambda: self.search()).pack(side=BOTTOM)  # 查询按钮

        self.mid = Frame(self.root)
        self.tree = Treeview(self.mid, show="headings",columns=('col1', 'col2', 'col3', 'col4', 'col5', 'col6','col7'))
        self.tree.column('col1', width=100, anchor='center')
        self.tree.column('col2', width=100, anchor='center')
        self.tree.column('col3', width=100, anchor='center')
        self.tree.column('col4', width=100, anchor='center')
        self.tree.column('col5', width=100, anchor='center')
        self.tree.column('col6', width=100, anchor='center')
        self.tree.column('col7', width=100, anchor='center')

        self.tree.heading('col1', text='id')
        self.tree.heading('col2', text='型号')
        self.tree.heading('col3', text='名称')
        self.tree.heading('col4', text='功能')
        self.tree.heading('col5', text='管脚数')
        self.tree.heading('col6', text='管脚定义')
        self.tree.heading('col7', text='芯片介绍')
        self.tree.bind("<Double-1>", self.onDBClick)
        self.tree.pack()
        self.mid.pack()
        # 时钟模块
        self.label = Label(text="")
        self.label.pack()
        self.update_clock()


    def helpMessage(self):
        mes = """欢迎使用芯片查询系统！
在界面选择“id、名称、型号、功能、管脚数”，之后输入需要查询的相应信息即可进行芯片属性的查询！
更多功能介绍：
1、“文件”可选择“导入更多芯片信息excel表格”、“导出所查询的芯片信息excel表格”。
2、“修改”可选择“删除”、“增加”、“修改”，对芯片信息做出相应改动。
3、“查询”可选择“组合查询”，选择所需要查询的芯片信息条件以及所需要的组合“与”、“或”、“非”即可进行查询。
ps：本查询系统还有计时器功能，可以看到您使用本系统的时间喔！
希望我有帮到你⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄"""
        tkMessageBox.showinfo('Help',mes)

    def search(self):
        chooseDic = {
            '名称':'name',
            '型号':'typename',
            '管脚数':'number',
            '功能':'function'
        }
        name_choose = chooseDic.get(self.chooseList.get().encode('utf-8'))
        if name_choose:
            self.tree.delete()
            name = self.test_in.get()  # 通过Entry获取输入信息，然后拼接成SQL查询语句
            searchString  = "SELECT * FROM test WHERE {}='{}'".format(name_choose,name)
            cursor.execute(searchString)
            data = cursor.fetchall()
            map(self.tree.delete,self.tree.get_children())
            if data:
                i = 1
                for each in data:
                    # treeview显示查询到的信息
                    self.tree.insert('',i,values=each)
                    i += 1
            else:
                tkMessageBox.showinfo('None','没有匹配项')

    def onDBClick(self,event):
        # 双击显示详细信息
        item = self.tree.selection()[0]
        tkMessageBox.showinfo('Detail',self.tree.item(item, "values"))

    def importdata(self):
        # 利用xlrd读取excel信息并分别倒入到mysql当中
        filename = tkFileDialog.askopenfilename()
        data = xlrd.open_workbook(filename)
        table = data.sheets()[0]
        nrows = table.nrows
        for i in range(nrows):
            if i >= 1:
                try:
                    if type(table.row_values(i)[1]) == float:
                        temp = str(table.row_values(i)[1])
                    else:
                        temp = table.row_values(i)[1].encode('utf-8')
                    insertstring = insertSQLstring.format(temp,
                                                          table.row_values(i)[2].encode('utf-8'),
                                                          table.row_values(i)[3].encode('utf-8'),
                                                          table.row_values(i)[4],
                                                          table.row_values(i)[5].encode('utf-8'),
                                                          table.row_values(i)[6].encode('utf-8'))
                    cursor.execute(insertstring)
                except Exception as e:
                    print e
                    print i
        conn.commit()
        tkMessageBox.showinfo("import","Import successfully")

    def outputExcel(self):
        # 读取数据库中现有的数据然后写入新的excel
        cursor.execute("SELECT * FROM test")
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Main')
        filename = tkFileDialog.asksaveasfilename(filetypes=[('Excel files', '.xls')])
        data = cursor.fetchall()
        for each in range(len(data)):
            for single in range(len(data[each])):
                if type(data[each][single]) == unicode:
                    temp = data[each][single]
                else:
                    temp = str(data[each][single])
                ws.write(each,single,temp)
        wb.save(filename+'.xls')
        tkMessageBox.showinfo('Export','Export Successfully')

    def deleteSoc(self):
        DeleteFun()

    def addSoc(self):
        AddSoc()

    def modify(self):
        Modify()

    def combination(self):
        # 组合查询
        combine = combination()
        self.root.wait_window(combine)
        data = combine.returndata
        map(self.tree.delete, self.tree.get_children())
        if data:
            i = 1
            for each in data:
                self.tree.insert('', i, values=each)
                i += 1
        else:
            tkMessageBox.showinfo('None','No one matched')


    def update_clock(self):
        now = time.time()-self.InitTime
        show = time.strftime("%M:%S",time.localtime(now))
        self.label.configure(text=show)
        self.root.after(1000, self.update_clock)

if __name__ == '__main__':
    test = app()
    test.root.mainloop()
