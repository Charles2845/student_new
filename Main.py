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
        self.root.title("hello world")
        self.InitTime = time.time()
        self.frm = Frame(self.root)
        self.frm_T = Frame(self.frm)
        self.root.geometry()

        Button(self.frm, text="help", command=lambda: self.helpMessage()).pack(side=LEFT)  # help
        self.test_in = Entry(self.frm_T)
        self.chooseList = Combobox(self.frm_T, values=['id','管脚数','型号','名称'])
        self.chooseList.pack(side=LEFT)
        self.test_in.pack(side=LEFT)
        Button(self.frm_T, text="export excel", command=lambda: self.outputExcel()).pack(side=RIGHT)  # 导出数据按钮
        Button(self.frm_T, text="import excel", command=lambda: self.importdata()).pack(side=RIGHT)  # 导入数据按钮
        self.frm_T.pack()
        self.frm.pack()
        Button(self.root, text="search", command=lambda: self.search()).pack()  # 查询按钮

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
        self.tree.pack()
        self.mid.pack()
        # 删除按钮
        Button(self.root,text="delete",command=lambda:self.deleteSoc()).pack()
        Button(self.root, text="add", command=lambda: self.addSoc()).pack()
        Button(self.root, text="modify", command=lambda: self.modify()).pack()
        Button(self.root, text="combination search", command=lambda: self.combination()).pack()
        # 时钟模块
        self.label = Label(text="")
        self.label.pack()
        self.update_clock()


    def helpMessage(self):
        mes = "Help info \n Hello"
        tkMessageBox.showinfo('Help',mes)

    def search(self):
        chooseDic = {
            'id':'Id',
            '名称':'name',
            '型号':'typename',
            '管脚数':'number'
        }
        name_choose = chooseDic.get(self.chooseList.get().encode('utf-8'))
        if name_choose:
            self.tree.delete()
            name = self.test_in.get()
            searchString  = "SELECT * FROM test WHERE {}='{}'".format(name_choose,name)
            cursor.execute(searchString)
            data = cursor.fetchall()
            map(self.tree.delete,self.tree.get_children())
            if data:
                i = 1
                for each in data:
                    self.tree.insert('',i,values=each)
                    i += 1
            else:
                tkMessageBox.showinfo('None','No one matched')

    def importdata(self):
        filename = tkFileDialog.askopenfilename()
        data = xlrd.open_workbook(filename)
        table = data.sheets()[0]
        nrows = table.nrows
        for i in range(nrows):
            if i >= 1:
                try:
                    if type(table.row_values(i)[0]) == float:
                        temp = str(table.row_values(i)[0])
                    else:
                        temp = table.row_values(i)[0].encode('utf-8')
                    insertstring = insertSQLstring.format(temp,
                                                          table.row_values(i)[1].encode('utf-8'),
                                                          table.row_values(i)[2].encode('utf-8'),
                                                          table.row_values(i)[3],
                                                          table.row_values(i)[4].encode('utf-8'),
                                                          table.row_values(i)[5].encode('utf-8'))
                    cursor.execute(insertstring)
                except:
                    print i
        conn.commit()
        tkMessageBox.showinfo("import","Import successfully")

    def outputExcel(self):
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
