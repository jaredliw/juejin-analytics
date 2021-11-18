---
theme: Chinese-red
---
小知识，大挑战！本文正在参与「[程序员必备小知识](https://juejin.cn/post/7008476801634680869 "https://juejin.cn/post/7008476801634680869")」创作活动。本文已参与「[掘力星计划](https://juejin.cn/post/7012210233804079141 "https://juejin.cn/post/7012210233804079141")」，赢取创作大礼包，挑战创作激励金。

在处理数据时，我们可能需要动态地修改 Markdown 文件以展示分析结果。这时，一个好用又简便的第三方库就派上用场了。大家好，我是披着狼皮的羊，今天和大家介绍一个处理 Markdown 的 Python 库：`mdutils`。

> PyPI 项目主页：https://pypi.org/project/mdutils/
>
> Github 仓库：https://github.com/didix21/mdutils/
>
> 官方文档：http://mdutils.readthedocs.io/en/latest/

## 写在前面

`mdutils` 支持 ATX（大家最为熟知的 # 写法）和 [Setext](https://en.wikipedia.org/wiki/Setext)（.rst 文件的写法，有用过 Sphinx 的小伙伴们应该知道把）两种风格。除了常用的基础语法，这个库也支持文字着色、居中等骚操作。由于这些东西我并不是很常用，Github Markdown 也不支持，就不展开讨论了，有兴趣的伙伴们请移步到官方文档。

用之前直接 pip 安装即可：
```bash
pip install mdutils
```

## 创建 Markdown 文件

```python
from mdutils import mdutils

f = MdUtils(file_name="hello.md")
```
`file_name` 的 `.md` 后缀可写可不写，不影响输出结果。

`MdUtils` 还有一个可选参数 `title`，将标题以 Setext 风格写在文件开头。

```text
This is a title
===============
```

**创建 `MdUtils` 实例后不会马上创建 Markdown 文件**，需在代码最后一行手动执行：
```python
f.create_md_file()
```

## 标题
```python
mdFile.new_header(level=1, title='Header 1')
mdFile.new_header(level=2, title='Header 2')
mdFile.new_header(level=3, title='Header 3')
mdFile.new_header(level=4, title='Header 4')
mdFile.new_header(level=5, title='Header 5')
mdFile.new_header(level=6, title='Header 6')
```

```text
# Header 1
## Header 2
### Header 3
#### Header 4
##### Header 5
###### Header 6
```

## 段落和文本格式
```python
f.new_line("This is a **line** with line break.", wrap_width=0)
```

```text
This is a **line** with line break.
```

**用这个方法的时候记得带上 `wrap_width=0`**，因为其默认值是 `120`，会使你的句子在奇怪的地方换行（我表示非常的不理解）。

## 表格
```python
list_of_strings = ['Items', 'Descriptions', 'Data', 'Item 0', 'Description Item 0', '0', 'Item 1', 'Description Item 1', '1', 'Item 2', 'Description Item 2', '2', 'Item 3', 'Description Item 3', '3', 'Item 4', 'Description Item 4', '4']
f.new_table(columns=3, rows=6, text=list_of_strings)
```

```text
|Items|Descriptions|Data|
| :---: | :---: | :---: |
|Item 0|Description Item 0|0|
|Item 1|Description Item 1|1|
|Item 2|Description Item 2|2|
|Item 3|Description Item 3|3|
|Item 4|Description Item 4|4|
```

`new_table` 的 `text_align` 参数可让内容向左/右对齐，参数选项包含 `left`、`right` 和 `center`，默认 `center`。

## 链接

```python
f.new_line('This is an inline link: ' + f.new_inline_link(link='https://github.com/didix21/mdutils', text='mdutils'))
```

```text
This is an inline link: [mdutils](https://github.com/didix21/mdutils)
```
与其他方法不同的是，`new_inline_link` 方法只返回 markdown 格式的链接，**不会直接写入文件**。

## 列表

### 无序列表
```python
items = ['Item 1', 'Item 2', 'Item 3', 'Item 4', ['Item 4.1', 'Item 4.2', ['Item 4.2.1', 'Item 4.2.2'], 'Item 4.3', ['Item 4.3.1']], 'Item 5']
f.new_list(items)
```

```
- Item 1
- Item 2
- Item 3
- Item 4
    - Item 4.1
    - Item 4.2
        - Item 4.2.1
        - Item 4.2.2
    - Item 4.3
        - Item 4.3.1
- Item 5
```

### 有序列表
```python
items = ['Item 1', 'Item 2', 'Item 3', 'Item 4', ['Item 4.1', 'Item 4.2', ['Item 4.2.1', 'Item 4.2.2'], 'Item 4.3', ['Item 4.3.1']], 'Item 5']
f.new_list(items, marked_with='1')
```

```text
1. Item 1
2. Item 2
3. Item 3
4. Item 4
    1. Item 4.1
    2. Item 4.2
        1. Item 4.2.1
        2. Item 4.2.2
    3. Item 4.3
        1. Item 4.3.1
5. Item 5
```

### Todo 列表
```python
items = ['Item 1', 'Item 2', ['1. Item 2.1', '2. Item 2.2'], 'Item 3']
f.new_checkbox_list(items)
```

```
- [ ] Item 1
- [ ] Item 2
    - [ ] 1. Item 2.1
    - [ ] 2. Item 2.2
- [ ] Item 3
```

如果想打勾其中的一些，在要该字符串前添加一个 `x`：
```python
items = ['Item 1', 'Item 2', ['Item 2.1', 'x Item 2.2'], 'x Item 3']
f.new_checkbox_list(items)
```

```text
- [ ] Item 1
- [ ] Item 2
    - [ ] Item 2.1
    - [x] Item 2.2
- [x] Item 3
```

**这个做法我非常的不理解，如果我就想显示 `x Item 2.2` 又该怎么办呢？？？**

## 图片
```python
mdFile.new_line(mdFile.new_inline_image(text='snow trees', path='https://github.com/didix21/mdutils/blob/master/doc/source/images/photo-of-snow-covered-trees.jpg'))
```

```
![snow trees](https://github.com/didix21/mdutils/blob/master/doc/source/images/photo-of-snow-covered-trees.jpg)
```

和 `new_inline_link` 一样，`new_inline_image` 只返回 markdown 格式的链接，**不会直接写入文件**。

## 自动生成目录
在 `MdUtils.create_md_file` 之前一行执行：
```python
f.new_table_of_contents(table_title='Table of Contents', depth=6）
```
生成的目录会放在文件开头。**默认只生成一级目录**，可通过 `depth` 参数修改。

## 总结

总的来说，这个第三方库可圈可点，使用的话有几点需要注意：

1. 记得转义 `]`、`)` 等字符（视情况而定）；
2. 如果上线使用的话可能会有**代码注入的问题**，**有访问本地文件的风险**；
3. 其他需要注意的点我已经标粗了，大家留意，避免踩坑。

其他的没什么问题，用不用这个库，大家自行斟酌。

说句题外话，我也贡献了为这个库贡献了 <small><small>一行</small></small> 代码：

![screencapture-github-didix21-mdutils-pull-63-2021-10-30-00_16_57.png](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/6e4e96c154f34130b9bcc8724a094555~tplv-k3u1fbpfcp-watermark.image?)

如果有后续的话会再跟大家更新，拜拜~
