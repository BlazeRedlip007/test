# Linux 的 Shell 脚本编写

最基本的 Linux Shell 脚本，就是将命令写到一个以 ```.sh``` 结尾的文本文件内，然后用

    chmod +x 文件名

赋予可执行权限。当然，用```chmod -x 文件名```可以去除授予的可执行权限。

# linux在shell中执行命令并将结果赋值给变量

    #!/bin/bash
    envlocation=`pwd`
    echo $envlocation
    unset envlocation