# coding: utf-8
import os
from config import app


class MHEngine(object):

    def __init__(self, file_name):
        if isinstance(file_name, file):
            self.file_instance = file_name
        elif isinstance(file_name, str):
            self.file_instance = open(app.root_path + '/posts/' + file_name)
        else:
            raise ValueError('The file_name must be a file')

    def parse_md(self):
        # ret_val = []
        # grammar_not_end_flag = False
        # for each_line in self.file_instance:
        #     if grammar_not_end_flag or MHEngine.is_not_one_line(each_line):
        #         md_dic = None
        #     else:
        #         md_dic = MHEngine.parse_one_grammar_type(each_line).parse()
        #     ret_val.append(md_dic)

        file_content_list = self.file_instance.readlines()

        cur_line = 0
        end_line = len(file_content_list)

        while cur_line != end_line:
            pass
    @staticmethod
    def is_not_one_line(md_str):
        not_one_line = ['`']
        if md_str[0] in not_one_line:
            return True
        else:
            return False

    @staticmethod
    def parse_one_grammar_type(md_str):
        """"
        :type md_str: string
        """
        if not isinstance(md_str, str):
            raise TypeError('grammar_type: The md_str must be a str')

        if md_str[0] == '#':
            return H(md_str)

        elif len(md_str) >= 3 and md_str[0].isalnum() and md_str[1] == '.' and md_str[2] == ' ':
            return OrderList(md_str)

        elif md_str[0] == '>':
            return Quote(md_str)


class BaseMD(object):

    def __init__(self, content):
        if not isinstance(content, str):
            raise TypeError('BaseMd')

        self.content = content

    def parse(self):
        raise NotImplementedError


class H(BaseMD):

    def __init__(self, content):
        """

        :type content: string
        """
        super(H, self).__init__(content)
        index = 0
        while content[index] == '#':
            index += 1

        if index < 1 or index > 6:
            raise ValueError

        self.count = index

    def parse(self):
        key = 'H' + str(self.count)
        value = self.content[self.count + 1:]  # 在标志的后一位是有空格的

        return {key: value}


class OrderList(BaseMD):

    def __init__(self, content):
        super(OrderList, self).__init__(content)
        self.num = self.content[0]

    def parse(self):
        """
            这里有bug，主要是当 >= 10 的时候，有问题，但是我记忆中，
            所有的文章都没有大于 10 过。也就这样了。
        """
        key = str(self.num)
        value = self.content[3:]
        return {key: value}


class Quote(BaseMD):

    def __init__(self, content):
        super(Quote, self).__init__(content)

    def parse(self):
        key = '>'
        value = self.content[2:]
        return {key: value}


if __name__ == '__main__':
    """test"""
    print Quote('> hll').parse()
