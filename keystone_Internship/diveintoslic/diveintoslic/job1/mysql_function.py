# -*- coding: utf-8 -*-


import mysql.connector
import uniout  # 解决输出時汉字以ASCII码值形式出现的


class MySql(object):
    global my_cursor, my_db
    # 如果不存在，则创建数据库
    my_db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123123",
    )
    my_cursor = my_db.cursor()
    my_cursor.execute("create database if not exists users_db character set UTF8")  # 不存在時创建数据库

    # 连接数据库--如果表格不存在，创建数据库表格
    my_db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123123",
        database="users_db"
    )

    my_cursor = my_db.cursor()
    sql = "create table if not exists user_message(name VARCHAR(255), id VARCHAR(255) PRIMARY KEY)"
    my_cursor.execute(sql)  # 创建数据库表格

    # 插入几条基本的信息    -------------ignore关键字--不插入重复的关键字记录
    sql = "insert ignore into user_message (name, id) values (%s, %s)"
    val = [
        ('张三', '1234567890@qq.com'),
        ('李四', '1101101100@qq.com'),
        ('王五', '2220002220@qq.com')
    ]
    my_cursor.executemany(sql, val)
    my_db.commit()  # 数据表内容有跟新，必须要使用到这条语句
    print(my_cursor.rowcount, "初始化记录成功!")

    def __init__(self):
        # print("初始化数据库-----")
        pass

    def add_my_sql(self, user_name, user_id):
        sql = "insert ignore into user_message (name, id) values (%s, %s)"
        val = (user_name, user_id)
        my_cursor.execute(sql, val)
        my_db.commit()
        back_status = my_cursor.rowcount
        if back_status == 1:
            print(my_cursor.rowcount, "添加成功！")
        else:
            print(my_cursor.rowcount, "数据库中已有该记录,不做插入操作！")
        return back_status

    def delete_my_sql_name(self, user_name):
        sql = "delete from user_message where name = %s"
        val = (user_name,)
        my_cursor.execute(sql, val)
        my_db.commit()
        back_status = my_cursor.rowcount
        if back_status == 1:
            sentence_back = ("已查询到这条记录，姓名为 %s 的记录删除成功！" %user_name)

        else:
            sentence_back = ("已查询到这条记录，但姓名为 %s 的记录删除失败！" %user_name)

        return sentence_back

    def delete_my_sql_id(self, id):
        sql = "delete from user_message where id = %s"
        val = (id,)
        my_cursor.execute(sql, val)
        my_db.commit()
        back_status = my_cursor.rowcount
        if back_status == 1:
            print(my_cursor.rowcount, "删除成功！")
        else:
            print(my_cursor.rowcount, "数据库中没有匹配该id记录, 删除失败!")

    def lookup_one_my_sql(self, name):
        sql = "select * from user_message where name = %s"
        val = (name,)
        my_cursor.execute(sql, val)

        # for name, _id in my_cursor:
        #     print name, _id
        # my_db.commit()   # 查询的时候不需要这条语句---会出错

        my_result = my_cursor.fetchall()
        back_status = my_cursor.rowcount
        if back_status == 1:
            print(my_result, "查找成功！")
        else:
            print("在数据库中查询无果, 请确认name是否正确！")
        return my_result

    def lookup_all_my_sql(self):
        sql = "select * from user_message"
        my_cursor.execute(sql)
        my_result = my_cursor.fetchall()  # fetchall() 获取所有的记录
        print("查询成功, 记录如下：\n")
        for x in my_result:
            print(x)
        print (type(my_result))
        return my_result

    # 按名字查找，返回查找结果(数字：表示几条记录)
    def query_Record_name(self, user_name):
        sql = "select * from user_message where name = %s"
        val = (user_name,)
        my_cursor.execute(sql, val)
        my_result = my_cursor.fetchall()
        return my_result  # 返回查询的记录--几条

    def update_user_by_name(self, user_name, new_name, new_id):
        sql = "update users set name = %s, id = %s where name = %s"
        val = (user_name, new_name, new_id)
        my_cursor.execute(sql, val)

        my_db.commit()

        # my_result = my_cursor.fetchall()
        back_status = my_cursor.rowcount
        if back_status == 1:
            sentence_back = "更新成功！"
        else:
            sentence_back = "跟新失败！"
        return sentence_back


a = MySql()
name1 = "张三"
name2 = "赵云"
name3 = 'xx'
id1 = "1436006750@qq.com"
id2 = "0000000000@qq.com"
id3 = "000000000xx@qq.com"
# a.add_my_sql(name2, id1)
# a.add_my_sql(name3, id3)
a.lookup_all_my_sql()
# a.lookup_one_my_sql(name3)
# a.delete_my_sql_id(id1)
# a.delete_my_sql_name(name1)
# a.lookup_all_my_sql()
# a.lookup_one_my_sql(name1)


# print ('\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x81')
# print ('\xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe8\xae\xb0\xe5\xbd\x95\xe6\x88\x90\xe5\x8a\x9f!')









