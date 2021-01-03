from blog import db
from sqlalchemy.orm import Session
from .posts_context import PostsContext
from werkzeug.datastructures import FileStorage

__all__ = ['PostManage']


class DbBase(object):

    def push(self):
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


class Posts(db.Model, DbBase):
    posts_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 文件原来的名字
    posts_filename = db.Column(db.String(128), nullable=False)
    # 文件的存储地址
    posts_path = db.Column(db.String(128))


class PostsTag(db.Model, DbBase):
    posts_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(128), primary_key=True)


class PostManage(object):
    save_path = './post_file'

    def __init__(self, posts_content, posts_path=None):
        self.posts_content: PostsContext = posts_content
        self.save_path = posts_path if posts_path else PostManage.save_path
        self.tags = tags

    def save(self):
        filename = self.file_object.filename
        save_path = self.save_path

        posts_instance = Posts(posts_filename=filename, save_path=save_path)
        db.session.add(posts_instance)
        # 为了获取 posts_id
        db.session.flush()

        # 添加 tags
        if self.tags:
            for each_tag in self.tags:
                tag_instance = PostsTag(posts_id=posts_instance.posts_id, tag_name=each_tag)
                db.session.add(tag_instance)

        try:
            # 提交事务
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    def __getitem__(self, item):
        pass


if __name__ == '__main__':
    pass
