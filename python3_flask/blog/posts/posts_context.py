from markdown import markdown
import os
from uuid import uuid4
from werkzeug.datastructures import FileStorage


class PostsContext(object):
    """
        这个类：完成对posts的抽象和封装。
    """

    def __init__(
            self,
            posts_content,
            posts_title,
            posts_tags
    ):
        # 以下是实例传递参数
        self.content = posts_content
        self.title = posts_title
        self.up_time = None
        self.tags = posts_tags

    def __getattr__(self, item):
        if item == 'introduction':
            self.introduction = self.__parse_introduction()
            return self.introduction
        raise AttributeError("AttributeError: '%s' object has no attribute '%s"
                             % (self.__class__.__name__, item))

    def __parse_introduction(self):
        # 找到 第二行
        first_loop_flag = True
        ret_val = ''
        for each_line in self.content.splitlines():
            if first_loop_flag:
                first_loop_flag = False
                continue
            each_line = each_line.strip()
            if each_line != '':
                ret_val = each_line
        return ret_val


class FileStoreAdapter(PostsContext):
    def __init__(self):
        super(FileStoreAdapter, self).__init__(1, 1, 1)


if __name__ == '__main__':
    temp_var = PostsContext(1, 1, 1)
