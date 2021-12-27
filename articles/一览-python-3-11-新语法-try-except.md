---
theme: qklhk-chocolate
---
官方文档（[What’s New In Python 3.11](https://docs.python.org/3.11/whatsnew/3.11.html)）预告将会在下一个 Python 的正式版本中引入“异常组（exception group）”的概念，并添加与其对应的  `except*` 语法扩展：

![官方预告](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/a02f83bc8c554833ae53959d0af163c7~tplv-k3u1fbpfcp-watermark.image?)

目前发布的 Python 3.11.0a3 仍未实现此功能，下一个 alpha 版本预计会在 2022 年 1 月 3 日发布。

![Python 发布周期](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7c34c3fea40442c9bbca43cefaedc258~tplv-k3u1fbpfcp-zoom-1.image)

## 异常组

这个概念的提出是为了让程序在一个时间内**同时抛出/处理多个异常**。

### `BaseExceptionGroup` 和 `ExceptionGroup`

这两种新的异常类型能组合几个不相关的异常并一起传播。简单来说，抛出一个异常组就等同于同时抛出 n 个异常。举个例子：

```python
raise ExceptionGroup('bad param', [ValueError('bad value'), TypeError('bad type')])
```

错误信息展示如下：

```python
  | ExceptionGroup
  +-+---------------- 1 ----------------
    | Exception Group Traceback (most recent call last):
    |   File "<stdin>", line 1, in <module>
    | ExceptionGroup: bad param
    +-+---------------- 1 ----------------
      | ValueError: bad value
      +------------------------------------
      | TypeError: bad type
      +------------------------------------
```

`ExceptionGroup` 的第一个参数为信息字符串 `message`，第二个参数为异常序列（`list`、`tuple` 等）。当然多层嵌套的序列也是行的：

```python
raise ExceptionGroup("one", [
  TypeError(1),
  ExceptionGroup("two", [TypeError(2), ValueError(3)]),
  ExceptionGroup("three", [OSError(4)]),
])
```

`BaseExceptionGroup` 继承自 `BaseException` 类，`ExceptionGroup` 继承自 `Exception` 类。

![`Exception` 关系图](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1cace888976340b1a3daba86b07284f0~tplv-k3u1fbpfcp-watermark.image?)

### `ExceptionGroup.subgroup` 和 `ExceptionGroup.split` 方法

新增的两个方法。`subgroup(condition)` 可以根据 `condition` 函数的返回值递归地筛选异常组里的异常/异常组。

举个例子：

```python
eg = ExceptionGroup("one", [
  TypeError(1),
  ExceptionGroup("two", [
      TypeError(2),
      ValueError(3)
  ]),
  ExceptionGroup("three", [
      OSError(4)
  ])
])
```

执行 `eg.subgroup(lambda e: isinstance(e, TypeError))` 将得到：

```python
ExceptionGroup("one", [
    TypeError(1),
    ExceptionGroup("two", [
        TypeError(2)
    ])
])
```

由 `subgroup` 类似的方法还有 `split(condtion)`。`split` 返回一个元组，第一个值为匹配的结果，第二个值为不匹配的结果。

还是以上面的 `eg` 为例，`eg.split(lambda e: isinstance(e, TypeError))` 将得到：

```python
(
    ExceptionGroup("one", [
        TypeError(1),
        ExceptionGroup("two", [
            TypeError(2)
        ])
    ]),
    ExceptionGroup("one", [
        ExceptionGroup("two", [
            ValueError(3)
        ]),
        ExceptionGroup("three", [
            OSError(4)
        ])
    ])
)
```

### `except*`

**一个异常组能触发多个 `except*` 子句。**

对于组中所有匹配的异常，每个 `except*` 子句最多执行一次。每个异常要么由第一个匹配其类型的子句处理，要么在最后重新抛出。

为了能更清楚的理解 `try-except*` 背后的整个执行过程，我将以下面这段代码作为例子：

```python
try:
    raise ExceptionGroup('msg', [FooError(1), FooError(2), BazError()])
except* SpamError:
    ...
except* FooError:
    ...
```

我们在 `try` 子句中抛出了一个异常组：

```python
ExceptionGroup("msg", [FooError(1), FooError(2), BazError()])
```

在第一个`except*` 子句中，Python 解释器将 `unhandled` 初始化为这个异常组，并调用 `unhandled.split(SpamError)`，得到结果：

```python
(
    None,  # 匹配的异常
    ExceptionGroup("msg", [FooError(1), FooError(2), BazError()])  # 其他异常
)
```

第一个值值为 `None`，表示没有匹配，这个 `except*` 块不执行。接着来到第二个 `except*` 子句，程序执行 `unhandled.split(FooError)`，返回：

```python
(
    ExceptionGroup('msg', [FooError(1), FooError(2)]),  # 匹配的异常
    ExceptionGroup('msg', [BazError()])  # 其他异常
)
```

第一个值不为 `None`，执行这个 `except*` 块。`ExceptionGroup('msg', [BazError()])` 赋值给 `unhandled`。

重复整个流程直至结束，如果最后 `unhandled` 的值不为 `None`，则重新抛出异常并打印错误信息。

### `except` 和 `except*` 的可组合性

这个混用 `except` 和 `except*` 的概念大致上是为了让一个 `except* T:` **只**处理异常组中的 `T` 异常，再用一个 `except T:` 来处理不在异常组里的 `T` 异常（简称裸异常）。这个想法被官方拒绝了，认为这种语法没有增加有用语义，反而提高了复杂性。

这种方式在实践中意义不大，但如果需要，则可以使用嵌套的 `try-except` 块来实现相同的结果：

```python
try:
    try:
        ...
    except SomeError:
        # 处理裸异常
except* SomeError:
    # 处理异常组
```

此外，`except` 能捕获 `BaseExceptionGroup` 和 `ExceptionGroup`，但 `except*` 不能（这个语法是模糊的，被禁止了）。

```python
except ValueError:  // OK, 捕获裸异常
except ExceptionGroup:  // OK, 捕获异常组
except* ValueError:  // OK, 捕获裸异常 & 异常组
except* ExceptionGroup: // 错误！
except*: // 错误！
```

`except*` 捕获的裸异常会当作异常组处理：

```python
try:
    raise BlockingIOError
except* OSError as e:
    print(repr(e))
```

```python
ExceptionGroup("", [BlockingIOError()])
```

### 为什么不直接拓展 `except` 的功能，而是引入了一种新的语法？

原因很简单：版本兼容性问题。

1. 捕获的类型不同。

    假如我们之前有这样的一段代码：

    ```python
    try:
        ...
    except OSError as err:
        if err.errno != ENOENT:
            raise
    ```

    如果 `except` 的功能被拓展了，`err` 的类型将会是 `ExceptionGroup`，那么访问 `err.errno` 属性将会导致错误。
    
2. 多个 `except` 子句只执行一次，但多个 `except*` 子句可执行多次。

    这是一个潜在的破坏性变化，因为目前它打破了我们对 `except` 只执行一次的认知。如果之前版本的 `except` 子句中包含非幂等操作（执行第一次和第二次结果不同的操作，例如释放资源）将会出现灾难性的问题。

## 新增 `__note__` 属性

`BaseException` 新增了一个可变属性 `__note__`（默认为 `None`）。这个属性可以作为异常的注释，会连同错误信息一起打印出来。

至于用途嘛，就捕获异常后添加信息比较方便，总比用 `print` 来得好吧 (手动狗头)。

我装了 Python 3.11.0a3（[下载链接](https://www.python.org/downloads/release/python-3110a3/)）试试：

```python
try:
    1 / 0
except Exception as e:
    e.__note__ = "Custom message"
    raise
```

```python
Traceback (most recent call last):
  File "<pyshell#12>", line 2, in <module>
    1 / 0
ZeroDivisionError: division by zero
Custom message
```

## 参考资料

1. https://docs.python.org/3.11/whatsnew/3.11.html
2. https://www.python.org/dev/peps/pep-0654
3. https://bugs.python.org/issue45607
4. https://www.python.org/dev/peps/pep-0678
