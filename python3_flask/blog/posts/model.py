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


class Posts(db.Model, DbBase):
    posts_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 文件原来的名字
    posts_filename = db.Column(db.String(128), nullable=False)
    # 文件的存储地址
    posts_path = db.Column(db.String(128))


class PostsTag(db.Model, DbBase):
    posts_id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, primary_key=True)


class Tag(db.Model, DbBase):
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(128), unique=True)


class TagIter(object):

    def __init__(self, tag_list):
        self.tag_list = tag_list
        self.max_count = len(tag_list)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == self.max_count:
            raise StopIteration

        self.index += 1

        return {'tag_name': self.tag_list[self.index - 1].tag_name,
                'tag_id': self.tag_list[self.index - 1].tag_id
                }


class PostsStoreDB(object):

    def __init__(
            self,
            posts_filename,
            posts_path,
            *tags_list,
    ):
        self.filename = posts_filename
        self.path = posts_path
        self.t_list = tags_list

    def save(self):

        # 不实用 BaseDb push 的原因是为了建立事务
        posts_db = Posts(posts_filename=self.filename, posts_path=self.path)
        db.session.add(posts_db)
        db.session.flush()  # 从数据库获取posts_id

        for tag in self.t_list:
            tag_db = PostsTag(posts_id=posts_db.posts_id, tag_id=tag)
            db.session.add(tag_db)

        try:
            db.session.commit()
        except Exception as e:
            print('PostStoreDb error', e)
            db.session.rollback()

    @staticmethod
    def get_list(page=0, limit=30):
        session: Session = db.session
        session.query(Posts, Tag).join()


def test():
    db.drop_all()
    db.create_all()
    Tag(tag_name='C++').save()
    Tag(tag_name='Python').save()
    Tag(tag_name='Mysql').save()
    Tag(tag_name='Flask').save()
