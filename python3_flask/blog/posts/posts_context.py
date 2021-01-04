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


if __name__ == '__main__':
    pass
