#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# This is a example to answer:
# How to use TFRecord to train a model?
# Note: the code still have some problem.

import tensorflow as tf

def createTFRecordFile():
    option = tf.python_io.TFRecordOptions(tf.python_io.TFRecordCompressionType.GZIP)
    writer = tf.python_io.TFRecordWriter('example.TFRecord.gz', option)

    def createExample(data, label):
        example = tf.train.Example(features=tf.train.Features(feature={
          'x': tf.train.Feature(float_list=tf.train.FloatList(value=data)),
          'y': tf.train.Feature(float_list=tf.train.FloatList(value=label))
        }))
        return example

    for i in range(1000):
        example = createExample([0, 0], [0])
        writer.write(example.SerializeToString())
        example = createExample([0, 1], [1])
        writer.write(example.SerializeToString())
        example = createExample([1, 0], [1])
        writer.write(example.SerializeToString())
        example = createExample([1, 1], [0])
        writer.write(example.SerializeToString())
    writer.close()

def createModel():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(2, tf.keras.activations.tanh, 1, input_shape = (1, 2)),
        tf.keras.layers.Dense(1, tf.keras.activations.sigmoid, 1)
    ])
    model.compile(optimizer = 'Adam', loss = 'MSE', metrics = ['accuracy'])
    return model

# create file 'example.TFRecord.gz'
createTFRecordFile()

# tf.data.TFRecordDataset
# A Dataset comprising records from one or more TFRecord files.
# __init__(
#    filenames,
#    compression_type=None,
#    buffer_size=None,
#    num_parallel_reads=None
# )

# A tf.string tensor or tf.data.Dataset containing one or more filenames.
filenames = tf.constant(['example.TFRecord.gz'])

# (Optional.) A tf.string scalar evaluating to one of "" (no compression),
# "ZLIB", or "GZIP"
compression_type = tf.constant('GZIP')

# (Optional.) A tf.int64 scalar representing the number of bytes in the read
# buffer. 0 means no buffering.
buffer_size = tf.constant(100, dtype = tf.int64)

# (Optional.) A tf.int64 scalar representing the number of files to read in
# parallel. Defaults to reading files sequentially.
num_parallel_reads = tf.constant(2)

# data is a TFRecordDataset object
data = tf.data.TFRecordDataset(filenames, compression_type, buffer_size)
iterator = data.make_initializable_iterator()

sess = tf.Session()
sess.run(tf.global_variables_initializer())
sess.run(iterator.initializer)
print(sess.run(iterator.get_next()))
print(sess.run(iterator.get_next()))
print(sess.run(iterator.get_next()))

#model = createModel()
#model.fit(data, batch_size=10, epochs=10, verbose=0)