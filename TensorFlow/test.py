#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import tensorflow as tf
import time

trainInput = [
  [[0, 0]],
  [[0, 1]],
  [[1, 0]],
  [[1, 1]]
]
trainOutput = [
  [[0]],
  [[1]],
  [[1]],
  [[0]]
]

# 自定义的损失函数
def loss(a, b):
    return tf.abs(tf.subtract(a, b))

model = tf.keras.Sequential([
  tf.keras.layers.Dense(
      units = 2,
      activation = tf.keras.activations.sigmoid,
      use_bias = True,
      input_shape = [1, 2]
  ),
  tf.keras.layers.Dense(
      units = 1000,
      activation = tf.keras.activations.sigmoid,
      use_bias = True
  ),
  tf.keras.layers.Dense(
      units = 100,
      activation = tf.keras.activations.sigmoid,
      use_bias = True
  ),
  tf.keras.layers.Dense(
      units = 1,
      activation = tf.keras.activations.sigmoid,
      use_bias = True
  )
])
model.compile(
  optimizer = tf.keras.optimizers.RMSprop(lr = 0.5),
  loss = "MSE"
)
t0 = time.time()
model.fit(trainInput, trainOutput, 1, 400, 0)
t1 = time.time()
print(model.predict(trainInput));
print(t1 - t0)
