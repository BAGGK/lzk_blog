from werkzeug.datastructures import FileStorage
from .tag_context import TagContext
from .model import Posts


class PostsContext(object):
    """
        这个类：完成对posts的抽象和封装。
    """

    def __init__(self, posts_id, filename, content,
                 introduction, tags, last_modify_time):
        # 以下是实例传递参数
        for k, v in locals().items():
            if k == 'self':
                continue
            elif v is not None:
                self.__setattr__(k, v)

    def __getattr__(self, item):
        if item == 'posts_id':
            self.posts_id = 0
            return self.posts_id

        if item == 'introduction':
            self.introduction = self.__parse_introduction()
            return self.introduction

        if item == 'content':
            self.content = 'writing .....'
            return self.content

        if item == 'last_modify_time':
            self.last_modify_time = 0
            return self.last_modify_time

        if item == 'tags':
            self.tags = []
            return self.tags

        if item == 'filename':
            self.filename = 'filename'
            return self.filename

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


class FileStorageAdapter(PostsContext):
    def __init__(self, fs, tags_list, last_modify_time):
        fs: FileStorage

        content = fs.stream.read().decode('utf-8')
        tags = []
        for each_tag in tags_list:
            tags.append(IDAdapterTag(each_tag))
        super(FileStorageAdapter, self).__init__(None, fs.filename, content,
                                                 None, tags, last_modify_time)


class DBAdapterPosts(PostsContext):
    def __init__(self, posts_ins):
        posts_ins: Posts
        tags = []

        for each_tag in posts_ins.tags:
            tags.append(TagContext(each_tag.tag_id, each_tag.name))

        super(DBAdapterPosts, self).__init__(
            posts_ins.posts_id, posts_ins.filename,
            posts_ins.content, None, tags, posts_ins.last_modify_time
        )
