from blog import db
from sqlalchemy.orm import Session


class DbBase(object):

    def save(self):
        session: Session = db.session

        try:
            session.add(self)
            session.commit()
        except Exception as e:
            print(str(self.__class__) + 'push error:', e)
            session.rollback()

    def delete(self):
        session: Session = db.session
        try:
            session.delete(self)
            session.commit()
        except Exception as e:
            class_str = str(self.__class__)
            print(class_str + 'delete error', e)

    @classmethod
    def get_list(cls, page=0, limit=30):
        session: Session = db.session
        """
        如果 limit = 0 , 则代表不限制
        """
        if limit == 0:
            ret_data = session.query(cls).all()
        else:
            ret_data = session.query(cls).limit(limit).offset(page * limit).all()
        return ret_data
