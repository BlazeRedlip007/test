# 判断Elasticsearch有运行的方法（Linux）

    curl -XGET http://127.0.0.1:9200

输出应类似

    [root@localhost ~]# curl -XGET http://127.0.0.1:9200
    {
      "name" : "EnBPAov",
      "cluster_name" : "elasticsearch",
      "cluster_uuid" : "xUzHRihDQt2C5s8iu5SkfQ",
      "version" : {
        "number" : "6.3.1",
        "build_flavor" : "default",
        "build_type" : "rpm",
        "build_hash" : "eb782d0",
        "build_date" : "2018-06-29T21:59:26.107521Z",
        "build_snapshot" : false,
        "lucene_version" : "7.3.1",
        "minimum_wire_compatibility_version" : "5.6.0",
        "minimum_index_compatibility_version" : "5.0.0"
      },
      "tagline" : "You Know, for Search"
    }

# PHP类库引入测试

    <?php
    /**
     * Laravel 框架内测试 Elasticsearch 类库是否能正常引入
     *
     * @version 0.0.0
     */
    namespace App\Http\Controllers;

    use App\User;
    use App\Http\Controllers\Controller;
    use Illuminate\Http\Request;
    use Elasticsearch\ClientBuilder; // 引入类库

    class IndexController extends Controller
    {
        /**
         * 默认访问的方法
         *
         * @return string 返回一个空字符串
         */
        public function index()
        {
            echo '<pre>';
            $this->testPushDataMethod();
            $this->testGetDocument();
            echo '</pre>';
            return '';
        }

        /**
         * 测试类是否被加载
         *
         * @return void
         */
        private function testClassLoader()
        {
            $client = ClientBuilder::create()->build();
            var_dump($client);
        }

        /**
         * 测试索引写入
         *
         * @return void
         */
        private function testPushDataMethod()
        {
            $params = [
                'index' => 'test_index',
                'type' => 'test_type',
                'id' => 'test_id',
                'body' => ['testField' => rand()]
            ];
            $client = ClientBuilder::create()->setHosts(['http://127.0.0.1:9200'])->build();
            $response = $client->index($params);
            print_r($response);
        }

        /**
         * 测试获取数据
         *
         * @return void
         */
        private function testGetDocument()
        {
            $params = [
                'index' => 'test_index',
                'type' => 'test_type',
                'id' => 'test_id'
            ];
            $client = ClientBuilder::create()->setHosts(['http://127.0.0.1:9200'])->build();
            $response = $client->get($params);
            print_r($response);
        }
    }
