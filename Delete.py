# coding=utf-8

from Tkinter import *
from Config import *
import tkMessageBox
class DeleteFun(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        Label(self,text='id').pack(side=LEFT)
        self.Socid = Entry(self)
        self.Socid.pack(side=LEFT)
        Button(self,text="delete",command=lambda:self.deleAction()).pack()


    def deleAction(self):
        deletestring = "DELETE FROM test WHERE id='{}'".format(self.Socid.get())
        cursor.execute(deletestring)
        tkMessageBox.showinfo('Success','删除成功！')
        self.destroy()