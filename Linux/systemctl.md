# systemctl的服务定义配置文件

```systemctl```命令是新的CentOS系统引入用来管理系统服务的。

## 系统开机就可以运行的服务

系统开机就能运行的服务（无需用户登录）定义在

    /usr/lib/systemd/system/

目录下，保存为扩展名```service```。修改了这里的文件，则需要用

    systemctl daemon-reload

使修改后的配置重新加载到```systemctl```。

```service```文件内一般有几个块，用中括号区分。它们分别是Unit、Service和Install。比如下面这份就是配置文件：

    [Unit]
    Description=The Apache HTTP Server
    After=network.target remote-fs.target nss-lookup.target
    Documentation=man:httpd(8)
    Documentation=man:apachectl(8)

    [Service]
    Type=notify
    EnvironmentFile=/etc/sysconfig/httpd
    ExecStart=/usr/sbin/httpd $OPTIONS -DFOREGROUND
    ExecReload=/usr/sbin/httpd $OPTIONS -k graceful
    ExecStop=/bin/kill -WINCH ${MAINPID}
    # We want systemd to give httpd some time to finish gracefully, but still want
    # it to kill httpd after TimeoutStopSec if something went wrong during the
    # graceful stop. Normally, Systemd sends SIGTERM signal right after the
    # ExecStop, which would kill httpd. We are sending useless SIGCONT here to give
    # httpd time to finish.
    KillSignal=SIGCONT
    PrivateTmp=true

    [Install]
    WantedBy=multi-user.target

## 各个参数的含义

### Unit

- Description 这个是注释，说明这个是什么服务。在启动服务的时候，会显示这个信息。
- After 指明此需要依赖的服务。After意思是在什么东西之后。
- Documentation 指明如何使用这个服务的帮助文档。

### Service

