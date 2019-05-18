# How to scale a image precisely

First publish at WeChat: [贝贝60秒：怎样不等比例精准缩放一张图](https://mp.weixin.qq.com/s/Q6mO7ZUXE3cqQyUxbI7Tcg)

贝贝60秒：怎样不等比例精准缩放一张图 

原创：曲政 贝拉图 

今天是贝贝报告给你的第 22 天

老板交给你一张图，是来自竞争对手的财报，请你还原出来特定的原始数据。要测量这张图，首先是把它摆在恰当的坐标系里。这里有一个办法，我走通了，汇报给你。

第一步，你需要找到一个能做精准测量的工具，我推荐 LibreCAD，开源，跨平台。

第二步，你需要准备好那张图，清晰，简洁。如果原图来自于 pdf 文档，那就放到最大再截图。截图时只保留必要的信息，与测量无关的部分都丢掉。

第三步，导入图片。

第四步，移动图片。将图片的原点，与坐标原点对齐。

第五步，测量缩放比例。图片中的某个数据，你想让它就是某个长度。那就测量一下当前图片里这个线段的实际长度。理想长度除以实际长度，就是该方向的缩放比例。

第六步，不等比例缩放。通常图上的 x 和 y 坐标有各自的含义，单位也不同。相比于 FreeCAD，LibreCAD 支持 x 和 y 方向的缩放比例不同。

可是，缩放之后，你的那张图却不见了。前功尽弃了吗？保存文档，重新打开，华丽变身之后的它在等你。

![](https://ws2.sinaimg.cn/large/006tNc79ly1g34l4ui50nj30u00jcdi0.jpg)
图 1: LibreCAD 的下载页面

![](https://ws4.sinaimg.cn/large/006tNc79ly1g34l59rtvvj30u0102q63.jpg)
图 2: 插入图片按钮的位置

![](https://ws1.sinaimg.cn/large/006tNc79ly1g34l5jrdz6j30mc0e8mxv.jpg)
图 3: 要改掉移动功能默认带的 30 度旋转

![](https://ws2.sinaimg.cn/large/006tNc79ly1g356c4lpu3j30fm0asjs7.jpg)
图 4: 测量水平和坚直线段长度

![](https://ws2.sinaimg.cn/large/006tNc79ly1g356cetughj30p60g6q3n.jpg)
图 5: 计算两个方向的缩放比例

![](https://ws1.sinaimg.cn/large/006tNc79ly1g356nk0p6yj30u00m7q5v.jpg)
图 6: 缩放按钮的位置

![](https://ws4.sinaimg.cn/large/006tNc79ly1g356nyj4kyj30na0f6gmd.jpg)
图 7: 缩放功能面板

![](https://ws4.sinaimg.cn/large/006tNc79ly1g356py4i6yj30u00pytbj.jpg)
图 8: 缩放之后图片不见了

![](https://ws2.sinaimg.cn/large/006tNc79ly1g356qeul9nj30u00etgnj.jpg)
图 9: 这是为定性分析相位功能搭建的六张图

点击“阅读原文”，是 LibreCAD 的官方下载页。

[阅读原文](https://www.librecad.org/#download) https://www.librecad.org/#download
