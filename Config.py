#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
conn = pymysql.connect(host='127.0.0.1',user='',passwd='',db='',charset='utf8')
cursor = conn.cursor()
insertSQLstring = "INSERT INTO test (typename,name,function,number,definition,information) VALUES ('{}','{}','{}','{}','{}','{}')"

cursor.execute("DROP TABLE IF EXISTS test")
sqlstring = """CREATE TABLE test(
                Id INT PRIMARY KEY AUTO_INCREMENT,
                typename TEXT,
                name TEXT,
                function TEXT,
                number INT(255),
                definition TEXT,
                information TEXT)"""

cursor.execute(sqlstring)
