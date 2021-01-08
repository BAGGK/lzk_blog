"""
这个文件的目的是为了对model（数据库 + 硬盘）进行统一的接口管理 也就是实现:
    门面模式 (外界与数据库的交互，全部用 PostsStruct来完成，也就是对文章的抽象)
那么对于这个模块来说，需要程序做什么呢，
希望能查询，能保存数据，能修改数据，能删除 -> posts 这个抽象的概念，而不是去关心具体的

添加：直接存入就好了
删除：简单
查询：这个问题比较复杂，主要是情况比较多
    单个查询：
    无条件 list 查询：这个其实也简单
    条件查询：问题就是这个了，我该如何去表达条件，建立不同的类么？
修改：简单
"""

from .input import InputFactor
from .model import Tag, Posts
from .tag_context import DBAdapterTag
from .posts_context import DBAdapterPosts


class ModelInterface(object):

    @staticmethod
    def input(context, db_list=None):
        db_list = db_list if db_list else [InputFactor(context)]

        for each_db in db_list:
            each_db(context).save()

    @staticmethod
    def output(query_instance):
        # 1. 得到查询的列表
        # 2. 遍历循环，全部转换成 FitnessContext

        db_list = query_instance.all()
        ret_list = []

        for each_ins in db_list:
            temp_var = AdapterFactor(each_ins)
            ret_list.append(temp_var)
        return ret_list


class AdapterFactor(object):

    def __new__(cls, instance):

        if isinstance(instance, Tag):
            return DBAdapterTag(instance)

        elif isinstance(instance, Posts):
            return DBAdapterPosts(instance)

        return super(AdapterFactor, cls).__new__(cls)
