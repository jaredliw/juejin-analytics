---
theme: qklhk-chocolate
---
这是我参与 11 月更文挑战的第 4 天，活动详情查看：[2021最后一次更文挑战](https://juejin.cn/post/7023643374569816095/ "https://juejin.cn/post/7023643374569816095/")。

从 `a = [1, 2, 3, 4, 5, 6]` 中获得所有偶数的立方，你会怎么做？

你或许会回答我：
```python
list(map(lambda x: x ** 3, filter(lambda x: x % 2 == 0, a)))
```

但有了 pipe 这个第三方库，代码变得简洁许多：
```python
from pipe import select, where

list(a | select(lambda x: x ** 3) | where(lambda x: x % 2 == 0))
```

## 介绍
类似于 bash，pipe 库是中缀语法（infix syntax）在 Python 中的实现。这是一种很有新意的使用迭代器和生成器的方法 —— 把数据看作是流（stream）并在并在一系列函数中处理、传递。这种写法能大大地避免函数之间的嵌套，代码简洁有力！

老实说，看到这里，我已经想把我所有的代码重构了……（但当然不行）

pip 下载：
```bash
pip install pipe
```

## 那些使用的函数

### `select` —— 内建 `map` 的替代

示例：求前 100 个自然数的平方和与总和的平方之间的差。（Project Euler 第六题）

```python
sum(range(101)) ** 2 - sum(range(101) | select(lambda x: x ** 2))
```

### `where` —— 内建 `filter` 的替代

示例：计算 1000 以下所有 3 或 5 的倍数之和。（Project Euler 第一题）
```python
sum(range(1000) | where(lambda x: x % 3 == 0 or x % 5 == 0))
```

### `take_while` 和 `skip_while` —— `itertools.takewhile` 和 `itertools.dropwhile` 的替代

`take_while` 当 lambda 表达式为真时就返回元素，`skip_while` 则相反。

示例：考虑斐波那契数列中值不大于 4000000 的项，找出偶数值项的总和。（Project Euler 第二题）
```python
def fib(a, b):
  ...

sum(fib(1, 2) | where(lambda x: x % 2 == 0) | take_while(lambda x: x < 4000000))
```

### `chain` —— 链接几组可迭代对象

示例：
```python
>>> list([[1, 2], [3, 4], [5]] | chain)
[1, 2, 3, 4, 5]
```

`chain` 只展开只包含可迭代的可迭代：，像是 `[1, 2, [3]]` 这种是不行的，抛出 `TypeError`。

### `traverse` —— 递归展开可迭代对象

对于扁平化可迭代非常有用。

示例：
```python
>>> list([1, 2, [3]] | traverse)
[1, 2, 3]
>>> list([[1, 2], [[[3], [[4]]], [5]]] | traverse)
[1, 2, 3, 4, 5]
```

### `dedup` 与 `uniq` —— 去重函数

示例：
```python
>>> list([1, 1, 2, 2, 3, 3, 1, 2, 3] | dedup)
[1, 2, 3]
>>> list([1, 1, 2, 2, 3, 3, 1, 2, 3] | dedup(key=lambda n: n % 2))
[1, 2]
```

`uniq` 与 `dedup` 类似，但只对连续值进行重复数据删除。

```python
>>> list([1, 1, 2, 2, 3, 3, 1, 2, 3] | uniq)
[1, 2, 3, 1, 2, 3]
>>> list([1, 1, 2, 2, 3, 3, 1, 2, 3] | uniq(key=lambda n: n % 2))
[1, 2, 3, 2, 3]
```

这里只举例几个比较常用的函数，欲知更多请参阅[文档](https://github.com/JulienPalard/Pipe#existing-pipes-in-this-module)。

下一篇文章带大家扒一扒这个库的源码，拜拜~