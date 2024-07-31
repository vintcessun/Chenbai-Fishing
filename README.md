# 尘白禁区自动钓鱼
一个基于CNN训练的自动钓鱼模型

其他界面识别直接使用模式匹配，但是图片经过mask处理后经测试能够在1920x1080和2560x1440下运行

需要安装CUDA 11.5.2

我的显卡是RTX4060 评分为8.9

并且按照如下教程进行安装后才能运行

安装完成后在releases下面下载run-all.exe并且运行尘白禁区后运行此程序即可

# 安装过程

(三)、cuda下载和安装
下载cuda和cuDNN。在官网上下载对应的cuda和cuDNN，版本可以低于上面查到的CUDA版本但不能高于电脑支持的版本。

cuda下载地址：CUDA Toolkit Archive | NVIDIA Developer；
cudnn下载地址：cuDNN Archive | NVIDIA Developer。
1)、下载：

我下载的是CUDA Toolkit 11.5.2, 点击前面的 CUDA Toolkit 11.5.2

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c6271d90211c101f48a6de13e94ee50a.png)

选择相应的系统、版本等选项，点击Download下载：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d09942f64d4d7b7c4fe7a513b0fb94bf.png)

2）、安装

a、 双击安装包，此时会出现一个提示框，让你选择临时解压位置（该位置的内容在你安装完cuda之后会自动删除），这里默认即可，点击ok。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7dd77cb527659ecfa423cbd0c7233bcd.png)

b、点击同意并继续：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/74aef1767221f423fa36ea2bb849388c.png)

c、完成上一步后，选择自定义，然后点下一步：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6d9579f895ae701066dddd77a5a11470.png)

d、完成上一步，这里CUDA一定要勾选上，下面的可选可不选，对后续没有影响。

在组件CUDA一栏中，取消勾选Visual Studio Integration（因为我们并没有使用Visual Stduio环境，即使勾选上了也会安装失败）

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/78e57c39a08d7d87617cb2bf978fa547.png)

在Driver components一栏比较Display Driver的新版本和当前版本的信息。
若当前版本高于新版本，则取消勾选Display Driver；
若当前版本低于新版本，则保留默认安装信息即可，否则电脑会死机或者卡顿，甚至可能蓝屏。！！！

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8ad849140b43ae4a5c0302444f1e6027.png)


e、这个安装位置可以自己改。要截图记录一下你装到哪里了，后面要用到！我选择了默认安装位置。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4e793a2d2647fa99151bd98eb7264218.png)

f、正在安装

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4db4963d3dd679eaa62554c80ae20257.png)

g、安装成功！

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/89f5cd4eb0061c12ab22c9483b38a7da.png)

点击关闭即可！

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f2087392931b26b055c7cedf22e9a7b0.png)

检查环境变量：

完成安装后，检查一下环境变量是否存在，一般安装完成会自动配置好环境变量，若是没有，则需手动配置，具体过程如下。

打开 电脑属性，找到 高级系统设置，选择 环境变量 打开。

查看是否有以下系统变量，没有则需要自行添加，对应图片上的名称和值，配置你电脑CUDA安装所在的位置。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d7cb86cdeafc4f1ebe487e522314c1d4.png)

打开系统变量的Path，查看是否有一下两条内容，若没有则需自行添加，一定要配置对安装的位置。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/308b30ea9a8a449a82c63d63ca6396b7.png)


配置好环境变量后，我们检查下CUDA是否安装成功。

打开cmd，输入以下命令查看CUDA是否安装成功（二选一）
如果不能显示以下信息，则说明安装失败。
nvcc -V
nvcc --version
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0ff4d64e7bd78cfaced97f72211efd62.png)

还可以查看CUDA 设置的环境变量。
set cuda
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/567b0f580a93f965253c95fc83b245c6.png)


我们还可以搜索CUDA 的安装目录，找到“nvcc.exe”文件。


CUDA的安装就结束了，接下来下载解压cuDNN文件。

(四)、cudnn下载安装
CUDA并不是实现GPU的神经网络加速库，如果希望针对的是神经网络进行加速，我们还需要安装cuDNN神经网络加速库。

cuDNN并非是应用程序，而是几个文件包，下载后把它复制到CUDA 的目录下即可。
下载地址：cuDNN Archive | NVIDIA Developer。

第一次单击下载时，会让你先注册登录，然后再进行下载，注册过程认真填写内容就没问题，此处略过，接下来进入下载环节。

1)、下载：

下载对应版本的cuDNN。这里选择的是cuDNN v8.3.2 for CUDA 11.5。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d40b46465fe29acb3573ad3b4461a873.png)

、下载解压好安装包后，我们解压可以看到有四个文件：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/20aeb371ef3c03633d25d86a5c32e456.png)

3）、教程的这一步要格外注意！

要将cudnn文件中的对应文件夹下的所有文件复制 到对应的安装目录中，
而 不是 把cudnn文件中的文件夹复制过去。eg：复制的不是cudnn中的bin文件夹，而是bin文件夹下的所有文件。（有重复的文件是正常的，覆盖掉就好！）

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0fb7d1232f3fcf1de5ed4f2ec583d52c.png)

打开cudnn文件中的bin文件夹，将该文件夹中所有的 文件 复制粘贴 到CUDA\v11.5\bin文件夹中：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/647f13ace4a09cb3f003bbf3ddd42957.png)

打开cudnn文件中的include文件夹，将该文件夹中所有的 文件 复制粘贴 到CUDA\v11.5\include文件夹中：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ec6f36dac99fdc0c9867f13b46c7b7eb.png)

打开cudnn文件中的lib文件夹，将该文件夹中所有的 文件 复制粘贴 到CUDA\v11.5\lib\x64文件夹中：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/96f63708c6653e351391e69fc50d5fec.png)

打开cudnn文件中的剩下的文件， 复制粘贴 到CUDA\v11.5文件夹中：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/46c809a92860bfbdafcaec8991012da5.png)

cuDNN其实就是CUDA的一个补丁而已，专为深度学习运算进行优化的，然后我们再添加环境变量！继续往下走。

(五)、配置环境变量
、打开系统变量的Path，在系统变量的path路径下添加以下路径：（具体要根据自己的安装路径下做调整）
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.5\bin
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.5\libnvvp
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.5
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.5\lib\x64
添加好后是这样的：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7b8efe7fb8b4773a4ba1d6649d548883.png)

2)、配置好环境后，我们需要验证环境变量是否配置成功：

打开cmd，进入自己CUDA的安装下路径...\CUDA\v11.5\extras\demo_suite：,我是默认路径，所以我的是：

cd \Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.5\extras\demo_suite
然后分别执行以下两个命令：

.\bandwidthTest.exe
.\deviceQuery.exe
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5597a4053372f8d444366d6f984b47a6.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5597a4053372f8d444366d6f984b47a6.png)

如果Result都为PASS的话则配置成功！

3）、都安装好之后，我们可以继续输入nvidia-smi查看CUDA的信息，然后根据安装版本的信息再去实现其他的库（环境）安装和使用！

nvidia-smi
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/dd7d29e2de6bbe00911b9b1c5c237df4.png)


如图所示，可以看到驱动的版本是527.41；最高支持的CUDA版本是12.0版本。
————————————————

                            版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。

原文链接：https://blog.csdn.net/weixin_43412762/article/details/129824339
