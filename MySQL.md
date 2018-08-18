# 给数据库表某一字段增加索引的正确姿势：

    ALTER TABLE n_article ADD INDEX HASH(`url`);
    ALTER TABLE n_article ADD INDEX BTREE(`url`);

# mysqldump 使用帮助

    mysqldump --help

# 导出数据库中的某些表，而不是全部表都导出：

    mysqldump --user=用户名 --password=密码 --port=3306 --result-file=文件名.sql --tz-utc 数据库名称 表1 表2 表3

```--tz-utc``` 用于统一 timestamp 字段的计时。

# MySQL 导入数据库备份的方法：

    mysql --user=用户名 --password=密码 --database=数据库名 < 备份文件

# 查看有哪些用户

    use mysql;
    select user,host from user;

# 如何创建用户

MySQL 有两种方法可以创建用户。

1. ```CREATE USER``` 或 ```GRANT```
2. INSERT, UPDATE, DELETE

    CREATE USER 'remoteyong'@'%' IDENTIFIED BY 'xqg8787785552cccsiau2890';
    GRANT ALL PRIVILEGES ON *.* TO 'finley'@'%' WITH GRANT OPTION;
