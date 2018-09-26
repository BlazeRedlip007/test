#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# How to use tf.python_io.TFRecordWriter , this is a example

import tensorflow as tf

option = tf.python_io.TFRecordOptions(tf.python_io.TFRecordCompressionType.GZIP)
writer = tf.python_io.TFRecordWriter('test.TFRecord.gz', option)
# Or just use writer = tf.python_io.TFRecordWriter('test.TFRecord')
# if you do not need compression

for i in range(1000):
    example = tf.train.Example(features=tf.train.Features(feature={
      'data': tf.train.Feature(float_list=tf.train.FloatList(value=[1.222, 55.444, 55.444])),
      'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[1, 0, 1]))
    }))
    writer.write(example.SerializeToString())

writer.close()
