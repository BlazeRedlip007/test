# tf.keras.layers.LSTM

这一部分的单元没有针对GPU优化，使用```tf.keras.layers.CuDNNLSTM```来获得更好的GPU性能。

## 参数

- ```units``` 整数，输出空间的维度
- ```activation``` 激励函数。如果设置为None，不使用任何激励函数。默认使用的是tanh函数。
- ```recurrent_activation``` 循环的步骤中使用的激活函数。默认为hard sigmoid函数，设置为None不使用激活函数。
- ```use_bias``` 布尔值，该层是否采用一个偏置向量
- ```kernel_initializer``` ```kernel```权重矩阵的初始化器，用于对输入进行线性转换
- ```recurrent_initializer``` ```recurrent_kernel```权重矩阵的初始化器，用于对循环状态进行线性转换
- ```bias_initializer``` 偏置向量的初始化器
- ```unit_forget_bias``` 布尔值，如果True，遗忘门在初始化时对偏置加1。设置为True时会强制设置```bias_initializer="zeros"```
- ```kernel_regularizer``` 应用于kernel矩阵权重的正则化函数
- ```recurrent_regularizer``` 应用于```recurrent_kernel```矩阵权重的正则化函数
- ```bias_regularizer``` 偏置向量的正则化函数
- ```activity_regularizer``` 对层的输出进行正则化的函数
- ```kernel_constraint``` 用于kernel权重矩阵的约束函数
- ```recurrent_constraint``` ```recurrent_kernel```约束函数
- ```bias_constraint``` bias约束函数
- ```dropout``` 0到1之间的浮点数。对输入进行线性转换时，抑制部分单元。
- ```recurrent_dropout``` 0到1之间的浮点数。对循环状态进行线性转换时，抑制部分单元。
- ```implementation``` 新机制模式，取值1或者2。模式1将使用大量的和更小的点乘和加法来运算，模式2将将它们批量处理成更少、更大的操作。这些模式将在不同的硬件和不同的应用程序上具有不同的性能表现。
- ```return_sequences``` 布尔值，在输出序列或完整序列中，是否返回最后的输出。
- ```return_state``` 布尔值，是否返回最后的状态，附加在输出中。
- ```go_backwards``` 布尔值，默认False。如果为True, 则向后处理输入序列并返回反向序列。
- ```stateful``` 布尔值，默认为False。如果为True，每个批次中的索引i的每一个样本的最后状态将被用为批次中的下一个索引i的样本的初始状态。
- ```unroll``` 布尔值，默认为False。如果为 True, 则将展开网络, 否则将使用符号循环。展开可以加速一个 RNN, 但是会占用更多的内存。展开只适用于短序列。

## ```__init__```

	__init__(
	    units,
	    activation='tanh',
	    recurrent_activation='hard_sigmoid',
	    use_bias=True,
	    kernel_initializer='glorot_uniform',
	    recurrent_initializer='orthogonal',
	    bias_initializer='zeros',
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
	    implementation=1,
	    return_sequences=False,
	    return_state=False,
	    go_backwards=False,
	    stateful=False,
	    unroll=False,
	    **kwargs
	)

## 实验

	#!/usr/bin/env python3
	# -*- coding: UTF-8 -*-
	
	import tensorflow as tf
	
	input = tf.constant([
	    [[0.1, 0.2, 0.3, 0.4]], # 第一批输入
	    [[0.1, 0.2, 0.3, 0.4]], # 第二批输入
	])
	lstm = tf.keras.layers.LSTM(
	    units = 3,
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
	    return_sequences=False,
	    return_state=False,
	    go_backwards=False,
	    stateful=False,
	    unroll=False
	)
	output = lstm.apply(input)
	
	init = tf.global_variables_initializer()
	
	sess = tf.Session()
	sess.run(init)
	print(sess.run(output))

输出：

	[[0.00212363 0.00045427 0.00152596]
	 [0.00212363 0.00045427 0.00152596]]


----------

## 下面是对上面的说明的一些更正。代码：

	#!/usr/bin/env python3
	# -*- coding: UTF-8 -*-
	
	import tensorflow as tf
	
	input = tf.constant([
	    [[0.1,0.2], [0.2,0.3], [0.3,0.4], [0.4,0.5], [0.5,0.6], [0.6,0.7]]
	])
	lstm = tf.keras.layers.LSTM(
	    units = 3,
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
	    return_sequences=False,
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

看图说话：

![](imgs/lstm.png)

处理周期序列的正确姿势：

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

输出：

	[[[ 0.03019683]
	  [-0.00010327]
	  [ 0.03051727]
	  [-0.00010655]
	  [ 0.03052413]
	  [-0.00010662]]]