> - 原文地址：[10 CSS tips you need to know right now.](https://devdojo.com/abhiraj/10-css-tips-you-need-to-know-right-now#_3-add-smooth-scroll-in-just-one-line-of-css)
> - 原文作者：[Abhiraj Bhowmick](https://devdojo.com/abhiraj)
> - 译文出自：[掘金翻译计划](https://juejin.cn/translate)

## 1. 改变输入框的光标颜色

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/eb6f70804e574badbe6f4de5dbb595a3~tplv-k3u1fbpfcp-watermark.image?)

```css
input {
  caret-color: red;
}
```

## 2. 3 行 CSS 将任意元素居中

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/4c91617c5d5c434f9ce11fd76f912bd8~tplv-k3u1fbpfcp-watermark.image?)

```css
.center {
  display: flex;
  align-items: center;
  justify-content: center;
}
```

## 3. 1 行 CSS 添加平滑滚动

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/65909c9a5fa14999ad30ac6d4fefd166~tplv-k3u1fbpfcp-watermark.image?)

```css
html {
  scroll-behavior: smooth;
}
```

## 4. 将任意图片添加到页面标题以创建炫酷的效果

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/150a031255684d3f9f0547814fb74363~tplv-k3u1fbpfcp-watermark.image?)

```css
h1 {
  background: blue url("image.jpg");
  backgroud-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  margin-top: 20px;
  font-size: 120px;
}

@media(max-width: 600px) {
  h1 {
    font-size: 45px;
  }
}
```

## 5. 纯 CSS 实现多行文字截断

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7deedc4967034d689017b78d8aed513b~tplv-k3u1fbpfcp-watermark.image?)

```css
.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

## 6. 使任意元素可缩放

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/006ae53694ea4fc7bac3c1821fbe51b1~tplv-k3u1fbpfcp-watermark.image?)

```css
.resize {
  resize: both;
}
```

## 7. 将图片作为鼠标样式
![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/34c07dfab33b467d8aea68ef3edbb172~tplv-k3u1fbpfcp-watermark.image?)

```css
.my-cursor {
  cursor: url("image.png"), auto;
}
```

## 8. 平滑滚动动画

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/f19a4256d60f4bdaa54f1223086774d8~tplv-k3u1fbpfcp-watermark.image?)

```css
html {
  scroll-behavior: smooth;
}
```

## 9. 启用混合模式

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d8b514a9fdbe429f9f9951b3b6d26943~tplv-k3u1fbpfcp-watermark.image?)

```css
body {
  background-image: url("image.jpg");
  background-color: purple;
  background-blend-mode: screen;
}
```

## 10. 设置处于高亮状态时的样式

![carbon (5).png](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/2f15494ac4e94bf3ac1d353b61cd02f4~tplv-k3u1fbpfcp-watermark.image?)

```css
p::selection {
  background-color: pink;
  color: rgb(235, 23, 41);
}
```

感谢阅读！

