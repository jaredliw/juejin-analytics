---
theme: condensed-night-purple
---
这是我参与 11 月更文挑战的第 2 天，活动详情查看：[2021最后一次更文挑战](https://juejin.cn/post/7023643374569816095/ "https://juejin.cn/post/7023643374569816095/")。

> - 原文地址：[Bamboolib: One of the Most Useful Python Libraries You Have Ever Seen](https://towardsdatascience.com/bamboolib-one-of-the-most-useful-python-libraries-you-have-ever-seen-6ce331685bb7)
> - 原文作者：[Ismael Araujo](https://ismaelaraujo.medium.com)
> - 译者：[披着狼皮的羊](https://juejin.cn/user/167543676602120)

> 这篇文章是 Bamboolib 系列的第二篇，还没看过上一篇的到我主页/专栏找找吧~

## 数据转换阶段
### 过滤数据
如果要过滤数据集或创建一个包含过滤信息的新数据集，可以在 `Search transformation` 栏中搜索 `filter`，选择要过滤的内容，决定是否要创建新数据集，然后点击执行，就这么简单！

![过滤数据](https://miro.medium.com/max/700/1*cHE0Ll6qPRggedh0wERgHg.gif)

### 合并数据集
如果需要合并两个数据集，直接搜索 `merge`，选择要合并的两个数据集、合并的类型（inner join, left join, right join 或 outer join）和要用于合并数据集的关键列，然后点击执行。你可以创建新数据集或仅编辑当前数据集。

![合并数据集](https://miro.medium.com/max/700/1*s2dskzB_M78tootUspuGOw.gif)

### 提取 datetime 属性
如果你想从日期列中提取诸如星期或月份之类的字符串，你知道该怎么写吗？或者你需要 Google 一下？然而，使用 Bamboolib，你不需要知道代码也不需要 Google。你只需搜索 `extract datetime property`，选择日期列，选择你要提取的内容。

有多种选择供您玩耍。我必须承认，我不知道如何做到这一点，甚至不知道可以使用 Pandas 做到这一点…… 嗯，我刚刚学到了一些新东西。

![提取 datetime 属性](https://miro.medium.com/max/700/1*4rRDAbfSBKEjjJth78wDAQ.gif)

### group by
Pandas 中的其中一个价值体现于 group by。幸运的是，Bamboolib 可以非常直观和轻松地进行 group by。在 `Search transforamtion` 栏中搜索 `group by`，选择要分组的列，然后选择要查看的计算。

在这个例子中，我想查看每个平台的游戏数量和平均得分。从中，我们得知 PlayStation 4 在所有平台中的平均得分最低。

![group by 操作](https://miro.medium.com/max/700/1*leBNTHiRu9b9hdpw5ihaSA.gif)

> Bamboolib 这个主题会拆解成多篇文章和大家探讨，下一篇文章将会是数据可视化的部分，记得留守，明天见！
