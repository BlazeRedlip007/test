# 记录在疼讯云服务器上源码安装nginx的操作过程

## 安装过程实录

首先用wget从官方网站上下载稳定版的源代码。

    wget http://nginx.org/download/nginx-1.10.1.tar.gz

然后解压。

    tar -vxf nginx-1.10.1.tar.gz

按照官方网站给出的源码编译的操作指导，接下来需要按顺序执行：

    ./configure
    make
    sudo make install

由于我用root账号进行软件编译，所以这里的最后是不用加```sudo```的。

执行```./configure```：

    [root@VM_13_157_centos nginx-1.10.1]# ./configure
    checking for OS
     + Linux 3.10.0-693.el7.x86_64 x86_64
    checking for C compiler ... found
     + using GNU C compiler
     + gcc version: 4.8.5 20150623 (Red Hat 4.8.5-28) (GCC)
    checking for gcc -pipe switch ... found
    checking for -Wl,-E switch ... found
    checking for gcc builtin atomic operations ... found
    checking for C99 variadic macros ... found
    checking for gcc variadic macros ... found
    checking for gcc builtin 64 bit byteswap ... found
    checking for unistd.h ... found
    checking for inttypes.h ... found
    checking for limits.h ... found
    checking for sys/filio.h ... not found
    checking for sys/param.h ... found
    checking for sys/mount.h ... found
    checking for sys/statvfs.h ... found
    checking for crypt.h ... found
    checking for Linux specific features
    checking for epoll ... found
    checking for EPOLLRDHUP ... found
    checking for O_PATH ... found
    checking for sendfile() ... found
    checking for sendfile64() ... found
    checking for sys/prctl.h ... found
    checking for prctl(PR_SET_DUMPABLE) ... found
    checking for sched_setaffinity() ... found
    checking for crypt_r() ... found
    checking for sys/vfs.h ... found
    checking for nobody group ... found
    checking for poll() ... found
    checking for /dev/poll ... not found
    checking for kqueue ... not found
    checking for crypt() ... not found
    checking for crypt() in libcrypt ... found
    checking for F_READAHEAD ... not found
    checking for posix_fadvise() ... found
    checking for O_DIRECT ... found
    checking for F_NOCACHE ... not found
    checking for directio() ... not found
    checking for statfs() ... found
    checking for statvfs() ... found
    checking for dlopen() ... not found
    checking for dlopen() in libdl ... found
    checking for sched_yield() ... found
    checking for SO_SETFIB ... not found
    checking for SO_REUSEPORT ... found
    checking for SO_ACCEPTFILTER ... not found
    checking for IP_RECVDSTADDR ... not found
    checking for IP_PKTINFO ... found
    checking for IPV6_RECVPKTINFO ... found
    checking for TCP_DEFER_ACCEPT ... found
    checking for TCP_KEEPIDLE ... found
    checking for TCP_FASTOPEN ... found
    checking for TCP_INFO ... found
    checking for accept4() ... found
    checking for eventfd() ... found
    checking for int size ... 4 bytes
    checking for long size ... 8 bytes
    checking for long long size ... 8 bytes
    checking for void * size ... 8 bytes
    checking for uint32_t ... found
    checking for uint64_t ... found
    checking for sig_atomic_t ... found
    checking for sig_atomic_t size ... 4 bytes
    checking for socklen_t ... found
    checking for in_addr_t ... found
    checking for in_port_t ... found
    checking for rlim_t ... found
    checking for uintptr_t ... uintptr_t found
    checking for system byte ordering ... little endian
    checking for size_t size ... 8 bytes
    checking for off_t size ... 8 bytes
    checking for time_t size ... 8 bytes
    checking for setproctitle() ... not found
    checking for pread() ... found
    checking for pwrite() ... found
    checking for pwritev() ... found
    checking for sys_nerr ... found
    checking for localtime_r() ... found
    checking for posix_memalign() ... found
    checking for memalign() ... found
    checking for mmap(MAP_ANON|MAP_SHARED) ... found
    checking for mmap("/dev/zero", MAP_SHARED) ... found
    checking for System V shared memory ... found
    checking for POSIX semaphores ... not found
    checking for POSIX semaphores in libpthread ... found
    checking for struct msghdr.msg_control ... found
    checking for ioctl(FIONBIO) ... found
    checking for struct tm.tm_gmtoff ... found
    checking for struct dirent.d_namlen ... not found
    checking for struct dirent.d_type ... found
    checking for sysconf(_SC_NPROCESSORS_ONLN) ... found
    checking for openat(), fstatat() ... found
    checking for getaddrinfo() ... found
    checking for PCRE library ... not found
    checking for PCRE library in /usr/local/ ... not found
    checking for PCRE library in /usr/include/pcre/ ... not found
    checking for PCRE library in /usr/pkg/ ... not found
    checking for PCRE library in /opt/local/ ... not found

    ./configure: error: the HTTP rewrite module requires the PCRE library.
    You can either disable the module by using --without-http_rewrite_module
    option, or install the PCRE library into the system, or build the PCRE library
    statically from the source with nginx by using --with-pcre=<path> option.

按照最后错误的提示信息，可以通过指定PCRE的源代码目录来静态编译PCRE到Nginx内。这里采用这种方法解决错误。

> PCRE是一个Perl库，包括 perl 兼容的正则表达式库。

通过PCRE的官方网站[https://pcre.org/](https://pcre.org/)找到下载源码的位置[https://ftp.pcre.org/pub/pcre/](https://ftp.pcre.org/pub/pcre/)，获取源代码：

    wget https://ftp.pcre.org/pub/pcre/pcre2-10.31.tar.gz

解压代码：

    tar -xvf pcre2-10.31.tar.gz

在这里我解压后源代码的目录是

    /root/pcre/pcre2-10.31

回到nginx进行配置：

    ./configure --with-pcre=/root/pcre/pcre2-10.31

Linux下源码安装软件果然一波三折，这次给出的错误提示是：

    configure: error: libxml2 not found. Please check your libxml2 installation.

这个库是：

> Libxml2是个C语言的XML程式库，能简单方便的提供对XML文件的各种操作，并且支持XPATH查询，及部分的支持XSLT转换等功能。

这里就不去折腾源码了，我在yum里面看有没有，有就直接通过yum安装了：

    yum list|grep libxml2

发现有：

    [root@VM_13_157_centos php-7.2.8]# yum list|grep libxml2
    libxml2.x86_64                            2.9.1-6.el7_2.3              @anaconda
    libxml2-python.x86_64                     2.9.1-6.el7_2.3              @anaconda
    libxml2.i686                              2.9.1-6.el7_2.3              os
    libxml2-devel.i686                        2.9.1-6.el7_2.3              os
    libxml2-devel.x86_64                      2.9.1-6.el7_2.3              os
    libxml2-static.i686                       2.9.1-6.el7_2.3              os
    libxml2-static.x86_64                     2.9.1-6.el7_2.3              os
    mingw32-libxml2.noarch                    2.9.3-1.el7                  epel
    mingw32-libxml2-static.noarch             2.9.3-1.el7                  epel
    mingw64-libxml2.noarch                    2.9.3-1.el7                  epel
    mingw64-libxml2-static.noarch             2.9.3-1.el7                  epel
    [root@VM_13_157_centos php-7.2.8]#

于是直接就yum安装：

    yum install libxml2.x86_64

然而：

    Package libxml2-2.9.1-6.el7_2.3.x86_64 already installed and latest version
    Nothing to do

明明有为什么还报错？最后通过试验，解决办法是安装```libxml2-devel```

    yum install /y libxml2-devel.x86_64

安装后执行configure是没问题了，但是make又出问题。

    [root@VM_13_157_centos nginx-1.10.1]# make
    make -f objs/Makefile
    make[1]: Entering directory `/root/nginx/nginx-1.10.1'
    cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I /root/pcre/pcre2-10.31 -I objs \
            -o objs/src/core/nginx.o \
            src/core/nginx.c
    In file included from src/core/ngx_core.h:72:0,
                     from src/core/nginx.c:9:
    src/core/ngx_regex.h:15:18: fatal error: pcre.h: No such file or directory
     #include <pcre.h>
                      ^
    compilation terminated.
    make[1]: *** [objs/src/core/nginx.o] Error 1
    make[1]: Leaving directory `/root/nginx/nginx-1.10.1'
    make: *** [build] Error 2
    [root@VM_13_157_centos nginx-1.10.1]#

根据问题出现的信息```pcre.h: No such file or directory```，显然pcre没有被识别出来。根据博客园的一片文章显示，nginx使用的是旧版的pcre，用新版的pcre2去编译会报找不到这个头文件。

鉴于这份nginx是2016年的，可能nginx真的太旧了。于是重新下载一份新的：

    wget https://nginx.org/download/nginx-1.14.0.tar.gz

这个是版本号1.14.0的：

    [root@VM_13_157_centos nginx-1.14.0]# ls
    auto     CHANGES.ru  configure  html     man     src
    CHANGES  conf        contrib    LICENSE  README
    [root@VM_13_157_centos nginx-1.14.0]#

执行下面的命令：

    ./configure --with-pcre=/root/pcre/pcre2-10.31
    make

结果还是一样，在make的时候报相同的错误。最新稳定版还是这样，那就只能

    wget https://ftp.pcre.org/pub/pcre/pcre-8.42.tar.gz

然后解压```pcre-8.42.tar.gz```。再重新配置：

    [root@VM_13_157_centos nginx-1.14.0]# ./configure --with-pcre=/root/pcre/pcre-8.42

然而```make```的时候继续来问题：

    configure: error: Invalid C++ compiler or C++ compiler flags
    make[1]: *** [/root/pcre/pcre-8.42/Makefile] Error 1
    make[1]: Leaving directory `/root/nginx/nginx-1.14.0'
    make: *** [build] Error 2

没安装C++编译器。```yum install gcc-c++.x86_64```安装gcc-c++，继续编译。这次make就没错了。

最后执行

    make install

这个```make install```执行会很快就结束。最后在/usr/local/目录会找到nginx的可执行文件。至此编译安装结束。

## 总结

在CentOS7上源码安装nginx的正确步骤是

首先确定需要的一些工具和库存在

    yum install /y libxml2-devel.x86_64
    yum install /y gcc-c++.x86_64

需要下载的软件

    wget https://ftp.pcre.org/pub/pcre/pcre-8.42.tar.gz
    wget https://nginx.org/download/nginx-1.14.0.tar.gz

下载后解压。

配置和安装

    ./configure --with-pcre=pcre-8.42解压位置
    make
    make install

最后没错就是安装好了。