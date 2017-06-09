# coding=utf-8

from Tkinter import *
from Config import *

class AddSoc(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        self.one = Frame(self)
        self.two = Frame(self)
        self.three = Frame(self)
        self.four = Frame(self)
        self.five = Frame(self)
        self.six = Frame(self)
        self.one.pack()
        self.two.pack()
        self.three.pack()
        self.four.pack()
        self.five.pack()
        self.six.pack()

        Label(self.one,text='typename').pack(side=LEFT)
        self.typename = Entry(self.one)
        self.typename.pack(side=RIGHT)

        Label(self.two, text='name').pack(side=LEFT)
        self.name = Entry(self.two)
        self.name.pack(side=RIGHT)

        Label(self.three, text='function').pack(side=LEFT)
        self.function = Entry(self.three)
        self.function.pack(side=RIGHT)

        Label(self.four, text='number').pack(side=LEFT)
        self.number = Entry(self.four)
        self.number.pack(side=RIGHT)

        Label(self.five, text='definition').pack(side=LEFT)
        self.definition = Entry(self.five)
        self.definition.pack(side=RIGHT)

        Label(self.six, text='information').pack(side=LEFT)
        self.information = Entry(self.six)
        self.information.pack(side=RIGHT)

        Button(self,text='Add',command=lambda:self.addtodatabase()).pack()

    def addtodatabase(self):
        typename = self.typename.get()
        name = self.name.get()
        function = self.function.get()
        number = self.number.get()
        definition = self.definition.get()
        information = self.information.get()

        insertstring = insertSQLstring.format(typename.encode('utf-8'),
                                              name.encode('utf-8'),
                                              function.encode('utf-8'),
                                              number,
                                              definition.encode('utf-8'),
                                              information.encode('utf-8'))
        cursor.execute(insertstring)