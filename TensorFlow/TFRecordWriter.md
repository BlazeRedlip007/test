# TensorFlow 数据处理

[TensorFlow接口文档](https://tensorflow.google.cn/api_docs/python/tf/python_io)

## ```tf.python_io.TFRecordWriter```的性质

此类用于将记录写入一个TFRecords类型的文件。它的初始化函数接受一个文件名和一个可选的配置项。
可选的配置项是一个```tf.python_io.TFRecordOptions```的实例。

当文件不存在时，执行下面的语句，将会创建一个0字节的文件。

    tf.python_io.TFRecordWriter('test.TFRecord')

对象的```write()```方法的解释是写入一个字符串到文件内。下面尝试写入一个字符串并关掉对象。

    obj = tf.python_io.TFRecordWriter('test.TFRecord')
    obj.write('123456789')
    obj.close()

执行发现程序出错。```obj.write()```似乎不能接受字符串。但是文档给出的解释是：

> Write a string record to the file.

这时靠文档的解释已经不能继续，所以我网上找到了这篇文章：
[数据读取之TFRecords](http://www.cnblogs.com/upright/p/6136265.html)。
文章利用了```tf.train.Example```对象的```SerializeToString()```方法的返回值作为```write()```
的输入值。

然而，官网文档中关于```tf.train.Example```类的解释是一片空白，线索又断了。不过我又找到这篇
文章：[TFRecord 的使用](https://blog.csdn.net/xueyingxue001/article/details/68943650)。
看到这篇文章使用```write()```方法与上一篇文章是一样的。于是整理出下面这段代码：

    example = tf.train.Example(features=tf.train.Features(feature={
      'data': tf.train.Feature(),
      'label': tf.train.Feature()
    }))
    writer.write(example.SerializeToString())

由于两篇文章说法一致，用法也是一致，所以据此可以反推出这个```write()```方法的使用。

1. ```tf.train.Example()```接收一个```tf.train.Features()```的返回值；
2. ```tf.train.Features()```接收一个字典，字典内嵌套```tf.train.Feature()```，没有s；
3. 调用```SerializeToString()```方法将```tf.train.Example```实例转换为```write()```
方法的输入。

我现在的目的是尝试往```test.TFRecord```文件内写入数据。于是我要知道```tf.train.Feature```
能接收怎样的参数。悲剧的是这部分的文档依旧一片空白。回去看我在第一篇文章里发现了这句话：
Feature里包含有一个 FloatList， 或者ByteList，或者Int64List。但是，FloatList、ByteList、
Int64List都是一片空白，官方几个意思？差评。

根据已有的文章只能得到下面的信息：

FloatList、ByteList、Int64List接受这样的参数：```value=[]```。

接着我整理了这分测试代码出来：

    #!/usr/bin/env python3
    # -*- coding: UTF-8 -*-

    import tensorflow as tf

    obj = tf.python_io.TFRecordWriter('test.TFRecord')

    example = tf.train.Example(features=tf.train.Features(feature={
      'data': tf.train.Feature(int64_list=tf.train.Int64List(value=[12])),
      'label': tf.train.Feature(float_list=tf.train.FloatList(value=[1.222]))
    }))

    obj.write(example.SerializeToString())
    obj.close()

注意，```features=```,```feature=```和```value=```不能省略。以及下面这三个可能的选项
也不能省：

- int64_list=
- float_list=
- bytes_list=

为了节省空间可以开启压缩：

    option = tf.python_io.TFRecordOptions(tf.python_io.TFRecordCompressionType.GZIP)
    obj = tf.python_io.TFRecordWriter('test.TFRecord.gz', option)

这样压缩出来是一个gz文件，可以用压缩软件解压。
