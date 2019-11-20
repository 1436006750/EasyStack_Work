# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, ForeignKey, Table, Column, String, Integer, Boolean, Enum
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


# 添加记录
def orm_insert(name_value, id_value):
    session.query(Users).filter_by(name=name_value).first()
    obj = Users(name=name_value, id=id_value)  # 生成数据对象
    session.add(obj)  # 把要创建的数据对象添加到session里
    session.commit()  # 创建数据


# 查看所有记录：
def orm_query_all():
    result = session.query(Users).all()
    for i in result:
        print i.name, i.id    # 打印所有记录
    return result


# 查询数据，查不到情况下异常处理
def orm_id_query(name_key):
    try:
        ret = session.query(Users).filter_by(name=name_key).first().id
    except AttributeError:
        print '\n*********异常***********'
        return 1
    else:
        print ret
        return ret
    finally:
        print '\n================='


# 删除一条数据
def orm_delete_by_name(name_key):
    session.query(Users).filter(Users.name == name_key).delete()
    session.commit()


# 修改记录
def orm_change_by_name(name_key, new_name, new_id):
    sql = session.query(Users).filter(Users.name == name_key).first()
    sql.name = new_name
    sql.id = new_id
    session.commit()  # 提交记录
    # print sql.name, sql.id  打印的是姓名和id
    # print sql打印的是地址


rm_table()                  # 删除表结构
create_table()              # 创建表结构
session = create_session()  # 创建session


orm_insert('zhengxiang', 100)
orm_insert('zheng', 100)
orm_insert('xiang', 100)


query_data = orm_query_all()
query_data = orm_id_query('zhengxiang')

orm_change_by_name('zhengxiang', 'dainei', 23)
query_data = orm_id_query('zhengxiang')


query_data = orm_query_all()