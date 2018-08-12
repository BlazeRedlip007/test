# 在源码编译成功的基础上，增加OpenSSL的支持，然后重新编译

Laravel 框架要求 OpenSSL PHP Extension 。从```phpinfo()```打印的结果来看，不在编译的时候指定一些参数，编译出来的 PHP 是不支持 OpenSSL 的。