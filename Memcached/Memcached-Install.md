# 如何在服务器上通过编译安装Memcached服务

> 这是我在服务器上安装Memcached的探索性质的过程记录，不是为了写教程。

## 寻找Mencached的官方网站，获取源代码

我用Bing搜索的：[https://cn.bing.com](https://cn.bing.com)，不要问我为什么不用垃圾熊掌度。搜索出来第三个看上去是官网：
>memcached - a distributed memory object caching …

好吧，就是官网。在服务器上获取源码包：

    wget http://memcached.org/files/memcached-1.5.10.tar.gz

解压缩之后的文件：

    [root@localhost memcached-1.5.10]# ls
    aclocal.m4    crc32c.h           logger.h            slab_automove.c
    assoc.c       daemon.c           m4                  slab_automove_extstore.c
    assoc.h       depcomp            Makefile.am         slab_automove_extstore.h
    AUTHORS       doc                Makefile.in         slab_automove.h
    bipbuffer.c   extstore.c         memcached.c         slabs.c
    bipbuffer.h   extstore.h         memcached_dtrace.d  slabs.h
    cache.c       hash.c             memcached.h         solaris_priv.c
    cache.h       hash.h             memcached.spec      stats.c
    ChangeLog     INSTALL            missing             stats.h
    compile       install-sh         murmur3_hash.c      storage.c
    config.guess  items.c            murmur3_hash.h      storage.h
    config.h.in   items.h            NEWS                t
    config.sub    itoa_ljust.c       openbsd_priv.c      testapp.c
    configure     itoa_ljust.h       protocol_binary.h   thread.c
    configure.ac  jenkins_hash.c     README.md           timedrun.c
    COPYING       jenkins_hash.h     sasl_defs.c         trace.h
    crawler.c     LICENSE.bipbuffer  sasl_defs.h         util.c
    crawler.h     linux_priv.c       scripts             util.h
    crc32c.c      logger.c           sizes.c             version.m4
    [root@localhost memcached-1.5.10]#

## 编译安装

关于编译安装，官方有一个简短的介绍：

    wget http://memcached.org/latest
    tar -zxvf memcached-1.x.x.tar.gz
    cd memcached-1.x.x
    ./configure && make && make test && sudo make install

然后出现了两个神奇的提示：

    checking for libevent directory... configure: error: libevent is required.  You can get it from http://www.monkey.org/~provos/libevent/

          If it's already installed, specify its path using --with-libevent=/dir/

首先是需要```libevent```。去这里找了[http://www.monkey.org](http://www.monkey.org)，什么鬼网站？仔细看原来是这里[http://www.monkey.org/~provos/libevent/](http://www.monkey.org/~provos/libevent/)。跳转[http://libevent.org/](http://libevent.org/)。

    wget https://github.com/libevent/libevent/releases/download/release-2.1.8-stable/libevent-2.1.8-stable.tar.gz

编译安装：

    ./configure
    make
    make install

回去继续memcached：

    ./configure
    make
    make install

这次没错了。

## 启动服务

参考了帮助文件后，我觉得可以使用这个命令去启动它，作为服务：

    memcached --port=11211 --listen=127.0.0.1 --memory-limit=20MB --threads=2 --protocol=auto --conn-limit=1024 --pidfile=/run/memcached.pid --daemon --enable-shutdown --enable-coredumps

用root启动的话，需要加个```--user=root```，也就是```-u```

## CentOS .service文件

    [root@localhost system]# cat memcached.service
    [Unit]
    Description=memcached server
    After=syslog.target network.target remote-fs.target nss-lookup.target

    [Service]
    Type=forking
    ExecStart=/usr/local/bin/memcached --user=root --port=11211 --listen=127.0.0.1 --memory-limit=20MB --threads=2 --protocol=auto --conn-limit=1024 --pidfile=/run/memcached.pid --daemon --enable-shutdown --enable-coredumps
    ExecStop=/bin/kill -s QUIT $MAINPID
    PrivateTmp=true

    [Install]
    WantedBy=multi-user.target

    [root@localhost system]#


## 帮助文件

    # memcached --help
    memcached 1.5.10
    -p, --port=<num>          TCP port to listen on (default: 11211)
    -U, --udp-port=<num>      UDP port to listen on (default: 0, off)
    -s, --unix-socket=<file>  UNIX socket to listen on (disables network support)
    -A, --enable-shutdown     enable ascii "shutdown" command
    -a, --unix-mask=<mask>    access mask for UNIX socket, in octal (default: 0700)
    -l, --listen=<addr>       interface to listen on (default: INADDR_ANY)
    -d, --daemon              run as a daemon
    -r, --enable-coredumps    maximize core file limit
    -u, --user=<user>         assume identity of <username> (only when run as root)
    -m, --memory-limit=<num>  item memory in megabytes (default: 64 MB)
    -M, --disable-evictions   return error on memory exhausted instead of evicting
    -c, --conn-limit=<num>    max simultaneous connections (default: 1024)
    -k, --lock-memory         lock down all paged memory
    -v, --verbose             verbose (print errors/warnings while in event loop)
    -vv                       very verbose (also print client commands/responses)
    -vvv                      extremely verbose (internal state transitions)
    -h, --help                print this help and exit
    -i, --license             print memcached and libevent license
    -V, --version             print version and exit
    -P, --pidfile=<file>      save PID in <file>, only used with -d option
    -f, --slab-growth-factor=<num> chunk size growth factor (default: 1.25)
    -n, --slab-min-size=<bytes> min space used for key+value+flags (default: 48)
    -L, --enable-largepages  try to use large memory pages (if available)
    -D <char>     Use <char> as the delimiter between key prefixes and IDs.
                  This is used for per-prefix stats reporting. The default is
                  ":" (colon). If this option is specified, stats collection
                  is turned on automatically; if not, then it may be turned on
                  by sending the "stats detail on" command to the server.
    -t, --threads=<num>       number of threads to use (default: 4)
    -R, --max-reqs-per-event  maximum number of requests per event, limits the
                              requests processed per connection to prevent
                              starvation (default: 20)
    -C, --disable-cas         disable use of CAS
    -b, --listen-backlog=<num> set the backlog queue limit (default: 1024)
    -B, --protocol=<name>     protocol - one of ascii, binary, or auto (default)
    -I, --max-item-size=<num> adjusts max item size
                              (default: 1mb, min: 1k, max: 128m)
    -F, --disable-flush-all   disable flush_all command
    -X, --disable-dumping     disable stats cachedump and lru_crawler metadump
    -o, --extended            comma separated list of extended options
                              most options have a 'no_' prefix to disable
       - maxconns_fast:       immediately close new connections after limit
       - hashpower:           an integer multiplier for how large the hash
                              table should be. normally grows at runtime.
                              set based on "STAT hash_power_level"
       - tail_repair_time:    time in seconds for how long to wait before
                              forcefully killing LRU tail item.
                              disabled by default; very dangerous option.
       - hash_algorithm:      the hash table algorithm
                              default is murmur3 hash. options: jenkins, murmur3
       - lru_crawler:         enable LRU Crawler background thread
       - lru_crawler_sleep:   microseconds to sleep between items
                              default is 100.
       - lru_crawler_tocrawl: max items to crawl per slab per run
                              default is 0 (unlimited)
       - lru_maintainer:      enable new LRU system + background thread
       - hot_lru_pct:         pct of slab memory to reserve for hot lru.
                              (requires lru_maintainer)
       - warm_lru_pct:        pct of slab memory to reserve for warm lru.
                              (requires lru_maintainer)
       - hot_max_factor:      items idle > cold lru age * drop from hot lru.
       - warm_max_factor:     items idle > cold lru age * this drop from warm.
       - temporary_ttl:       TTL's below get separate LRU, can't be evicted.
                              (requires lru_maintainer)
       - idle_timeout:        timeout for idle connections
       - slab_chunk_max:      (EXPERIMENTAL) maximum slab size. use extreme care.
       - watcher_logbuf_size: size in kilobytes of per-watcher write buffer.
       - worker_logbuf_size:  size in kilobytes of per-worker-thread buffer
                              read by background thread, then written to watchers.
       - track_sizes:         enable dynamic reports for 'stats sizes' command.
       - no_inline_ascii_resp: save up to 24 bytes per item.
                               small perf hit in ASCII, no perf difference in
                               binary protocol. speeds up all sets.
       - no_hashexpand:       disables hash table expansion (dangerous)
       - modern:              enables options which will be default in future.
                 currently: nothing
       - no_modern:           uses defaults of previous major version (1.4.x)