# Image-to-Image Translation with Conditional Adversarial Networks

## 我获得的资料

一开始我找到了这个：
[官方示例](https://github.com/tensorflow/tensorflow/blob/r1.11/tensorflow/contrib/eager/python/examples/pix2pix/pix2pix_eager.ipynb)，
[张雨石 pix2pix-基于GAN的图像翻译](https://blog.csdn.net/stdcoutzyx/article/details/78820728)。
以及按照指引，我找到了这里：
[PDF文献](https://arxiv.org/pdf/1611.07004.pdf)，
[官网链接的文献](https://arxiv.org/abs/1611.07004)。
这两篇文献是同一篇，题目是
“Image-to-Image Translation with Conditional Adversarial Networks”，
翻译成中文是“图像到图像，使用条件对抗网络进行转换”。

既然连官方都是按照论文的理论弄出来的，那么我有理由去浏览这篇P2P文献了，我英文不
好，仔细读很累。

## 初看Image-to-Image Translation with Conditional Adversarial Networks

大概看这篇文章，我印象深刻的是它很长，有数学公式，很硬核。但是我找到了这个链接
[https://github.com/phillipi/pix2pix](https://github.com/phillipi/pix2pix)。
然而里面的代码让人砍不动。

## 确定这次攻略的目标

现在我的目标是，用TensorFlow重现论文
Image-to-Image Translation with Conditional Adversarial Networks的效果。由于
论文长达17页，对于我这种英文不好和非学术圈子的人，显然带来了很大的压力，所以我
下面只是说明我做的事情，关于论文我只能挑选一些能够理解的部分来写。



