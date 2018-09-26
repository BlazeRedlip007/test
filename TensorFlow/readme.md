# TensorFlow - 快速攻略学习笔记

## 快速攻略TensorFlow

今天玩一玩Python版本的TensorFlow，首先看一下官方给出的[攻略](https://tensorflow.google.cn/get_started/get_started_for_beginners "Graph Execution 使用入门")：

>在您开始编写 TensorFlow 程序时，我们强烈建议您重点了解下列两个高阶 API：

> - Estimator

> - Dataset

另外：

>执行下列步骤以获取示例程序：

>通过输入以下命令从 GitHub 克隆 TensorFlow 模型代码库：

>```git clone https://github.com/tensorflow/models```

>将此分支内的目录更改为包含本文档中所用示例的位置：

>```cd models/samples/core/get_started/```

克隆过程有点慢，看点别的。

![](imgs/tensorflow_programming_environment.png)

看来TensorFlow.js跟这个差不多了。接着看到这个：

>要指定模型类型，请实例化一个 Estimator 类。TensorFlow 提供了两类 Estimator：

>预创建的 Estimator：有人已为您编写完成。

>自定义 Estimator：必须自行编码（至少部分需要）。

>为了实现神经网络，premade_estimators.py 程序会使用一个叫做tf.estimator.DNNClassifier 的预创建 Estimator。此 Estimator 会构建一个对样本进行分类的神经网络。

看来Estimator内有已经封装好的神经网络模型，估计是传递一些配置参数就可以拿来用的。

    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        hidden_units=[10, 10],
        n_classes=3)

看示例代码，果然跟我想的一样。

>如果训练样本是随机排列的，则训练效果最好。要对样本进行随机化处理，请调用 tf.data.Dataset.shuffle。将 buffer_size 设置为大于样本数 (120) 的值可确保数据得到充分的随机化处理。

>在训练期间，train 方法通常会多次处理样本。在不使用任何参数的情况下调用 tf.data.Dataset.repeat 方法可确保 train 方法拥有无限量的训练集样本（现已得到随机化处理）。

也就是说，数据集转换和处理的方法都在Dataset里了。

>为评估模型的效果，每个 Estimator 都提供了 evaluate 方法。premade_estimator.py 程序会调用 evaluate。

看到这里，发现连怎么写程序都不清楚。自己写一个程序玩一下？

## TensorFlow运作的过程

理解的重点两个，

1. 通过框架来定义的张量和操作都不会立刻运行；
2. sess.run()方法将定义的操作发送给显卡，告诉显卡执行什么操作，等显卡操作完成后才返回。

### 官方示例

	#!/usr/bin/env python3
	# -*- coding: UTF-8 -*-

	import tensorflow as tf
	import numpy as np

	# 使用 NumPy 生成假数据(phony data), 总共 100 个点.
	x_data = np.float32(np.random.rand(2, 100)) # 随机输入
	y_data = np.dot([0.100, 0.200], x_data) + 0.300

	# 构造一个线性模型
	# 
	b = tf.Variable(tf.zeros([1]))
	W = tf.Variable(tf.random_uniform([1, 2], -1.0, 1.0))
	y = tf.matmul(W, x_data) + b

	# 最小化方差
	loss = tf.reduce_mean(tf.square(y - y_data))
	optimizer = tf.train.GradientDescentOptimizer(0.5)
	train = optimizer.minimize(loss)

	# 初始化变量
	init = tf.global_variables_initializer()

	# 启动图 (graph)
	sess = tf.Session()
	sess.run(init)

	# 拟合平面
	for step in range(0, 201):
	    sess.run(train)
	    if step % 20 == 0:
	        print(step, sess.run(W), sess.run(b))

	# 得到最佳拟合结果 W: [[0.100  0.200]], b: [0.300]

结合官网的示例和网上找到的说法，TensorFlow跟JS版本的运作原理有点相似的地方：都是将运算交给显卡去算的，不是在CPU上算，所以代码写出来有点奇怪。

似乎凡是调用tf里面的方法，代码都在TensorFlow内进行某些不为人知的操作，当调用sess.run()的时候将这些不为人知的操作传输给显卡进行计算。

这个sess.run()是同步的，它将参数里面涉及的tf代码发给显卡后等待显卡计算完，将返回值返回给python环境。

从目前这份示例上看，```tf.run()```接受的是一个Tensor对象的时候，返回这个对象当前的值（这个对象定义后sess.run()发送给显卡了，它返回的是对象在显卡中的值），如果sess.run()接受的是一个运算过程，比如 ```tf.global_variables_initializer()``` 或 ```optimizer.minimize(loss)``` ，那么显卡就会执行对应的运算。

官方文档说明是， sess.run() 接的是叫做Op的东西，它代表了某些操作。这种新颖的编程方式实质上是面向设备编程。熟悉这种编程方式看来需要分清楚哪些东西是Python里面跑，而哪些东西是在显卡里面跑。

另外的问题是，你编写了一个 Tensor ，想要直接打印出这个 Tensor 的值是徒劳的，你非得用 sess.run() 把它发送到显卡，然后根据 sess.run() 的返回值来查看变量值。sess.run() 完全就是跟显卡通信的接口嘛。

为了验证我的猜测，我折腾出了下面这个代码：

    #!/usr/bin/env python3
    # -*- coding: UTF-8 -*-

    import tensorflow as tf

    test = tf.Variable(tf.zeros([2, 2]))

    sess = tf.Session()
    # 下面这一步操作实际上就是将到目前为止的张量定义发送给显卡，大概吧
    sess.run(tf.global_variables_initializer())

    # 打印test的值
    print(sess.run(test))

程序输出：

    C:\python>python test.py
    [[0. 0.]
     [0. 0.]]

印证了我所想，sess.run() 把“tf操作代码”（就是Op）发送给显卡，然后返回结果！

## 能被优化的和不能被优化的

```tf.train.GradientDescentOptimizer(0.5)```就是梯度下降嘛。那些可以被用来下降的值不就是由```tf.Variable()```定义的咯。numpy定义的值是不能被修改的。这样看，1，明确定义为```tf.Variable()```的值才会在优化的时候被修改，2，Tensor跟numpy数组是兼容的。

## 文档怎么看

### 基本运算

找[第一个函数](https://tensorflow.google.cn/api_docs/python/tf/abs)，写一份代码测一下：

    #!/usr/bin/env python3
    # -*- coding: UTF-8 -*-

    import tensorflow as tf

    x = tf.constant([[-2.25 + 4.75j], [-3.25 + 5.75j]])
    test = tf.abs(x)  # [5.25594902, 6.60492229]

    # 初始化变量到显卡
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    # 打印test的值
    print(sess.run(test))

输出

	[[5.25594901]
	 [6.60492241]]


```tf.constant``` 不就是定值，不会被优化嘛。

	tf.constant(
	    value,
	    dtype=None,
	    shape=None,
	    name='Const',
	    verify_shape=False
	)

文档的 ```value``` 意思就是自己定义的Python的list数据类型，```dtype``` 就是数据类型嘛。

好了，**tf** 基本运算部分过。

### 构造模型

这部分代码直接运行好像有毛病。不管了，看人家的思路。

	import tensorflow as tf
	mnist = tf.keras.datasets.mnist
	
	(x_train, y_train),(x_test, y_test) = mnist.load_data()
	x_train, x_test = x_train / 255.0, x_test / 255.0
	
	model = tf.keras.models.Sequential([
	  tf.keras.layers.Flatten(),
	  tf.keras.layers.Dense(512, activation=tf.nn.relu),
	  tf.keras.layers.Dropout(0.2),
	  tf.keras.layers.Dense(10, activation=tf.nn.softmax)
	])
	model.compile(optimizer='adam',
	              loss='sparse_categorical_crossentropy',
	              metrics=['accuracy'])
	
	model.fit(x_train, y_train, epochs=5)
	model.evaluate(x_test, y_test)

这个跟TensorFlow.js不是一样的嘛，它用的是tf.keras提供的方法而已啊。[https://tensorflow.google.cn/tutorials/keras/basic_classification](https://tensorflow.google.cn/tutorials/keras/basic_classification) ，还有 [https://tensorflow.google.cn/tutorials/estimators/cnn](https://tensorflow.google.cn/tutorials/estimators/cnn)。

代码，这两行用来加载数据：

    (x_train, y_train),(x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

调用API构建整个模型：

    model = tf.keras.models.Sequential([
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(512, activation=tf.nn.relu),
      tf.keras.layers.Dropout(0.2),
      tf.keras.layers.Dense(10, activation=tf.nn.softmax)
    ])

编译模型，指定优化的方法：

    model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

```fit()```方法，看文档意思是：Trains the model for a fixed number of epochs (iterations on a dataset).

    model.evaluate(x_test, y_test)

上面一句话是测试模型性能的。到此为止，大概流程过了一遍。编写一个神经网络至少需要哪些东西已经齐全。

晚安。

----------

接着上次的写。由于加载数据失败，这里不加载了。

	#!/usr/bin/env python3
	# -*- coding: UTF-8 -*-
	
	import tensorflow as tf
	
	model = tf.keras.models.Sequential([
	  tf.keras.layers.Flatten(),
	  tf.keras.layers.Dense(512, activation=tf.nn.relu),
	  tf.keras.layers.Dropout(0.2),
	  tf.keras.layers.Dense(10, activation=tf.nn.softmax)
	])
	model.compile(optimizer='adam',
	              loss='sparse_categorical_crossentropy',
	              metrics=['accuracy'])

Error

	Traceback (most recent call last):
	  File "model.py", line 11, in <module>
	    tf.keras.layers.Dense(10, activation=tf.nn.softmax)
	  File "D:\Program Files\python\lib\site-packages\tensorflow\python\keras\_impl\keras
	\models.py", line 439, in __init__
	    self.add(layer)
	  File "D:\Program Files\python\lib\site-packages\tensorflow\python\keras\_impl\keras
	\models.py", line 482, in add
	    raise ValueError('The first layer in a '
	ValueError: The first layer in a Sequential model must get an `input_shape` argu
	ment.

吐槽，这部分都是官网的代码居然会出问题，原因：没定义```input_shape```。修改后：

	#!/usr/bin/env python3
	# -*- coding: UTF-8 -*-
	
	import tensorflow as tf
	
	# 别名：tf.keras.models.Sequential
	model = tf.keras.Sequential([
	  tf.keras.layers.Flatten(input_shape = (3, 32, 32)),
	  tf.keras.layers.Dense(512, activation = tf.nn.relu),
	  tf.keras.layers.Dropout(0.2),
	  tf.keras.layers.Dense(10, activation = tf.nn.softmax)
	])
	
	# keep_dims is deprecated, use keepdims instead 这个这里没用到不管它了
	model.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])

## 自定义模型和模型的训练

这里定义网络没问题了。写一个异或的来训练一下：

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

    # 顺序层
    model = tf.keras.Sequential([
      # 去tf.keras.layers里面找神经网络层，第一个是输入层
      tf.keras.layers.Dense(2, tf.keras.activations.tanh, 1, input_shape = (1, 2)),
      tf.keras.layers.Dense(1, tf.keras.activations.sigmoid, 1)
    ])
    # 配置网络的优化算法和误差算法，tf.keras下找optimizer和loss
    model.compile(
      optimizer = 'Adam',
      loss = 'MSE',
      metrics = ['accuracy']
    )

    # 开始训练，第5个参数是0，关闭进度条
    model.fit(trainInput, trainOutput, 4, 15000, 0);
    # 打印预测结果
    print(model.predict(trainInput));

    # 保存模型，需要h5py。pip3 install --upgrade h5py
    model.save('xor.h5');

    # 加载模型使用model = tf.keras.models.load_model('xor.h5')


输出的预测结果是

    [[[0.00373096]]

     [[0.9945686 ]]

     [[0.9954489 ]]

     [[0.00281842]]]

代码里面15000次是从小到大试出来的，运行一次1分钟以内可以结束。

至此，简单的模型训练和使用方法完，可以简单玩耍了。