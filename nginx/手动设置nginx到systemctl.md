# systemctl的服务管理机制

源码编译的nginx可执行文件默认保存在

    /usr/local/nginx/sbin/

可以用cd转至，用```./nginx```启动nginx作为后台运行的服务进程。但是出于强迫症的问题，如何将这个手动编译的软件设置为systemctl可以管理的系统服务呢？

## 实验A

由于我服务器上安装了Apache，所以```/usr/lib/systemd/system```目录下有个```httpd.service```文件。尝试修改这个文件里面的服务注释

    Description=The Apache HTTP Server

然后尝试用```systemctl stop httpd.service```会报这个警告：

    Warning: httpd.service changed on disk. Run 'systemctl daemon-reload' to reload units.

运行

    systemctl daemon-reload

之后重新用```systemctl```重启httpd，通过```systemctl status httpd.service```看到了修改后的内容。

因此可以肯定，**```/usr/lib/systemd/system```目录下保存着systemctl所管理的系统自启动服务进程的数据文件。**

## 实验B

在实验A的基础上，我拷贝```httpd.service```为```nginx.service```。然后做一些修改：

    [Unit]
    Description=The NGINX HTTP and reverse proxy server
    After=syslog.target network.target remote-fs.target nss-lookup.target

    [Service]
    Type=forking
    PIDFile=/usr/local/nginx/logs/nginx.pid
    ExecStartPre=/usr/local/nginx/sbin/nginx -t
    ExecStart=/usr/local/nginx/sbin/nginx
    ExecReload=/usr/local/nginx/sbin/nginx -s reload
    ExecStop=/bin/kill -s QUIT $MAINPID
    PrivateTmp=true

    [Install]
    WantedBy=multi-user.target

*由于我服务器已经有apache占用80端口，所以需要修改配置文件```/usr/local/nginx/conf/nginx.conf```，将端口改为其它数字，比如8080*

配置在此可以找到参考：[https://www.nginx.com/resources/wiki/start/topics/examples/systemd/](https://www.nginx.com/resources/wiki/start/topics/examples/systemd/)

然后

    systemctl daemon-reload
    systemctl start nginx.service
    ps -aux|grep nginx

可以看到nginx进程开始工作了。

    [root@VM_13_157_centos sbin]# ps -aux |grep nginx
    root      1682  0.0  0.0  18188   600 ?        Ss   16:33   0:00 nginx: master process /usr/local/nginx/sbin/nginx
    nobody    1684  0.0  0.1  20712  1620 ?        S    16:33   0:00 nginx: worker process
    root      1738  0.0  0.0 112704   976 pts/0    R+   16:39   0:00 grep --color=auto nginx
    [root@VM_13_157_centos sbin]#

# 结论

```systemctl```的开机自动启用的服务，配置文件在/usr/lib/systemd/system目录下。里面的文件一旦修改，需要用

    systemctl daemon-reload

重新加载。