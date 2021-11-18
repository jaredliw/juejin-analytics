---
theme: qklhk-chocolate
---
这是我参与 11 月更文挑战的第 5 天，活动详情查看：[2021最后一次更文挑战](https://juejin.cn/post/7023643374569816095/ "https://juejin.cn/post/7023643374569816095/")。

废话不多说，直接进入主题。不知道什么是 pipe 的小伙伴请到我主页/专栏里找找上一篇文章~

## 源码分析

这里以 `select` 作为例子，源代码如下：

```python
@Pipe
def select(iterable, selector):
    return builtins.map(selector, iterable)
```

`select` 调用 Python 内建 `map`，返回迭代器。`Pipe` 类装饰了 `select`：

```python
class Pipe:
    def __init__(self, function):
        self.function = function
        functools.update_wrapper(self, function)

    def __ror__(self, other):
        return self.function(other)

    def __call__(self, *args, **kwargs):
        return Pipe(lambda x: self.function(x, *args, **kwargs))
```

`Pipe` 是一个类装饰器（class decorator）。初始化时，被装饰的函数（即 `select`）会作为参数传入 `Pipe.__init__`。

### `functools.update_wrapper` 做了什么？

当我们使用 `Pipe` 类包装 `select` 函数时，`select` 的模块级常量（如 `__name__`，`__doc__` 等）将被 `Pipe` 的模块级常量替换。这会造成一定问题，`select` 函数的标识数据被覆盖了，`help(select)` 没办法展示有用的信息，对于使用者非常不友好。

`functools.update_wrapper(wrapper, wrapped)` 能更新 `wrapper` 函数以**使其类似于 `wrapped` 函数**。`wrapped` 的模块级常量将被赋值给 `wrapper` 函数的`__module__`, `__name__`, `__qualname__`, `__annotations__` 和 `__doc__`, `wrapper` 的 `__dict__` 也会一并更新。

### 呼叫函数

当你想要使用 `select` 时：`select(lambda x: x % 2 == 0)`，由于 `select` 已经被包装，则调用运算符 `()` 由 `Pipe.__call__` 重载。通过该方法，你便得到了一个 `Pipe` 对象，这与直接创建一个这样的 `Pipe` 对象等价：

```python
Pipe(lambda x: select(x, lambda x: x % 2 == 0))
```

### pipe 实现 —— `|` 运算符重载

`|` 运算符在 Python 中为按位或运算，由 `__or__`/`__ror__`/`__ior__` 重载。那么这个库必然重写了这个 dunder 方法。

#### `__or__`、`__ror__` 和 `__ior__` 的查询顺序

当你计算 `x | y` 这个表达式时，Python 会先查看 `x` 的类是否实现了 `__or__` 方法。如有，执行 `x.__or__(y)`，反之则查看 `y` 的类是否实现了 `__ror__`。如有，执行 `y.__ror__(x)`。当两个类都没有实现相关方法时，抛出 `TypeError`。

> 这里有一个例外：
>
> 如果右运算元（即 `y`）的类是运算元（即 `x`）类的子类，并且该子类为该运算提供了不同实现，则 `y.__ror__(x)` 会在 `x.__or__(y)` 之前调用。这么设定是为了让子类能覆盖其父类的操作。

对于 `x |= y`，如果 `x` 类实现了 `__ior__` 则该表达式等价于 `x = x.__ior__(y)` (`__ior__` 返回 `self`，`__or__` 返回新的实例），反之则 fallback 到 `x.__add__` 或 `y.__radd__` 中。

> 如果我想只允许我的自定义类和 `list` 做按位或运算，`__or__` 应该怎么写？
> <br><br>
> 对于非 `list` 类的运算元，返回 `NotImplemented` 常量即可。
> ```python
> def __or__(self, other):
>     if not isinstance(other, list):
>         return NotImplemented
>     ...
> ```

`Pipe.__ror__` 重载了 `|` 运算符（但又没完全重载）。由 `Pipe` 装饰的函数只能作为 `|` 的第二个运算元。

## 重点回顾

1. 类也能作为装饰器，`wrapped` 将作为第二个参数传入 `__init__`。
2. `functools.update_wrapper` 能避免 `wrapped` 的模块级常量被 `wrapper` 覆盖。
3. 运算符重载的顺序及例外。
3. `NotImplemented` 用于表示某个操作对该类型的 `other` 没有对应的实现。
