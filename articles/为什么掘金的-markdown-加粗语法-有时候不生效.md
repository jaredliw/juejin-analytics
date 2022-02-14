---
theme: orange
---

这是我参与 2022 首次更文挑战的第 5 天，活动详情查看：[2022首次更文挑战](https://juejin.cn/post/7052884569032392740)。

> ……那猹却将身一扭，反从他的胯下逃走了。\*\*这少年便是闰土。\*\*我认识他时，也不过十多岁，离现在将有三十年了；

如上，Markdown 渲染失效了……

先说结论，**这不是掘金的问题，Markdown 就是这么规定的**。更具体地说，这是由于自然语言之间的差异导致的。虽说这造成了一定的影响，但我觉得在可见的未来里 Markdown 规范是不会修改这方面的规则的。

<!-- CommonMark 规范是最早的 Markdown 规范，其他的规范或实现都是基于 CommonMark 的。-->

## CommonMark 规范

> Markdown 将 `*` 与 `_` 作为强调的指示符。被单个 `*` 或 `_` 包裹的文本将被 HTML `<em>` 标签包裹（也就是斜体）；被两个包裹的将被 HTML `<strong>` 标签包裹（也就是粗体）。

在了解问题之前，先来讲讲几个关键名词的意思：

### 定界符序列（delimiter run）

定界符类指的是：

- 一个或一串非转义的 `*`；
- 一个或一串非转义的 `_`。

#### 左侧定界符序列（left-flanking delimiter run）

左侧定界符序列是一个定界符序列，且：

1. 后面不能是空白；
2. 当前面没有空白或标点符号时，后面不能是标点符号。

#### 右侧定界符序列（right-flanking delimiter run）

右侧定界符序列是一个定界符序列，且：

1. 前面不能是空白；
2. 当后面没有空白或标点符号时，前面不能是标点符号。

---

1. 当 `**` 是左侧定界符序列的其中一部分时，它表示的是开始粗体；
2. 当 `**` 是右侧定界符序列的其中一部分时，它表示的是结束粗体；

斜体同理。

（相关的规则有 17 条，这里就不细说了，有兴趣的可以到 [CommonMark 规范](https://spec.commonmark.org/0.30/#right-flanking-delimiter-run)里看看。）

---

结合上方的例子，这里的 `**` 的前面是标点符号，但后面却不是空白或标点符号，所以它不是右侧定界符序列，不会被当作是结束粗体的标识符，自然粗体就不生效了。

> ……闰土。**我认识……

### 为什么会这么定义?

为了能支持嵌套分隔符序列，`**one **two two **three** two two** one**`：

> **one **two two **three** two two** one**

![定界符嵌套](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/17803b187ab8478db83f70573b7e2200~tplv-k3u1fbpfcp-watermark.image?)

这里就不具体说了（也很难具体说），配合上方的几条规矩你就能很好地明白其中的奥义了。

这样定义的影响显而易见，使用非空格分词语言的用户只能骂骂咧咧…… 地继续用下去。

## 怎么解决？

### #1

解决方法其实很简单，在 `**` 后面加个空格即可。

> ……那猹却将身一扭，反从他的胯下逃走了。**这少年便是闰土。** 我认识他时，也不过十多岁，离现在将有三十年了；

但像我这种要求格式高度统一的人可就不乐意了；中文可是没有空格这一说法的。

Github 用户 [haqer1](https://github.com/haqer1) 提供了一种更好的解决方案 —— **零宽空格（zero-width space，ZWSP）**。

### #2

这就是 ZWSP：

> ​

什么？你说你看不到？

那就对了，ZWSP 是一种不可打印的 Unicode 字符（`U+200B`），**用于可能需要换行处**。

我们可以使用 ZWSP **指定长文字的换行位置**；只有当荧幕宽度不足以单行显示时 ZWSP 才会起作用。

举个例子，没有使用 ZWSP 时是这样的：

> LongLongLongLongLongLongLongLongBreakBeforeHereLongLongLongLongLongLongLongLongLongLongLongLongLongLongText

使用 ZWSP 后是这样的：

> LongLongLongLongLongLongLongLong​BreakBeforeHereLongLongLongLongLongLongLongLongLongLongLongLongLongLongText

由于 ZWSP 这种特殊属性，它也被用于绕过敏感词检查（各位后端大佬们看好了，实现功能时多注意点）、创造不可复制的伪链接等等。

---

回到一开始的问题，我们只需要将 ZWSP 加在右翼定界符之前就可以了：

> ……那猹却将身一扭，反从他的胯下逃走了。**这少年便是闰土。​**我认识他时，也不过十多岁，离现在将有三十年了；
>
> <small>（ZWSP 加在句号之后，`**` 之前）</small>

这个字符可以到 Unciode 字符表网站上复制下来：<https://unicode-table.com/en/200B/>

![复制 Unicode 字符](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/b5c38b1101d546269fdd806901e17700~tplv-k3u1fbpfcp-watermark.image?)

---

**等等，零宽空格不也是空格吗？这和你上面说的规则（右侧定界符序列的前面不能是空格）矛盾啊……**

这就得说说规则里空格的定义了。

#### 空格是什么？

这里的空格指的是 **Unicode 空格字符**。

> Unicode 空格字符包含 tab（`U+0009`）、line feed（`U+000A`）、form feed（`U+000C`）、carriage return（`U+000D`）以及任何在 Unicode `Zs` 类别里的字符。

<small>注：line feed（LF，`\n`）和 carriage return（CR，`\r`）都是换行。在 Windows 里的换行是 CR+LF；在 Unix 系统里的换行是 LF。</small>

Unicode 里的字符是按类别区分的，第一个大写字母为主类（major category），第二个小写字母为次类（minor category）。

上方的 `Zs` 表示的是“分隔符，空格（seperator，space）”类。`Zs` 类里有 17 个字符，如下：

![Unicode `Zs` 类](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/f08b4e1c4aa8404ba41b903a0b931fb4~tplv-k3u1fbpfcp-watermark.image?)

(图片中的网站：<https://www.compart.com/en/unicode/category/Zs>)

由上可见，列表里并没有 `U+200B`，所以**ZWSP 不是空格**（虽然它叫零宽空格）。ZWSP 属于 `Cf` 类，也就是“其他，格式（other, format）”类。

---

同理，Java 对空格的定义也是如此：

```java
System.out.println(Character.isWhitespace(' '));
System.out.println(Character.isWhitespace('\t'));
System.out.println(Character.isWhitespace('\n'));
System.out.println(Character.isWhitespace('\u200b')); // ZWSP
```

结果：

```
true
true
true
false
```

## 题外话

### 1. 这不是 bug，这是 feature！

（我乱说的，仅代表个人立场）

为什么在文章开头时我说这东西应该是解决不了的呢？

这就得说另一个故事了，看看 CommonMark 论坛上的其中一个讨论：

![image.png](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/e711b902b54f4a248310e346c92faf03~tplv-k3u1fbpfcp-watermark.image?)

181 楼，讨论了将近 8 年的时间，你们猜讨论了什么？

公布答案：内容是关于**表格的 Markdown 语法支持**：

```markdown
| 标题 1 | 标题 2 |
| ------ | ------ |
| 内容 1 | 内容 2 |
```

没错，在 CommonMark 规范中的表格是要以 HTML 来书写的。

隔壁 [GitHub Flavored Markdown（GFM，也就是 Github 定义的 Markdown 规范）](https://www.markdownguide.org/extended-syntax/) 早都玩出花儿了，这边还在相互扯皮。一方一直建议添加新语法，各种建议、各种排版样式的都有；另一方就极力反对，说什么这种写法难以阅读、难以维护啊什么的……

嗯，我同意，用 HTML 写表格…… 真棒：

```html
<table>
  <thead>
    <tr>
      <th>标题 1</th>
      <th>标题 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>内容 1</td>
      <td>内容 2</td>
    </tr>
  </tbody>
</table>
```

### 2. 这明明是 Markdown 的问题，为什么你标题要加个“掘金”？

（确实，我在 Github 上也遇到过这样的问题。）

简单来说，这样写有两个原因：

#### #1

文章灵感来源于 `juejin-markdown-themes` 这个仓库中的一个 issue：

![issue 截图](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/a94f8da78b9f41eb82262897d2a71635~tplv-k3u1fbpfcp-watermark.image?)

一看发现自己也遇到过，但又不知道原因，兴趣一下就来了。一开始时看了看掘金的 Markdown 编辑器 —— `bytemd`，发现 Markdown 解析是调用 `remark` 库和 `rehype` 库的，接着就一路溯源，最后定位到了 CommonMark 规范……

#### #2

这样写标题不就更有带入感嘛，让人有一种：欸，我好像也遇到过的感觉……

<s>（再顺便诱捕一下掘金运营）</s>

## 参考资料

1. https://talk.commonmark.org/t/bold-failure-in-chinese-sentence-because-of-the-usage-of-chinese-punctuation-is-different-from-english/3478/5
2. https://ld246.com/article/1597581380183
3. https://github.com/commonmark/commonmark-spec/pull/644
4. https://spec.commonmark.org/0.30/#emphasis-and-strong-emphasis
5. https://blog.meathill.com/tech/fe/zero-width-space-issue-and-usage.html
6. https://en.wikipedia.org/wiki/Unicode_character_property
7. https://talk.commonmark.org/t/tables-in-pure-markdown/81/6
