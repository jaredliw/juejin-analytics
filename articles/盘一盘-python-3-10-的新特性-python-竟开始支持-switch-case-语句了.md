---
theme: cyanosis
highlight: an-old-hope
---
小知识，大挑战！本文正在参与「[程序员必备小知识](https://juejin.cn/post/7008476801634680869 "https://juejin.cn/post/7008476801634680869")」创作活动。本文已参与 [「掘力星计划」](https://juejin.cn/post/7012210233804079141 "https://juejin.cn/post/7012210233804079141")，赢取创作大礼包，挑战创作激励金。

就在几天前，Python 官方发布了 `Python 3.10.0` 正式版本（4/10/2021）和 `Python 3.11.0a1` alpha 测试版（5/10/2021）。

大家好，我是披着狼皮的羊。今天向大家介绍介绍 Python 3.10 中的新特性。

## 更直观的错误信息
### 标识错误的小箭头
在新版本的 Python 中，指示小箭头能更准确的定位到错误的位置了：

| Python 3.9 | Python 3.10 |
| --- | --- |
| <pre lang="python">>>> foo(x, z for z in range(10), t, w)<br/>  File "\<stdin>", line 1<br/>    foo(x, z for z in range(10), t, w)<br/>           ^<br/>SyntaxError: Generator expression must be parenthesized</pre>| <pre lang="python">>>> foo(x, z for z in range(10), t, w)<br/>  File "\<stdin>", line 1<br/>    foo(x, z for z in range(10), t, w)<br/>           ^^^^^^^^^^^^^^^^^^^^<br/>SyntaxError: Generator expression must be parenthesized</pre> |

### `SyntaxError`
SyntaxError 也能根据问题原因给出更详细的错误信息了，不再只是 `invalid syntax`。

| Python 3.9 | Python 3.10 |
| --- | --- |
| <pre lang="python">>>> if True<br/>  File "\<stdin>", line 1<br/>    if True<br/>           ^<br/>SyntaxError: invalid syntax</pre>| <pre lang="python">>>> if True<br/>  File "\<stdin>", line 1<br/>    if True<br/>           ^<br/>SyntaxError: expected ':'</pre> |
| <pre lang="python">>>> while a = b:<br/>  File "\<stdin>", line 1<br/>    while a = b:<br/>            ^<br/>SyntaxError: invalid syntax</pre> | <pre lang="python">>>> while a = b:<br/>  File "\<stdin>", line 1<br/>    while a = b:<br/>          ^^^^^<br/>SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?</pre> |
| <pre lang="python">>>> {x, y for x, y in zip('abcd', '1234')}<br/>  File "\<stdin>", line 1<br/>    {x, y for x, y in zip('abcd', '1234')}<br/>          ^<br/>SyntaxError: invalid syntax</pre>| <pre lang="python">>>> {x, y for x, y in zip('abcd', '1234')}<br/>  File "\<stdin>", line 1<br/>    {x, y for x, y in zip('abcd', '1234')}<br/>     ^^^^<br/>SyntaxError: did you forget parentheses around the comprehension target?</pre> |

### `NameError` 和 `AttributeError`
当找不到属性/变量时，`PyErr_Display()` 将打印类似属性/变量名称的建议：

| Python 3.9 | Python 3.10 |
| --- | --- |
| <pre lang="python">>>> import collections<br/>>>> collections.nametaple<br/>Traceback (most recent call last):<br/>  File "\<stdin>", line 1, in \<module><br/>  File "\<LONG_LONG_PATH>\Python39\lib\collections\\_\_init__.py", line 68, in \_\_getattr__<br/>    raise AttributeError(f'module {\_\_name__!r} has no attribute {name!r}')<br/>AttributeError: module 'collections' has no attribute 'nametaple'<br/></pre>| <pre lang="python">>>> import collections<br/>>>> collections.nametaple<br/>Traceback (most recent call last):<br/>  File "\<stdin>", line 1, in \<module><br/>AttributeError: module 'collections' has no attribute 'nametaple'. Did you mean: 'namedtuple'?<br/></pre> |

对于面向 Notepad 编程的程序员们，这特性还是非常有用的（只要单词拼写得不太离谱）。

> #### 后记：
>
> 看看上方错误信息中的：
> ```python
> f'module {__name__!r} has no attribute {name!r}
> ```
> 用了这么久的 f-string，但 `!r` 我还是第一次见过，上网查了查，原来它表示的是 `repr(__name__)`。
>
> 这算是 Python 的一个语法糖吧，学废了（没啥用，可读性又不高，适合装装 B）。
>
> 更多 f-string 的小技巧，请见这篇 [Medium 文章](https://jerrynsh.com/3-useful-python-f-string-tricks-you-probably-dont-know/)。

## 关于类型提示（Type Hints）的新特性
要想标注一个参数可以是 `int` 或 `float` 的话，之前我们是这么做的：
```python
from typing import Union

def add_one(num: Union[int, float]) -> Union[int, float]:
    return num + 1
```
Python 3.10 引进了一个新的类型并集运算符（type union operator），语法为 `X | Y`：
```python
def add_one(num: int | float) -> int | float:
    return num + 1
```
这样的写法更加清晰明了，预计在未来的某个版本 `typing.Union` 就会荣休了 ……

这语法也适用于 `isinstace()` 和 `issubclass()` 中：
```python
>>> isinstance(1, int | str)
True
```

## 结构化模式匹配 —— match-case 语句
大更新！Python 支持 ~~switch-case~~ match-case 啦！

```python
match subject:
    case <pattern_1>:
        <action_1>
    case <pattern_2>:
        <action_2>
    case <pattern_3>:
        <action_3>
    case _:
        <action_wildcard>
```

`match` 语句将 `subject` 表达式 与 `case` 语句中的每个模式（pattern）从上到下进行比较，直到找到匹配的模式。若找不到匹配的表达式，则匹配 `_` 通配符（wildcard）（如有），实际上它就是其它语言中的 `default` 关键字。

示例：
```python
def http_error(status):
    match status:
        case 400:
            print("Bad request")
        case 404:
            print("Not found")
        case 418:
            print("I'm a teapot")
        case _:
            print("Something's wrong with the internet")
```

在我看来，相较于其它语言中的 switch-case，Python 的 match-case 有几个特点：
1. 无需 `break` 关键字

    由于 Python 在匹配成功后就停止了，因此我们不能（这将会抛出 `SyntaxError`）也不用在每个 case 代码块结尾写 `break`。这是不是代表我们不能像其它语言一样堆叠多个 `case`？
    
    ```java
    switch(status) {
        case 401:
        case 403:
        case 404:
            System.out.println("Not allowed");
            break;
        default:
            System.out.println("Something's wrong with the internet");
    }
    ```
   
   其实不然。我们能用 `|` 来结合多个模式（这是模式匹配中唯一支持的运算符）：
   
    ```python
    match status:
        case 401 | 403 | 404:
            print("Not allowed")
        case _:
            print("Something's wrong with the internet")
    }
    ```
    简单明了，非常的 Pythonic！

2. 多种模式

    支持的模式有以下这几种：
    1. 字面常数（literal）模式
       
        如：`int`、`float`、`string`、`bool` 和 `None`，但 f-string 不行，毕竟它不是字面常数。

        注意，我们是**不能把变量中的值当作匹配模式**的：
        
        ```python
        FULL_SCORE = 100
        my_score = 20
        match my_score:
            case FULL_SCORE:
                print("Congratulations!")
        print(FULL_SCORE)  # FULL_SCORE 的值被更改为 20
        ```
        
        match-case 会把它当作捕获模式（下面会提到），并将 `my_score` 赋值给 `FULL_SCORE`。
        
    2. 捕获模式，作为匹配表达式的赋值目标，例：
    
        ```python
        match greeting:
            case "":
                print("Hello!")
            case name:
                print(f"Hi {name}!")
        if name == "Santa":      # <-- 可能抛出 UnboundLocalError
            ...                  # 当 greeting 不为空时没问题
        ```
    
        在匹配每个 `case` 子句时，一个名称最多只能绑定一次，有两个具有重合名称的捕获模式是错误的：
        
        ```python
        match data:
            case [x, x]:  # SyntaxError: multiple assignments to name 'x' in pattern
                ...
        ```
        
    3. 通配符模式
       
       `_` 在这里不作为变量名称，而是一种特殊的模式。它始终匹配但从不绑定值：
       
       ```python
       match data:
           case [_, _]:
               print("Some pair")
               print(_)  # NameError: name '_' is not defined
       ```
       
       注意：如果你上方使用了名叫 `_` 的变量，这里不会抛出错误，但得到的值是你之前所定下的值，和这里毫无关系，别搞混了~

    4. 常量值模式
       
       属性和枚举类（`enum.Enum`）也能作为模式，这里就不多做解释了。
      
    5. 序列模式 和
    6. 映射模式
       
       `list`、`tuple`、`dict` 等都能作为模式，并且能配合 `*` 或 `**` 和通配符使用，像是：
        - `[*_]` 匹配任意长度的 `list`;
        - `(_, _, *_)` 匹配长度至少为 2 的 `tuple`。
    
    6. 类模式
    
       废话不多说，例子如下：
       
        ```python
        class Point:
            x: int
            y: int

        def location(point):
            match point:
                case Point(x=0, y=0):
                    print("Origin is the point's location.")
                case Point(x=0, y=y):
                    print(f"Y={y} and the point is on the y-axis.")
                case Point(x=x, y=0):
                    print(f"X={x} and the point is on the x-axis.")
                case Point():
                    print("The point is located somewhere else on the plane.")
                case _:
                    print("Not a point")
        ```
        
        这个模式也可以和通配符配合使用，举例来说：
        - `Sandwich(cheese=_)` 检查匹配的 `Sandwich` 对象是否具有属性 `cheese`。

3. `case` 块中的 `if` 子句

   我们可以在模式中添加一个 `if` 子句，称为 guard（守卫）。即使模式匹配，如果 guard 为 `False`，`match` 将继续尝试匹配下一个 `case` 块。
   
   ```python
    match point:
        case Point(x, y) if x == y:
            print(f"The point is located on the diagonal Y=X at {x}.")
        case Point(x, y):
            print(f"Point is not on the diagonal.")
   ```

## 新增/优化的函数与模块
### 新增 `int.bit_count`
`int` 中的新方法，返回给定整数的二进制展开式中 1 的数量。示例：
```python
>>> n = 19
>>> bin(n)
'0b10011'
>>> n.bit_count()
3
>>> (-n).bit_count()
3
```

### `zip()` 内建函数新增可选参数 `strict`
`strict` 参数（预设值为 `False`）用于要求 `zip()` 函数检查 iterables 的长度是否相同，如果它们不相同，则抛出 `ValueError`：
```python
>>> list(zip(range(3), ['fee', 'fi', 'fo', 'fum'], strict=True))
Traceback (most recent call last):
  ...
ValueError: zip() argument 2 is longer than argument 1
```

### 新增内建函数 `aiter()` 和 `anext()`
与 `iter()` 和 `next()`  对应，用于异步编程。`aiter()` 返回异步的迭代器，等同于调用 `x.__aiter__()`。当 await 时，`anext()` 调用 `__anext__()`，返回异步迭代器的下一项。异步迭代器耗尽时抛出 `StopAsyncIteration`。

### 【Python 3.11】新增 `math.cbrt`
与 `math.sqrt` 类似，返回 `x` 的立方根。该方法会映射到 C 语言标准库中的 `double cbrt(double arg);`。

也许你会问，**`x ** (1/3)` 就能解决的问题，这函数岂不是可有可无？**

其实答案很简单 —— **防坑**。

如果让你实现这个函数你多半会这么做：
```python
def cbrt(x):
    return x ** (1/3)
```
但当参数 `x` 小于 0 的时候，问题就出现了：
```python
>>> cbrt(-27)  # 返回结果应该是: -3
(1.5000000000000004+2.598076211353316j)
```
要想正确地返回结果，应该这么写：
```python
def cbrt(x):
    if x < 0:
        return -(-x) ** (1/3)
    else:
        return x ** (1/3)
```

这么细致的东西，相信大家也不会注意。看不见，找不着的 bug 油然而生。关于这个东西，Python 的贡献者 —— [Mark Dickinson 是这么说的](https://bugs.python.org/issue44357)：

> Of course, even with `math.cbrt` in the standard library people will still fall into the `x**(1/3)` trap, but at least we then have a decent replacement to point them to.

此外，`x ** (1/3)` 也可能会有精度上的问题。至于速度的话，暂时没看到一个答案，但我猜想 `math.cbrt` 肯定会快些，毕竟少了运算符重载的时间。当然，现在还言之过早，得等 Python 3.11 发布后再测试才有个定论。

### 【Python 3.11】移除 `@asyncio.coroutine` 装饰器
在 Python 3.5 有了 `async def` 这个新语法，`@asyncio.coroutine` 装饰器就不需要了。该函数自 Python 3.8 起已被弃用，原计划在 Python 3.10 中删除该函数。

官方文档上还有很多新特性就不一一列举了，有兴趣的小伙伴们可到[官网](https://docs.python.org/3.10/whatsnew/3.10.html)看看。

就这样，拜了个拜。
