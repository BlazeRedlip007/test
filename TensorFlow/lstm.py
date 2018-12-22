#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import tensorflow as tf

input = tf.constant([
    [[1.0], [0.0], [1.0], [0.0], [1.0], [0.0]]
])
lstm = tf.keras.layers.LSTM(
    units = 1,
    activation = None,
    recurrent_activation = None,
    use_bias = False,
    kernel_initializer = "glorot_uniform",
    recurrent_initializer = 'orthogonal',
    bias_initializer = "zeros",
    unit_forget_bias=True,
    kernel_regularizer=None,
    recurrent_regularizer=None,
    bias_regularizer=None,
    activity_regularizer=None,
    kernel_constraint=None,
    recurrent_constraint=None,
    bias_constraint=None,
    dropout=0.0,
    recurrent_dropout=0.0,
    implementation=2,
    return_sequences=True,
    return_state=False,
    go_backwards=False,
    stateful=True,
    unroll=False
)
output = lstm.apply(input)

init = tf.global_variables_initializer()

sess = tf.Session()
sess.run(init)
print(sess.run(output))
