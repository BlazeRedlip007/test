#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import tensorflow as tf

x = tf.constant([[-2.25 + 4.75j], [-3.25 + 5.75j]])
test = tf.abs(x)  # [5.25594902, 6.60492229]

sess = tf.Session()
# 下面这一步操作实际上就是将到目前为止的张量定义发送给显卡，大概吧
sess.run(tf.global_variables_initializer())

# 打印test的值
print(sess.run(test))