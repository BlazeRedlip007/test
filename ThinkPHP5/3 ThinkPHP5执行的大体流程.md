controller类的实例化操作，在App类（thinkphp\library\think\App.php）的exec方法内通过```Loder::action()```进行。

按照流程，文件包含的顺序大致是：index.php、start.php、base.php、Loder.php、App.php、控制器和其它定义的文件。