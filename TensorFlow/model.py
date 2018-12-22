#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import tensorflow as tf

# 准备数据
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

model = tf.keras.models.load_model('xor.h5')
# 配置网络的优化算法和误差算法，tf.keras下找optimizer和loss
model.compile(
  optimizer = 'SGD',
  loss = 'MSE',
  metrics = ['accuracy']
)

# 开始训练，第5个参数是0，关闭进度条
model.fit(trainInput, trainOutput, 1, 100, 0);
# 打印预测结果
print(model.predict(trainInput));

# 保存模型，需要h5py。pip3 install --upgrade h5py
model.save('xor.h5');

# 加载模型使用model = tf.keras.models.load_model('xor.h5')
