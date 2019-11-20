# -*- coding: utf-8 -*-


from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker


class API(object):
    def __init__(self):
        args = 'mysql+mysqlconnector://root:123123@localhost:3306/test'
        engine = create_engine(args, poolclass=NullPool)
        session_ = sessionmaker(bind=engine)
        self.session = session_()

    def create(self, db, **body):
        self.session.add(db(**body))
        return 'CREATED'

    # 获取所有内容
    def get_all_content(self, db):
        result = list(t.__dict__ for t in self.session.query(db).all())
        for i in xrange(0, len(result)):
            result.pop('_sa_instance_state', None)
        return 'OK', result

    def delete_context(self, db, db_attr, value):
        res = self.session.query(db).filter(db_attr == value).delete()
        if res:
            self.session.commit()
            return 'OK'
        else:
            return False

    def delete_all(self, db):
        self.session.query(db).delete()
        self.session.commit()
        return 'OK'










