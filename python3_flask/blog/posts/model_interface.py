"""
这个文件的目的是为了对model（数据库 + 硬盘）进行统一的接口管理 也就是实现: 门面模式
那么对于这个模块来说，需要程序做什么呢，
希望能查询，能保存数据，能修改数据，能删除 -> posts 这个抽象的概念，而不是去关心具体的
"""
from .model import PostsStoreDB


class PostsStruct(object):
    """对 posts 的抽象"""

    def __init__(self, filename, content, tags):
        if tags is not list:
            raise TypeError('tags must be a list')

        self.filename = filename
        self.content = content
        self.tags = tags


class PostsStorageInterface(object):
    """
    将外部接口提供接口，传入获取返回 PostsStruct
    """

    @staticmethod
    def save(posts_instance):
        posts_instance: PostsStruct

        # if posts_instance is not PostsStruct:
        #     raise TypeError('The save function should be PostsStruct')

    def get_list(self):
        pass


PostsStorageInterface.save(1)
