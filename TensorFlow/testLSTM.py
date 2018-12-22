#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import tensorflow as tf
import numpy

trainInput = numpy.array([
    [[1.0], [0.0], [1.0], [0.0], [1.0], [0.0]],
    [[0.0], [1.0], [0.0], [1.0], [0.0], [1.0]]
])
trainOutput = numpy.array([
    [1.0],
    [0.0]
])

model = tf.keras.Sequential()
model.add(tf.keras.layers.Flatten(input_shape = (6, 1)))
model.add(tf.keras.layers.Dense(units = 10, activation = "tanh", use_bias = True))
model.add(tf.keras.layers.Dense(units = 1, activation = "tanh", use_bias = True))
model.compile(
  optimizer = tf.keras.optimizers.Adam(lr = 0.0002),
  loss = "MSE"
)
model.fit(trainInput, trainOutput, 1, 4000, 0)
print(model.predict(trainInput));
