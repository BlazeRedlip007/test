#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# How to read datas from TFRecord file?

import tensorflow as tf

# tf.data.TFRecordDataset
# A Dataset comprising records from one or more TFRecord files.
# __init__(
#    filenames,
#    compression_type=None,
#    buffer_size=None,
#    num_parallel_reads=None
# )

# A tf.string tensor or tf.data.Dataset containing one or more filenames.
filenames = tf.constant(['dataset/images.TFRecord.gz'])

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
print(data)
