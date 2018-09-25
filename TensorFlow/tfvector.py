#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# 向量

# TensorFlow and tf.keras
import tensorflow as tf


print(tf.add(1, 2))
print(tf.add([1, 2], [3, 4]))
print(tf.square(5))
print(tf.reduce_sum([1, 2, 3]))
print(tf.encode_base64("hello world"))

# Operator overloading is also supported
print(tf.square(2) + tf.square(3))