首先，停止Apache：

    systemctl stop httpd.service

然后移除旧的PHP：

    yum remove php.x86_64 php-cli.x86_64 php-common.x86_64 php-gd.x86_64 php-mbstring.x86_64 php-mysql.x86_64 php-pdo.x86_64 php-pear.noarch php-pecl-igbinary.x86_64 php-pecl-redis.x86_64 php-process.x86_64 php-xml.x86_64

在这个移除的过程中，脚本会自行修改apache的配置文件，所以我最多就是备份一下httpd下与php相关的文件。

接着，编译PHP7.2。这个过程这里就不详细说了。

我打算将Apache换成Nginx，所以下面说Nginx。Nginx需要修改一个地方就行了：

    fastcgi_param  SCRIPT_FILENAME  /documentroot$fastcgi_script_name;

```/documentroot```是web目录。上面那一行以及它所在的一个配置块的意思是说，当Nginx遇到请求```.php```文件的时候，将请求的内容通过9000端口，发送给另外一个监听进程，然后将进程反馈内容返回给客户端。