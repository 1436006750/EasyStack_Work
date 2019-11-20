# -*- coding: utf-8 -*-


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql+mysqlconnector://root:123123@localhost:3306/test?charset=utf8')

metadata = MetaData(engine)  # 绑定一个数据源的metadata
# MetaData类主要用于保存表结构，连接字符串等数据，是一个多表共享的对象


# 创建数据库表--------------------------------------------------
student = Table('student', metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String(50), ),
                Column('age', Integer),
                Column('address', String(10)),
                )

metadata.create_all(engine)   # 是来创建表，这个操作是安全的操作，会先判断表是否存在。


# 创建会话-----通过sessionmake方法创建一个Session工厂，然后在调用工厂的方法来实例化一个Session对象
DBSession = sessionmaker(bind=engine)
session = DBSession()


# 添加数据
Base = declarative_base()


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    age = Column(Integer)
    address = Column(String(100))


# 这里的值插入一次就可以了，再次插入会出现键值重复的问题
# student1 = Student(id=1001, name='ling', age=25, address="beijing")
# student2 = Student(id=1002, name='molin', age=18, address="jiangxi")
# student3 = Student(id=1003, name='karl', age=16, address="suzhou")
#
# session.add_all([student1, student2, student3])
# session.commit()
# session.close()


print "=================查询================"
my_student = session.query(Student).filter_by(name="ling").first()
print my_student
print (my_student.id, my_student.name, my_student.address)

# print "=================查询2================"
# my_student = session.query(Student).filter(Student.name.like("%slin"))
# print my_student


print "=================更新================"
my_stdent = session.query(Student).filter(Student.id == 1002).first()
my_stdent.name = "fengxiaoqing"
my_stdent.address = "chengde"
session.commit()
student1 = session.query(Student).filter(Student.id == 1002).first()
print(student1.name, student1.address)


print "=================删除================"
session.query(Student).filter(Student.id == 1001).delete()
session.commit()
session.close()