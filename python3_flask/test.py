a = """
## UNIX环境高级编程

用来记录自己学习UNIX认为的重点，以及感悟。

<!--more-->

# 第3章 文件IO

#### 幻数  magic number

​	第一次听到这个概念，感觉是类似于协议这样的东西。一些约定俗成的东西。比如文件描述符的0，1，2在UNIX家族的操作系统的中，就是代表标准输入、标准输入、标准错误。可读性更强应该是：`STDIN_FILENO、STDOUT_FILENO、STDREE_FILENO。`

#### 函数open和openat

​	都返回最小的未使用的描述符数值，一般与文件描述符有关函数都是这样，比如socket。不过可以通过due与due2来改变，这个常用来实现输入输出的重定义。

````c
#include <fcntl.h>
int open(const char *path,int oflag,...);
int openat(int fd,const char *path,int oflag,..);
````

lzk_baggk

> ​		open和openat主要的区别是openat的path是相对地址，而open是绝对地址。fg参数指出了相对路径名的开始地址。
>
> ​		openat主要解决的问题是让线程可以使用相对路径名来打开目录中的文件，而不是只能打开当前工作目录。还有就是解决time-of-check-to-time-of-use（TOCTTOU）。

#### 函数lseek

​		文件的读、写操作都是从当前文件偏移处开始的，在系统默认的情况下，除非是设置O_APPEND，否则就是被设置为0。lseek仅将偏移量记录到内核，并不引起任何的IO操作。

```c
#include<unistd.h>
off_t lseek(int fd, off_t offset,int whence);

若whence是SEEK_SET，就是从开始处开始。
若whence是SEEK_CUR，就是从当前开始，可正可负
若whence是SEEK_END，就是偏移量设置为文件长度加offset,可正可负。
```

##### 文件空洞

​		偏移量可以大于长度，当偏移量大于文件的长度的时候。下一次写时，会加长文件，没有被写的部分就会形成文件空洞。

​		文件空洞不会占用磁盘的空间。只是在读取的时候被读作0。

#### 函数read，write

````c
#include<unistd.h>
ssize_t read(int fd ,void *buf,size_t nbytes);
````

+ 普通文件，如果只有30字节，而要求是100字节，则read返回30，下一次读取是0.
+ 终端设备，通常一次是一行。

```c
#include<unistd.h>
ssize_t write(int fd ,void *buf,size_t nbytes);
```

​		如果在打开文件，指定了`O_APPEND`选项，则在每次写操作之前，将文件偏移量设置在文件的当前的结尾处。在一次成功之后，该文件偏移量增加实际写的字节数。而且是操作是原子性的。

size_t 反映内存中对象的大小（以字节为单位）

> size_t的真实类型与操作系统有关，在32位架构中被普遍定义为：
>
> typedef   unsigned int size_t;
>
> 而在64位架构中被定义为：
>
> typedef  unsigned long size_t;

ssize_t 供返回字节计数或错误提示的函数使用。

> ssize_t是有符号整型，在32位机器上等同与int，在64位机器上等同与long int，有没有注意到，它和long数据类型有啥区别？其实就是一样的。size_t 就是无符号型的ssize_t，也就是unsigned long/ unsigned int (在32位下），不同的编译器或系统可能会有区别，主要是因为在32位机器上int和long是一样的。
>
>   typedef  long  ssize_t;//ssize_t就是long类型

lzk_baggk

> 可以理解size_t是ssize_t的无符号版本吧。因为read有可能需要放回负数，所以使用了ssize_t;

#### 文件共享

​		UNIX支持共享文件，在这个之前需要了解I/O的数据结构。总的来说，使用三种数据结构表示打开文件。

##### 有关数据结构

+ 每个进程在进程表（PCB？）中都有一个记录项，这个记录项包含一张打开的文件描述符表，指向一个文件表项。
+ 内核内所有打开的文件维持一张文件表。记录了偏移量，和v-node的地址。
+ 每个打开文件有个v-node。

lzk_baggk

> ​		按照我的理解来说，当一个进程申请打开一个文件的时候，操作系统会在打开之后，记录到文件表中，里面记录v-node的信息，给文件是以什么样的方式打开的。之后，记录在对应进程的进程表里面。和文件描述符映射。
>
> ​		当我们需要read的时候，我们通过文件描述符，就可以找到操心系统的文件表中对应的一项，通过这个我们可以得到i-node。有了i-node，我就可以得到知道具体在那一块了。

#### 函数dup和dup2

​		都可以用来复制一个现有的文件描述符。

````c
#include<unistd.h>
int dup(int fd);
int dup2(int fd,int fd2);
````

​		若成功，则放回新的文件描述符，如果错误，放回-1。在dup放回的文件描述符一定是最小的可用文件描述符。dup2则是可以指定，如果fd2存在，则先关闭。

lzk_baggk

> 返回新的文件描述符，**使得多个文件描述符指向同一个文件表**。因为0，1，2默认是输入、输出、错误所以可以用来实现重定向。

````c
int file = open('../../',O_APPEND);
//将file定义为标准输出
int error = dup2(file,STDOUT_NO);
````



#### 函数sync，fsync，fdatasync

​		顾名思义，就是同步、文件同步、文件数据同步的意思。简单来说，因为磁盘的效率比内存低了很多，所以在操作系统层次，为了优化会延迟磁盘的写入，这样可以将多个写操作合为一个写操作。但是有时候，我们需要保证数据的同步。

````c
#include <unistd.h>
int 	fsync(int fd);
int		fdatasync(int fd);
void 	sync(void);
````

+ sync函数将所有修改过的块缓存区排入写操作，然后放回。不等待实际写操作结束。
+ fsync函数等待文件描述符fd描述的起作用。更新数据部分和文件属性。
+ fdatasync函数只会更新数据。

#### 函数fcntl

​		可以改变**已经打开文件**的属性

````c
#include <fcntl.h>
int fcntl(int fd,int cmd,../int arg/);
````

+ 复制一个已有的描述符(cmd = F_DUPFD或者F_DUPFD_CLOEXEC)。
+ 获取/设置文件描述符标志(cmd = F_GETFD或 F_SETFD)。
+ 获取/设置文件状态标志(cmd = F_GETFL或 F_SETFL)。
+ 获取/设置异步I/O所有权（cmd = F_GETOWN 或 F_SETOWN)。
+ 获取/设置记录锁(cmd = F_GETLK 、F_SETLK 、F_SETLKW)。

lzk_baggk

> 我们在使用fork的时候，后面很可能会接exec函数。这个时候，文件描述符会保留下来，但是其他的正文、数据、堆和栈会保留下来。我们就没有办法关掉没用的文件描述符。我们需要设置FD_CLOEXEC。
>
> 记录锁，详细看第14章

```c
int 	fd = open("foo.txt",O_RDONLY);
int 	flags = fcntl(fd,F_GETFD);
flags |= FD_CLOEXEC;
tcntl(fd,F_SETFD,flags);
```

#### 函数ioctl

````C
#include <unistd.h>
#include <sys/ioctl.h>
int 	ioctl(int fd,int request,s...);
````

# 第4章 文件和目录

# 第5章 标准I/O库

​		与文件I/O围绕文件描述符不同，标准I/O是围绕流的。

```c
#include<stdio.h>
#include<wchar.h>
int fwide(FILE *fd , int mode);
//返回值：若流是宽定向，返回正值。若流是字节定向则是负值；若为定向，则0
```

lzk_baggk

> fwide并不改变已定向的流。特意说明一下标准输入流，标准输出流，标准错误流。stdin\stdout\stderr。与STDIN_FILENO、STDOUT_FILENO、STDERR_FILENO。从概念上有些不同。

#### 缓冲

​		缓冲的目的是为了减少read、write的调用次数。标准I/O有三种类型

+ 全缓冲
+ 行缓冲
+ 不带缓冲

> 一般stderr不带缓冲。指向终端设备的是行缓存。可以通过flush来冲洗缓冲区。对于标准I/O，flush意味着写在硬盘上。在终端设备上，则是丢弃。

```c
#include<stdio.h>
void setbuf(FILE * restrict fp, char *restrict buf);
void setvbuf(FILE * restrict fp, char *restrict buf,int mode ,size_t size);
//返回值：若成功，返回0；若出错，返回非0
```

mode参数：_IOFBF | _IOLBF | _IONBF

```c
#include<stdio.h>
int fflush(FILE * fp);
```

讲该流所有未写的数据都送入内核。作为一种特殊情况，若fp==NULL，则全部输出流被冲洗。

#### 读与写流

+ 一次读写一个字符

```c
#include<stdio.h>
int getc(FILE * fp);
int fgetc(FILE *fg);
int getchar(void);

int putc(int c,FILE *fp);
int fputc(int c,FILE *fp);
int putchar(int c);
```

函数getchar()等同于getc(stdin)。

+ 每次一行I/O

```c
#include<stdio.h>
char * fgets(char *restrict buf,int n,FILE *restrict fp);
char * gets(char *buf); //不推荐使用的函数

int fputs(const char *restrict str,FILE * restrict fp);
int puts(const char *str);
```

+ 结构I/O

```c
#include<stdio.h>
size_t fread(void *restrict ptr,size_t size,size_t nojb,FILE * restrict fp);
size_t fwrite(const void * restrict ptr,size_t size ,size_t nobj,FILE *restrict fp);
```



# 第8章 进程控制

​		系统有一些专用进程，比如0（swapper）进程与1(init)进程。init进程是所有孤儿进程的父进程，在自举阶段由内核调用。

```C
#include<unistd.h>
pid_t getpid(void);
pid_t getppid(void);
uid_t getuid(void);
uid_t geteuid(void);
gid_t getgid(void);
git_t getegid(void)
```

#### 函数fork

```c
#include<unistd.h>
pid_t fork(void);
```

​		这个函数会有两个返回值，父进程会返回子进程的ID，子进程会返回0。通过这种方式来区别两个子进程还是父进程。fork会复制父进程的数据空间、堆和栈，不过现在都使用了copy-on-write技术了，内核把他们的访问权限设置为只读。如果试图修改，内核会把修改的部分制作成一个副本。

> linux提供了另外一种新进程的创建方法--clone();是一种fork的推广形式。

#### 函数vfork

​		vfork在使用上，和fork一致，但是会保证子进程先调用，只有当子进程使用exec()，或者是exit()的时候，父进程才会开始。他在复制父进程的时候，不会完全复制，只会复制一部分。

lzk_baggk

> 这个函数，现在应该不用了吧。因为就效率来说，肯定是没有cow高的，不复制比部分复制的效率高一些。并且存在移植的问题。

#### 函数exit

​		通常来说，exit是函数，而_exit是系统调用。\_exit不执行标准I/O缓冲区的冲洗操作。而exit由实现而定。但是现在的exit可能具体去实现了，因为在exit的时候，会关闭所有的文件描述符。感觉没有任何的好处。

> exit函数由IOS C定义，其操作包括调用各终端处理程序。（终止处理程序在调用atexti函数时登记），然后关闭所有标准I/O流等。

#### init进程收养

​		大致过程是，当一个进程终止时，内核逐个检查所有活动进程，来判断是不是他的子进程，如果是把他的父进程修改为init。这样可以保证每个进程都有一个父进程。

#### 僵死进程

​		如果子进程比父进程更早的结束，内核会为父进程保存一小部分信息（至少包括进程ID、终止状态以及CPU使用总量），所以当父进程使用wait或者是waitpid时，可以得到这些信息。状态为Z。在init进程中，只要有一个子进程终止，init就会调用一个wait。

#### wait与waitpid

​		当一个进程正常或异常终止时，内核就向其父进程发送SIGCHLD信号。系统的默认操作是无视他。

+ 如果子进程都在运行，阻塞
+ 如果存在子进程终止，正等待父进程获取，返回终止状态
+ 没有子进程，出错

```c
#include<sys/wait.h>
pid_t wait(int *statloc);
pid_t waitpid(pid_t pid,int *statloc,int option);
```

区别

+ 在一个子进程终止前，wait是一定使调用者阻塞，而waitpid可以不阻塞
+ waitpid并不等待第一个终止的进程，他有多个选项

lzk_baggk

> statloc是这个整型指针，用特定的位来表示特定的状态

| 宏           | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| WIFEXITED    | 若正常终止放回的状态，则为真。可以执行WEXITSTATUS来获取exit时的低8位 |
| WIFSIGNALED  | 若为异常终止子进程返回的状态，则为真                         |
| WIFSTOPPED   | 若为当前暂停子进程的返回的状态。WSTOPSIG使子进程暂停的信号编号 |
| WIFCONTINUED | 若在作业控制暂停后已经继续的子进程返回了状态                 |

关于waitpid函数中的pid

+ pid == -1 等待任一子进程，等效于wait
+ pid  > 0   等待进程ID与pid相等的子进程
+ pid == 0  等待组ID等于调用进程组ID的任一子进程
+ pid < -1   等待组ID等于pid绝对值的任一子进程

option参数是0或者是WCONTINUED | WNOHANG | WUNTRACT中的一个

lzk_baggk

> 如果不关心子进程的返回值，则可以fork两次，让子进程成为孤儿进程，回收工作交给init进程。

#### 函数waitid

```c
#include<sys/wait.h>
int 	waitid(idtype_t	idtype,id_t id,siginfo_t *infop,int option);
```

#### 函数wait3与wait4

​		比起wait、waitid与waitpid，允许内核返回终止进程及其所有子进程使用的资源情况。

```c
#include<sys/types.h>
#include<sys/wait.h>
#include<sys/time.h>
#include<sys/resource.h>
pid_t  wait3(int *statloc,int option, struct rusage *rusage);
pid_t  wait4(pid_t pid,int * statloc,int option,struct rusage *rusage);
```

#### 函数exec

```c
#include<unistd.h>
int execl(const char *pathname,const char *arg0,.../* char *0 */);
int execv(const char *pathname,char * argv[]);
int execle(const char *pathname,const char *arg0,.../* (char *)0,char *const envp[]*/);
int execve(const char *pathname,char * argv[],char *const envp[]);
int execlp(const char *filename,const char *arg0,.../* (char *)0*/)
int execvp(const char *filename,char *const argv[]);
int fexecve(int fd,char *const argv[],char *const envp[]);
```

lzk_baggk

> l是list的意思，v是vector，e是environment，p是PATH，f是file_id。在很多UNIX实现里面，只有execve是系统调用。

#### 更改用户ID与更改组ID

​		首先说明有效用户与实际用户。

lzk_baggk

> 就我个人理解，实际用户就是打开这个进程用户。有效用户一般等于实际用户，我觉得是指拥有着。

# 第14章高级I/O

### 记录锁

​		当第一个进程正在读或者修改文件的时候，使用记录锁可以阻止其他进程修改同一文件区。更准确的名字叫字节范围锁（bity-range locking）。早期只支持函数flock，对整个文件加锁。慢慢的可以通过函数fcntl来实现对部分加锁，函数lockf是fcntl这个功能的接口封装。

````c
struct flock{
  short l_type;		/*F_RDLCK,F_WRLCK,or F_UNICK*/
  short l_whence;   // SEEK_SET,SEEK_CUR ,or SEEK_END
  off_t l_start;;
  off_t l_len;
  pid_t l_pid;
};
//这个结构体和上面说明整个文件加锁的函数flock同名
````

### 读锁，写锁

​		F_RDLCK读锁，F_WRLCK是写锁。加读锁的文件必须是读打开，加写锁的文件必须是写打开。如果一个文件加了读锁，其他进程可以加读锁，但是不能加写锁。加了写锁之后，读锁与写锁都不能加了。

##### fcntl实现记录锁

```C
#include<fcntl.h>
int fcntl(int fd,int cmd,...);
```

​		对于记录锁，cmd是F_GETLK、F_SETLK或F_SETLKW。第三个参数是struct flock * flockptr。

> F_GETLK判断flockptr所表述的锁是否会被另外一把锁排斥。如果存在，他阻止创建。
>
> F_SETLK设置描述的锁。如果被系统阻止，立即阻止。
>
> F_SETLKW设置描述的锁。如果被系统阻止，被进程休眠，一直到允许。

lzk_baggk

> 一般来说，会用F_GETLK来测试，然后用F_SETLK来设置。但是这两者并不是一个原子操作。所以存在这样的情况，在F_GETLK之后，是没有写锁的，这个时候切换到另外一个进程，之后加了写锁。导致出错。所以处理F_SETLK出错是必须的。

​		在设置或释放文件上的一把锁时，系统按要求组合或者是分裂相邻区。

##### 锁的隐含继承和释放

+ 锁与进程和文件两者相关联 
  + 当进程终止时，建立的锁释放掉
  + 描述符关闭时，通过该进程的锁会释放掉
+ fork产生的子进程不继承父进程的锁

![](../images/recodelock.png)

lzk_baggk

> 如上面所说，文件的打开需要三张表。在v-node里面有一个指向lockf的链表，每个节点有创建他的进程ID，通过这种方式来实现上面的需求。因为v-node对于每个打开的文件是唯一的。

##### 建议锁与强制性锁

[来自：让自己行动起来](https://www.cnblogs.com/web-java/p/5539292.html)

> - 建议锁又称协同锁。对于这种类型的锁，内核只是提供加减锁以及检测是否加锁的操作，但是不提供锁的控制与协调工作。也就是说，如果应用程序对某个文件进行操作时，没有检测是否加锁或者无视加锁而直接向文件写入数据，内核是不会加以阻拦控制的。因此，建议锁，不能阻止进程对文件的操作，而只能依赖于大家自觉的去检测是否加锁然后约束自己的行为；多数 Unix 和类 Unix 操 作系统使用建议型锁,有些也使用强制型锁或兼而有之。 
> - 强制锁，是OS内核的文件锁。每个对文件操作时，例如执行open、read、write等操作时，OS内部检测该文件是否被加了强制锁，如果加锁导致这些文件操作失败。也就是内核强制应用程序来遵守游戏规则；微软的操作系统往往使用的是强制型锁。

###  多路IO复用转换

​	select，poll，epoll，pselect工作在内核层面上。

##### 函数select、pselect

lzk_baggk

> ​		在默认情况下，我们的操作文件的方式阻塞的。可以更改，通过fcntl（改变的是文件状态标志）。如果是阻塞的，那我们一次性最大只能监听一个文件，如果是非阻塞的我们需要不断的轮询，浪费CPU的性能。当然也可以使用多线程与多进程来实现，但是这样会造成程序更复杂。同时如果线程或者是进程一多，每个线程获得的时间片就会变少。从而服务器效率下降的非常快。
>
> ​		多路IO复用逻辑上server与client中间的一层，这一层就是多路IO复用，select实际上是在操作系统的内核。在服务器端接受到数据的时候，内核就可以判断是给那个描述符的。从而唤醒select（文件描述符就绪），select去通知server去read数据，这个时候，server的read就一定不会阻塞了。从而解决了两难的问题。
>
> ​		**可以这样理解，就是一个单线程模型的服务器，监听的工作交给了内核。**

select能监听的文件描述符个数受限与FD_SETSIZE，一般是1024（32\*32）个，如果是64位系统则是2048（32\*64）。

原型

```c
int select(int maxfdp1,
           fd_set	 	  * restrict readfds,
           fd_set 	 	  * restrict writefds,
           fd_set 		  * restrict exceptfds,
           struct timeval * restrict tvptr);
//返回-1表示出错，>=0 表示准备好的个数。0是超时了放回
```

> restrict，C语言中的一种类型限定符，用于告诉编译器，对象已经被指针所引用，不能通过除该指针外所有其他直接或间接的方式修改该对象的内容。

第一个参数是最大文件描述符+1，告诉内核扫描的范围。  

二三四个参数是传入传出参数。传入是告诉内核，那些文件描述符需要监听。传出是告诉服务器那些文件描述符可以被处理。可以理解是一个字节数据。

```c++
#include <sys/select.h>
int FD_ISSET(int fd,fd_set *fdset);
int FD_SET(int fd,fd_set *fdset);
int FD_CLR(int fd,fd_set *fdset);
int FD_ZERO(fd_set *fdset);

example
fd_set		readset,writeset;
FD_ZERO(&readset);
FD_ZERO(&writeset);
FD(0,&readset);
select(4,$readset,$writeset,NULL,NULL);
```

最后一个参数，是等待时间。

+ NULL，永远等下去
+ 设置timeval，等待固定时间
+ 设置timeval为0，检查后，马上放回，轮询。

```c
struct timeval{
		long 		tv_sec;			/*seconds*/
    	long 		tc_usec;		/*microseconds*/
};
```

> 在POSIX.1中允许修改最后一个参数。所以不能确保它没有被更新。Linux就将用剩余时间更新该结构。

​		pselect是select的变体，POSIX.1定义的。

````c
#include<sys/select.h>
int pselect(int maxfdp1,
           fd_set	 			  * restrict readfds,
           fd_set 	 			  * restrict writefds,
           fd_set 				  * restrict exceptfds,
           const struct timespec  * restrict tvptr
           const sigset_t 		  * restrict sigmask);
````

​		除了下列几点外，pselect与select相同

+ select的超时值使用timeval结果指定，但pselect使用timespec结构，精度更好一点。
+ timespec是const，不可以被函数修改。
+ 可以选择信号屏蔽字。如果为NULL，那么与在信号方面一致。

```c++
struct timespec{
    	time_t		tv_sec;		/*seconds*/
    	long 		tv_nsec;	/*nanosecond*/
};
//time_t其实也是long
//s（秒）、ms（毫秒）、μs（微秒）、ns（纳秒），
//其中：1s=1000ms，1 ms=1000μs，1μs=1000ns
```

##### 函数 poll

​		poll函数类似于select，但是接口有所不同。支持人任何类型的文件描述符。

```c++
#include<poll.h>
int poll(struct follfd fdarray[],nfds_t nfds, int timeout);

struct pollfd{
    int 	fd;			//file descriptor to check,or < 0 to ignore;
    short 	events;		//events of interest on fd
    short	revents;	//events that occurrend on fd
};
```

​		poll构造一个pollfd结构的数组，每个数组元素指定一个描述符编号以及我们都感兴趣的编号。

##### 函数 epoll



"""

a = a.splitlines()

print(type(a))