## lzk_blog

​		使用的 Flask + Vue + Ajax 实现，因为前端不是很熟悉所以写的比较简单。后端的 URL 约定是按照RESTfull的流程，同时/api/module_name/api_name。

#### 总体模块分类

日志模块 ｜ 健身模块 ｜ 后台管理模块 | 个人信息模块 ｜ 登入模块



#### 日志模块功能

主要功能：

1. 上传 md 文件并解析
2. 展示blog，和blog列表
3. 能实现按 tags 分类查询
4. 在登入之后，能删除 ｜ 修改文章
5. 能模糊查询文章，《标题 ｜ 内容》
6. 文章评论，以及更新提醒
7. 记录查看文章的次数并推荐算法

#### 日志模块API

|      接口描述      |                 API                 | 方法 | 参数                      | 放回格式 |
| :----------------: | :---------------------------------: | ---- | ------------------------- | -------- |
| 显示查询的文章简介 |       /api/posts/posts_heads        | GET  | limit=30, page=0, tags=[] | {}       |
|  查看某个文章内容  | /api/posts/posts_content/<posts_id> | GET  |                           | {}       |
|   上传一个md文件   |       /api/posts/posts_upload       | POST | file_name,tags=[]         | {}       |
|    文件模糊查询    |       /api/posts/posts_query        | GET  | query_condition = ""      | {}       |
|                    |                                     |      |                           |          |



#### 登入模块流程

##### 用户视图

1. 日志模块
2. 如果按下登入，或者访问了需要登入的模块则显示登入模块
3. 验证，如果失败放回到登入界面，如果成功，则进入后台模块



##### 逻辑

1. 并不是所有的视图，都是需要通过验证的。通过蓝图来管理这个问题。一条 posts 的蓝图，一条 login 的蓝图的。

2. 有个矛盾的地方，自动加入 url 和希望蓝图管理。我既希望有一个机制可以让我不需要add_url_rule，但是我希望自己能管理蓝图。可以这么做呢？ 





需求：

+ 时间段访问人数。
+ 习惯记录表，没有坚持两天，开始警告
