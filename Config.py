#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
# 数据库连接信息
conn = pymysql.connect(host='127.0.0.1',user='root',passwd='jw07190811',db='test',charset='utf8')
cursor = conn.cursor()
insertSQLstring = "INSERT INTO test (typename,name,function,number,definition,information) VALUES ('{}','{}','{}','{}','{}','{}')"

# 每次创建新的test表格
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
