# 在源码编译成功的基础上，增加GD的支持，然后重新编译

*这文章是对 PHP 添加 GD 支持的探索过程记录。*

> 这个增加 GD 库是在源码编译 PHP 通过并成功配置 fpm 服务的前提下进行的。PHP 版本 7.2.8，服务器是CentOS 7.2 ，64位。参考 [http://php.net/manual/zh/image.requirements.php](http://php.net/manual/zh/image.requirements.php)

PHP 写的网站，通常会带有验证码功能，这个功能需要使用到GD库。

GD 库不是一个工具，它只是由 C 语言开发出来的一个编程库。PHP 使用这个库是通过编译时指定参数，然后将 GD 库代码连同 PHP 一起编译为可执行文件，实现功能的扩展。因此想要增加 GD 库就需要有 GD 库的源代码。

另外，有些图片格式 GD 库本身没有直接支持，比如 jpeg 和 png 。这些格式的支持是通过 jpeg 库和 png 库等第三方库实现的。鉴于目前 jpeg 和 png 属于主流的图片格式，需要启用他们的功能，那也需要准备对应的源代码。

> PHP 的源码有包含一份内置的 GD 库，启用内置的 GD 库指定```--with-gd```即可，不需要再加路径。但是，无论是否外置启用 GD 库都需要指定参数```--with-webp-dir=<DIR>```和```--with-jpeg-dir=<DIR>```。由于使用了zlib，所以同时需要指定```--with-zlib[=DIR]```。

## 获取 GD 库源代码

根据 PHP 文档的指引，找到[https://libgd.github.io/](https://libgd.github.io/)。在写这段文字的时候，我找到的最新 GD 版本是```2.2.5```。在服务器上获取源码：

    wget https://github.com/libgd/libgd/releases/download/gd-2.2.5/libgd-2.2.5.tar.gz

解压缩后的文件列表是

    [root@VM_13_157_centos libgd]# ls
    aclocal.m4    CMakeLists.txt  CONTRIBUTORS  m4           README.md  VMS
    bootstrap.sh  config          COPYING       Makefile.am  src        windows
    CHANGELOG.md  configure       docs          Makefile.in  test
    cmake         configure.ac    examples      netware      tests
    [root@VM_13_157_centos libgd]#

## 获取 jpeg 和 png 库的源代码

根据 jpeg 指向的来源[http://www.ijg.org/](http://www.ijg.org/) ，获取 Linux 系统格式的源代码：

    wget http://www.ijg.org/files/jpegsrc.v9c.tar.gz

获取 png 库的源代码(参考[http://www.libpng.org/pub/png/libpng.html](http://www.libpng.org/pub/png/libpng.html)，这里用的是1.6.35)：

    wget https://download.sourceforge.net/libpng/libpng-1.6.35.tar.gz

## zlib库

由于 libpng用到了zlib库，所以还需要zlib库的代码：

    wget https://www.zlib.net/zlib-1.2.11.tar.gz

这份zlib的库是在这里找到的：[https://www.zlib.net/](https://www.zlib.net/)

## 获取 libwebp 库

这个库名称是根据提示，去找```./configure --help```的输出内容时找到的。同时由于国内无法访问[https://developers.google.com](https://developers.google.com)，因此我找到github，从这里克隆代码：(https://github.com/webmproject/libwebp/)[https://github.com/webmproject/libwebp/]。

服务器上通过git工具，可以克隆代码：

    git clone https://github.com/webmproject/libwebp.git

## freetype 2字体库

鉴于编程可能用到freetype字体，这里顺便增加freetype2库。

    https://download.savannah.gnu.org/releases/freetype/freetype-2.4.0.tar.gz

在这里找到的下载链接[https://www.freetype.org/download.html](https://www.freetype.org/download.html)

## 解压缩

    [root@VM_13_157_centos jpegpng]# tar -xf freetype-2.4.0.tar.gz
    [root@VM_13_157_centos jpegpng]# tar -xf jpegsrc.v9c.tar.gz
    [root@VM_13_157_centos jpegpng]# tar -xf libpng-1.6.35.tar.gz

libwebp是用git克隆下来的，不需要解压。

## 配置参数

GD 库目前的位置

    /root/gdLibrary/libgd

其它的库

    /root/gdLibrary/jpegpng/jpeg-9c
    /root/gdLibrary/jpegpng/libpng-1.6.35
    /root/gdLibrary/jpegpng/zlib-1.2.11
    /root/gdLibrary/jpegpng/libwebp
    /root/gdLibrary/jpegpng/freetype-2.4.0

按照目前的源代码分布，需要添加的参数是：

    --with-gd=/root/gdLibrary/libgd --with-jpeg-dir=/root/gdLibrary/jpegpng/jpeg-9c --with-png-dir=/root/gdLibrary/jpegpng/libpng-1.6.35 --with-webp-dir=/root/gdLibrary/jpegpng/libwebp --with-freetype-dir=/root/gdLibrary/jpegpng/freetype-2.4.0 --with-zlib-dir=/root/gdLibrary/jpegpng/zlib-1.2.11

以上就是需要添加的参数。

接着运行脚本，就遇到这个问题：

    checking for GD support... yes
    checking for the location of libwebp... /root/gdLibrary/jpegpng/libwebp
    checking for the location of libjpeg... /root/gdLibrary/jpegpng/jpeg-9c
    checking for the location of libpng... /root/gdLibrary/jpegpng/libpng-1.6.35
    checking for the location of libXpm... no
    checking for FreeType 2... /root/gdLibrary/jpegpng/freetype-2.4.0
    checking whether to enable JIS-mapped Japanese font support in GD... yes
    configure: error: webp/decode.h not found.
    [root@VM_13_157_centos php-7.2.8]#

仔细查找代码，发现（注意最后一次```ls```）：

    [root@VM_13_157_centos php-7.2.8]# ls /root/gdLibrary/jpegpng/libwebp/
    Android.mk      configure.ac       gradlew        Makefile.vc     src
    AUTHORS         COPYING            gradlew.bat    man             swig
    autogen.sh      doc                imageio        NEWS            webp_js
    build.gradle    examples           iosbuild.sh    PATENTS
    ChangeLog       extras             m4             README
    cmake           gradle             Makefile.am    README.mux
    CMakeLists.txt  gradle.properties  makefile.unix  README.webp_js
    [root@VM_13_157_centos php-7.2.8]# ls /root/gdLibrary/jpegpng/libwebp/src/
    dec    dsp  libwebpdecoder.pc.in  libwebp.pc.in  Makefile.am  utils
    demux  enc  libwebpdecoder.rc     libwebp.rc     mux          webp
    [root@VM_13_157_centos php-7.2.8]# ls /root/gdLibrary/jpegpng/libwebp/src/webp/
    decode.h  demux.h  encode.h  format_constants.h  mux.h  mux_types.h  types.h
    [root@VM_13_157_centos php-7.2.8]#

看来webp目录需要修改为：

    /root/gdLibrary/jpegpng/libwebp/src

于是

    --with-gd=/root/gdLibrary/libgd --with-jpeg-dir=/root/gdLibrary/jpegpng/jpeg-9c --with-png-dir=/root/gdLibrary/jpegpng/libpng-1.6.35 --with-webp-dir=/root/gdLibrary/jpegpng/libwebp/src --with-freetype-dir=/root/gdLibrary/jpegpng/freetype-2.4.0 --with-zlib-dir=/root/gdLibrary/jpegpng/zlib-1.2.11

继续试，依然不行。结果发现拷贝src/webp到/usr/local/include/webp就可以了，只是下一步提示找不到a|so文件。

看来编译过程是寻找系统中现有的动态链接库去编译的，所以需要在系统中安装webp！

## libwebp 的编译安装

是去webp里面，按照github的提示执行```make -f makefile.unix```。毕竟我代码都下载下来了，编译环境也有了啊。

但是webp有依赖关系，先后需要png、jpeg。在机械式地对jpeg和libpng执行

    ./configure
    make
    make install

之后，它居然还需要libtiff库。在我记录这篇文章的时候，访问不了libtiff官网给出的下载链接，所以只能这样：

    yum install -y libtiff.x86_64 libtiff-devel.x86_64

然后执行

    make -f makefile.unix

终于，libwebp编译成功。但是也只是编译成功，webp的链接库等文件并不会自动部署到/usr/local。仔细看官方文档，git版本需要运行autogen.sh。于是运行，居然还需要安装：

    yum install -y autoconf automake libtool

不然就autogen就用不了！运行完autogen后生成了configure文件。接着：

    ./configure
    make
    make install

## 安装 freetype

再次运行编译，发现freetype-conf无效，果然 freetype也是要编译安装的。通过查看 docs/UPGRADE.UNIX 文件，发现这个 freetype 简单地

    ./configure
    make
    make install

就可以了。

## libxpm

然后，问题继续出现。现在xpm没有，make阶段出错。继续装。

    yum install libXpm-devel -y

## 继续配置参数（你妈）

