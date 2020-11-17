### 标题

​		这段话，主要是来介绍这个文章是用来干什么的。比如这个文件主要就是用来测试 blog 的。

### 序列

python 的主要类型分别是，字符串、列表、元组。

##### 序列类型操作符  

1. 成员关系操作符 (in, not in) 对象 [not] in 序列

> lzk_baggk：就是看序列里面有没有相等的。

2. 连接操作符
3. 重复操作符
4. 切片操作符

> lzk_baggk：需要注意的是，都是前闭开开区间。

##### extend 和 + 的区别

\+ 号是有返回值的，但是 extend() 函数是没有返回值。

```python
# 第一种
for i in [None] + range(-1, -len(s), -1):
  print s[:i]
  
# 第二种 这是错误的，因为 extend() 没有返回值
for i in [None].extend(range(-1,-len(s),-1))
```



##### 内建函数 BIF -> build_in function

+ len(iter) //长度
+ max(iter, key=None)  // key 的函数只能有一个传入值
+ reversed(seq)
+ sorted
+ sum()
+ zip()



#### 字符串

字符串是**不可变对象**，str()可以是一个工厂方法。

##### 切片 [start, end)

+ 正向索引
+ 反向索引
+ 默认索引

##### 字符串模版

```python
from string import Template
s = Template('There are $(howmany)')
s.subsititute(howmany=3)
```

##### 原始字符串操作符（r/R）

```python
s = r'hello\n'
```

> lzk_baggk：字符串不是通过 NUL 或者‘\0’来结束的。

#### 列表

##### 如何删除列表中的元素或者是列表

```python
a_list = [12, 'abc']
# 如果不知道索引
a_list.remove(12)
# 如果知道索引
del a_list[0]
```

> lzk_baggk：列表的实现是类似于可变数组来实现的。在计算操作的时候，在各个操作的时间复杂度上面也是一致的。

#### 元组

不可变，单元素元组需要一个括号加一个逗号。元组因为他不可变，所以他可以作为字典的关键字。

> lzk_baggk：lzk = (1,)

#### 浅拷贝和深拷贝

```python
test_1 = [1, [1,3,4]]
test_2 = [:]   # id(test_2) != test_1
test_2[1][0] = 10  # test_1[1][0] == 10
```

#### 其他

其他的常见数据结构中，类似的有队列和栈。栈的实现可以通过 list 来模拟。但是队列是不行，因为在pop(0)的代价太高了。

```python
# python 中的队列
from collections import deque

Q = deque()  # 
```



##### deque 类

 实现上是通过链表和数组来实现的。是一种双向队列。通过它能封装一个自己的 queue