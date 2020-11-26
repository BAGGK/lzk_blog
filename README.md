## lzk_blog

​		使用的 Flask + Vue + Ajax 实现，因为前端不是很熟悉所以写的比较简单。后端的 URL 约定是按照RESTfull的流程，同时/api/module_name/api_name。

#### 需求

​		主要是用来管理最近的blog实现增删改查，同时拥有对个人信息能进行整理。

日志模块 ｜ 健身模块 ｜ 后台管理模块 | 个人信息模块 ｜ 登入模块

#### 日志模块

|      接口描述      |                 API                 | 方法 | 参数                      | 放回格式 |
| :----------------: | :---------------------------------: | ---- | ------------------------- | -------- |
| 显示查询的文章简介 |       /api/posts/posts_heads        | GET  | limit=30, page=0, tags=[] | {}       |
|  查看某个文章内容  | /api/posts/posts_content/<posts_id> | GET  |                           | {}       |
|   上传一个md文件   |       /api/posts/posts_upload       | POST | file_name                 | {}       |
|    文件模糊查询    |       /api/posts/posts_query        | GET  | query_condition = ""      | {}       |
|                    |                                     |      |                           |          |

#### 健身模块

| 接口描述 |         API          | 方法 |   参数   | 放回格式 |
| :------: | :------------------: | :--: | :------: | :------: |
| 查询体重 | /api/fitness/weight/ | GET  | limit=30 |    {}    |
|          |                      |      |          |          |
|          |                      |      |          |          |

