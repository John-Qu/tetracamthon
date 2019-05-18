# How to Get Data from Chart

First publish at WeChat: [贝贝60秒：怎样取得位图曲线上的各点数据](https://mp.weixin.qq.com/s/bAhpcFNdFOLhhapKRivkPg)

你用 LibreCAD 准备好了一张图，下一步，怎么取得这张位图曲线上的各点数据呢？我走通一条路，可能是笨办法，但是有效，也报告出来吧。
简要来说，有四个步骤。
1. 描图。用样条曲线把位图上的曲线细致地描绘出来。注意，不能连续三点用水平约束，LibreCAD 会卡死，导致前功尽弃。
2. 划线。你想在什么位置取点，那就画出切分的线来。
3. 割点。用曲线作为边界，切割出各个线段。这样就把曲线的位置信息转换为线段的长度信息。
4. 取数。批量取得这些线段的信息，需要一点点技巧，和很多的耐心。我暂时只找到两个办法，一个方法是读取线段属性，看线段端点的 Y 值。另一个方法是输出线段长度到报告窗口，这样方便批量处理。注意，适时把报告窗口中的数据转存到电子表格中，及时校对有没有遗漏。
位图中的曲线是连续信息，我们要的也是能随意提取数据的连续曲线。上面的办法笨，因为绕了很大一圈：把连续信息离散化，然后再用各个离散点拟合出连续曲线。如果 LibreCAD 中的样条曲线能够直接导入 Python，那就好了。

![图 1: 用样条曲线细致地描绘位图上的曲线](https://ws1.sinaimg.cn/large/006tNc79ly1g34klxpm4bj30u00frmyg.jpg)
图 1: 用样条曲线细致地描绘位图上的曲线

![图 2: 读取线段属性，看线段端点的 Y 值](https://ws4.sinaimg.cn/large/006tNc79ly1g34klyfbp0j30u00t977g.jpg)
图 2: 读取线段属性，看线段端点的 Y 值

![图 3: 输出线段长度到报告窗口](https://ws1.sinaimg.cn/large/006tNc79ly1g34kly31vjj30u00sz0wq.jpg)
图 3: 输出线段长度到报告窗口

![图 4: 报告窗口中的数据转存到电子表格中处理](https://ws4.sinaimg.cn/large/006tNc79ly1g34klxmgoqj30h80vmdi1.jpg)
图 4: 报告窗口中的数据转存到电子表格中处理

![图 5: 用电子表格数据做出的曲线](https://ws1.sinaimg.cn/large/006tNc79ly1g34klxw5qrj30ny1laju5.jpg)
图 5: 用电子表格数据做出的曲线
