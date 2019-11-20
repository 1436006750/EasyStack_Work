# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


HOSTNAME = "localhost"
PORT = "3306"
DATABASE = "test"
USERNAME = "root"
PASSWORD = "123123"

# 1、连接数据库
connect_mysql_engine \
    = create_engine("mysql+mysqlconnector://{username}:{password}@{host}:{port}/{db}?charset=utf8".
                    format(username=USERNAME, password=PASSWORD, host=HOSTNAME, port=PORT, db=DATABASE),
                    encoding='utf-8'
                    )

# 2、生成ORM基类
Base = declarative_base()


# 3、继承基类，定义表结构
class Users(Base):
    # 创建orm对象
    __tablename__ = 'users'  # 数据表名
    number = Column(Integer, primary_key=True)  # 字段，设为主键，默认不用赋值，此字段会自增
    name = Column(String(32))
    id = Column(Integer)


# 4.1创建数据表
def create_table():  # 在数据库中创建表，已存在则不创建
    Base.metadata.create_all(connect_mysql_engine)


# 4.2删除表结构
def rm_table():
    Base.metadata.drop_all(connect_mysql_engine)


def create_session():
    # 创建与数据库的会话session class ,这里返回给session的是class
    session_class = sessionmaker(bind=connect_mysql_engine)
    # 生成session实例
    return session_class()


create_table()  # 创建表结构

session = create_session()  # 创建session
# print type(session)    # <class 'sqlalchemy.orm.session.Session'>


class Sql_Operation(object):

    # 添加记录
    def orm_insert(self, name_value, id_value):
        res = session.query(Users).filter_by(name=name_value).first()
        if res:
            print "数据库中已有该记录(不允许重复),请重新选择姓名!"
            return "Failure"
        else:
            obj = Users(name=name_value, id=id_value)  # 生成数据对象
            session.add(obj)  # 把要创建的数据对象添加到session里
            session.commit()  # 创建数据
            return "Success"

    # 查看所有记录：--------------return 一个list出错,return 字典OK
    def orm_query_all(self):
        result = session.query(Users).all()
        dictionary = {}
        for i in result:
            # dictionary[i.name] = i.id
            dictionary[i.number] = i.name, i.id
        return dictionary

        # for i in result:
        #     print i.name, i.id  # 打印所有记录
        # # print type(result)  <type 'list'>
        # return result

    # 查询数据，查不到情况下异常处理
    def orm_query_by_name(self, name_key):
        res = session.query(Users).filter_by(name=name_key).first()
        if res:
            print type(res)
            print "查询记录为：", res.name, res.id
            # return "Success"
            return "Query this record Success!", res.name, res.id
        else:
            print '数据库中没有这条记录'
            return "Failure to query this record!"

    # 删除一条数据
    def orm_delete_by_name(self, name_key):
        res0 = session.query(Users).filter(Users.name == name_key).first()
        res1 = session.query(Users).filter(Users.name == name_key).delete()
        if res1:
            session.commit()
            return "Delete this record Success", res0.name, res0.id
        else:
            return "Failure to delete this record!"

    # 修改记录
    def orm_change_by_name(self, name_key, new_name, new_id):
        res = session.query(Users).filter(Users.name == name_key).first()
        if res:
            res.name = new_name
            res.id = new_id
            session.commit()  # 提交记录
            return "Success to change this record to :", res.name, res.id
        else:
            print "数据库中尚无该记录，请先添加该记录！"
            return "Failure to find this record , Unable to change!"
        # print sql.name, sql.id  打印的是姓名和id
        # print sql打印的是地址


# 操作：
operator = Sql_Operation()
# operator.orm_query_all()
operator.orm_insert('zheng', 23)
operator.orm_insert('xiang', 33)
operator.orm_insert('li', 18)
# operator.orm_query_by_name('xiang')
# operator.orm_delete_by_name('zheng')
