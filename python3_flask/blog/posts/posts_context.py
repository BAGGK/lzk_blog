from markdown import markdown
import os
from .model import PostsStoreDB
from uuid import uuid4
from werkzeug.datastructures import FileStorage


class PostsContext(object):
    """
        这个类：完成对posts的抽象和封装。
    """
    content: str

    def __init__(
            self, posts_content,
            posts_title,
            posts_up_time=None,
            *posts_tags

    ):
        # 以下是实例传递参数
        self.content = posts_content
        self.title = posts_title
        self.up_time = posts_up_time
        self.tags = posts_tags
        self.introduction = None

    def get_file_introduction(self):
        """取出文件的简介部分"""
        if self.introduction:
            return self.introduction
        else:
            self.introduction = self.__parse_introduction()
            return self.introduction

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

    def save(self):
        """
        我总是纠结一些主动和被动的关系，这个类该不该有保存呢
        """
        # 存入文件
        security_name = uuid4().hex
        save_path = '../file_storage/'
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        fd = open(save_path + security_name, mode='w')
        fd.write(self.content)
        fd.close()

        # 存入db
        posts_db = PostsStoreDB(self.title, save_path, *self.tags)
        posts_db.save()

    @staticmethod
    def __content_to_html(content):
        return markdown(content, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])

    def get_introduction_html(self):
        if not hasattr(self, 'introduction'):
            self.get_file_introduction()

        return self.__content_to_html(self.introduction)

    def get_posts_html(self):
        return self.__content_to_html(self.content)


class FileAdapterPosts(PostsContext):

    def __init__(self, fd, tags=None):

        if fd is str:
            self.fd = open(fd)
        else:
            self.fd = fd

        content = []
        read_data = self.fd.read()
        while read_data:
            content.append(read_data)
            read_data = self.fd.read()
        content = ''.join(content)

        super(FileAdapterPosts, self).__init__(
            content,
            os.path.basename(self.fd.name),
            os.path.getctime(self.fd.name),
            *tags
        )


class FileStorageAdapterPosts(PostsContext):
    def __init__(self, fd, *tags):
        fd: FileStorage

        content = fd.stream.read().decode('utf-8')
        title = fd.filename

        super(FileStorageAdapterPosts, self).__init__(content, title, None, *tags)


if __name__ == '__main__':
    pass
