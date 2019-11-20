# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, String, schema
from sqlalchemy.ext.declarative import declarative_base


def table_args():
    return {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }


Base = declarative_base()


class Test(Base):
    """defined a Test"""
    __tablename__ = 'test'
    __table_args__ = (
        schema.UniqueConstraint('id', name='uniq_test_id'),
        table_args()
    )
    id = Column(Integer, primary_key=True, autoincrement='auto', nullable=False)
    name = Column(String(255), nullable=False)
    sex = Column(String(40), nullable=False)







