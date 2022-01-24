---
theme: healer-readable
highlight: mono-blue
---
这是我参与 2022 首次更文挑战的第 2 天，活动详情查看：[2022首次更文挑战](https://juejin.cn/post/7052884569032392740 "https://juejin.cn/post/7052884569032392740")。

## `lstrip` 源码

（为了能使初学者更容易地理解背后的原理，本文已对有关 C 语言的内容进行了大量的简化，一切还得以源码和文档为准。）

带参的 `(l/r)strip` 方法对应的底层源码是 `do_xstrip` 函数，位于 `Objects/stringobject.c` 文件中。

这里还是以标题的那行代码为例，给大家简单地说明一下这个函数：

```c
char *s = PyString_AS_STRING(self);
Py_ssize_t len = PyString_GET_SIZE(self);
char *sep = PyString_AS_STRING(sepobj);
Py_ssize_t seplen = PyString_GET_SIZE(sepobj);
```

函数的头 4 行获取了字符串和 `(l/r)strip` 参数的内容和长度，分别为 `s`、`len`、`sep` 和 `seplen`。

准确的来说，`s` 和 `sep` 为 C 指针，指向第一个字符的内存地址值。字符串在 C 语言中表现为**连续的字符数组**，而 `char` 类型的大小为 1 个字节。换句话说，`s` 指向第 0 个字符，`s + 1` 指向第 1 个字符，以此类推。

```c
Py_ssize_t i, j;

i = 0;
if (striptype != RIGHTSTRIP) {
    while (i < len && memchr(sep, Py_CHARMASK(s[i]), seplen)) {
        i++;
    }
}

j = len;
if (striptype != LEFTSTRIP) {
    do {
        j--;
    } while (j >= i && memchr(sep, Py_CHARMASK(s[j]), seplen));
    j++;
}
```

这里定义了两个相反方向的指针 `i` 和 `j` 进行扫描。`while` 中用到了 C 标准库的 `memchar` 函数，这里值得提一下：

> `memchar` 有 3 个参数：
> 1. `ptr` —— 指向执行搜索的内存块的指针；
> 2. `value` —— 要定位的值。该值作为 `int` 传递，但在执行逐字节的搜索时，函数会将该值当作 `unsigned char` 类型。（上方 `Py_CHARMASK` 做的就是将 $[-128, 127]$ 或 $[0, 255]$ 范围内的字符或整数强转为无符号字符类型。）
> 3. `num` —— 搜索的字节长度。

当 `i < len` 且索引 `i` 对应的字符存在于 `sep` 中时，我们将 `i` 自增 1；`i` 将作为之后返回的字符串的起始位置。

由于我们讨论的是 `lstrip`，上方代码段中的第二个 `if` 我就不多做说明了，原理基本一样。

```c
if (i == 0 && j == len && PyString_CheckExact(self)) {
    Py_INCREF(self);
    return (PyObject*)self;
}
else
    return PyString_FromStringAndSize(s+i, j-i);
```

最后来到了返回结果的阶段；如果字符串没有变动，则返回其自身，即 `self`。在返回之前， `PY_INCREF` 函数增加了 `self` 的引用计数，避免该对象被垃圾回收。

如果字符串有变动，则调用 `PyString_FromStringAndSize` 创建一个新的字符串并返回。该函数的第一个参数为新字符串（也就是起始字符的地址值），第二个参数则是字符串的字节长度。

### 完整源码

```c
Py_LOCAL_INLINE(PyObject *)
do_xstrip(PyStringObject *self, int striptype, PyObject *sepobj)
{
    char *s = PyString_AS_STRING(self);
    Py_ssize_t len = PyString_GET_SIZE(self);
    char *sep = PyString_AS_STRING(sepobj);
    Py_ssize_t seplen = PyString_GET_SIZE(sepobj);
    Py_ssize_t i, j;

    i = 0;
    if (striptype != RIGHTSTRIP) {
        while (i < len && memchr(sep, Py_CHARMASK(s[i]), seplen)) {
            i++;
        }
    }

    j = len;
    if (striptype != LEFTSTRIP) {
        do {
            j--;
        } while (j >= i && memchr(sep, Py_CHARMASK(s[j]), seplen));
        j++;
    }

    if (i == 0 && j == len && PyString_CheckExact(self)) {
        Py_INCREF(self);
        return (PyObject*)self;
    }
    else
        return PyString_FromStringAndSize(s+i, j-i);
}
```

## 文档怎么说？

> lstrip(self, chars=None, /) \
> Return a copy of the string with leading whitespace removed.
>
> If chars is given and not None, remove characters in chars instead.

通过 `help(str.lstrip)`，我们可以得知 `chars` 参数是一个字符串，指定**要删除的字符集**。简单来说，`lstrip` 将从左到右遍历字符串，移除存在于 `chars` 中的字符，直到不匹配为止，最后返回剩余的字符串。

## PEP 616 —— 删除前缀和后缀的字符串方法

由于 `(l/r)strip` 经常导致初学者混淆（在 StackOverflow、Bug Tracker、Python-Ideas 等等网站上都有许多人提出相关的问题；好多人都认为是 Python 的 bug），于是便有了 PEP 616。

该提案建议添加两个方法来改善这个问题：`removeprefix` 和 `removesuffix`。在此之前，去除前缀/后缀的功能是需要我们自己实现的。

当 `type(self) is type(prefix) is type(suffix) is str` 时，这两个方法的行为如下：

```python
def removeprefix(self: str, prefix: str, /) -> str:
    if self.startswith(prefix):
        return self[len(prefix):]
    else:
        return self[:]
```

```python
def removesuffix(self: str, suffix: str, /) -> str:
    # suffix='' should not call self[:-0].
    if suffix and self.endswith(suffix):
        return self[:-len(suffix)]
    else:
        return self[:]
```

（概念性代码，底层当然是使用 C 语言实现）

### 好处

1. 降低代码脆弱性

   Python 使用者不必手动计算文字的长度、偏移量等。
   
2. 更高效

   该代码不需要调用内置的 `len` 函数，也不需要调用更昂贵的 `str.replace` 方法。
   
3. 更具描述性

   与传统的字符串切片方法相比，这些方法提供了更高级的 API，提高了代码的可读性。

该提案已在 Python 3.9 版本中实现，你可以在 `str`、`bytes`、`bytearray` 和 `collections.UserString` 类中看到以上的两个方法。

## 总结

`str.(l/r)strip` 不能很好地移除前缀/后缀，别再用它在代码里下毒啦！

> 相关文章：
> 
> - [一览 Python 3.11 新语法：try-except*](https://juejin.cn/post/7046321690061570085)
> - [盘一盘 Python 3.10 的新特性：Python 竟开始支持 switch-case 语句了？！](https://juejin.cn/post/7015982514430804005)

## 参考资料

1. https://svn.python.org/projects/python/trunk/Objects/stringobject.c
2. https://docs.python.org/3/extending/extending.html#ownership-rules
3. https://docs.python.org/3/c-api/refcounting.html#c.Py_INCREF
4. https://docs.python.org/3/c-api/intro.html#c.Py_CHARMASK
5. https://docs.python.org/3/glossary.html#term-borrowed-reference
6. https://docs.python.org/3/glossary.html#term-strong-reference
7. https://www.python.org/dev/peps/pep-0616/