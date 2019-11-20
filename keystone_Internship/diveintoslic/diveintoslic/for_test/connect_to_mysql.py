# -*- coding: utf-8 -*-

# 导入相关库
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, PrimaryKeyConstraint


# Mysql数据库连接字符串
CONSTR = 'mysql+mysqlconnector://root:123123@localhost:3306/test?charset=utf8'

# 初始化数据库连接对象
engine = create_engine(CONSTR, echo=True)
db_session = sessionmaker(bind=engine)  # sessionmaker()生成数据库会话类。我们可以把session当成的一个数据库连接对象
session = db_session()


# 定义基类
Base = declarative_base()


class User(Base):
    # 显示声明关联的数据表名称
    __tablename__='user'

    # 表的结构
    # 主键Id
    id = Column(Integer, name='Id', primary_key=True)
    # name非空
    name = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)


user = User(name='kikay', age=0)

session.add(user)  # 添加
session.commit()   # 提交---------可在添加多条后一起提交
session.close()    # 关闭




