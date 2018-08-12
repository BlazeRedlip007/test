# 安装扩展

在composer.json的require部分，增加这个：

    "elasticsearch/elasticsearch": "~6.0"

然后运行

    composer update

代码库就装上去了。

# 代码里使用扩展

验证代码能正确引入：

    use Elasticsearch\ClientBuilder;

    $client = ClientBuilder::create()->build();
    var_dump($client);

能```var_dump()```出东西来，就表明类库引入正确。

# 参考文档：

更多请见原文：

[https://www.elastic.co/guide/en/elasticsearch/client/php-api/6.0/_quickstart.html](https://www.elastic.co/guide/en/elasticsearch/client/php-api/6.0/_quickstart.html)