这是我参与 11 月更文挑战的第 6 天，活动详情查看：[2021最后一次更文挑战](https://juejin.cn/post/7023643374569816095/)。

> - 原文地址：[Using Class Decorators in Python](https://towardsdatascience.com/using-class-decorators-in-python-2807ef52d273)
> - 原文作者：[Stephen Fordham](https://medium.com/@stephenfordham)
> - 译文出自：[掘金翻译计划](https://juejin.cn/translate)

> **在 Python 中使用类装饰器的示例与指南**

## 装饰器类

在 Python 中，装饰器可以是函数亦或是类。在这两种情况下，装饰器都能为现有的函数添加功能。当我们用一个类装饰函数时，**该函数就会变成类的实例**。我们可以通过在装饰器类中定义方法来为函数添加功能，这一切都能在不修改源代码的情况下实现。

本教程将演示如何使用类来装饰我们 Python 代码中的函数。我将展示两个用例，分别是：使用不接受参数的类装饰函数，以及使用可接受参数的类装饰函数。如果没有传递参数，我们的类将使用默认值。

为了帮助大家理解，我特意地简化了下方的示例。虽然我们可以使用更简单的替代方案来实现类似的结果，但我在本教程中的主要目的是演示如何使用类来装饰函数并扩展它们的功能。

本教程也旨在展示如何使用可接受参数的装饰器类。

## `multiple_together` 函数

`multiple_together` 函数获取两个整数值，将它们相乘并返回结果。让我们考虑这样一个场景，我们希望在不更改其源代码的情况下向该函数添加一些额外的功能。这里，我们想对返回的值进行平方。我们可以使用类装饰器来实现这一点。

如果要以一个类作为函数的装饰器，我们必须在函数定义的上方写上 `@className`（`className` 为类名）。按照惯例，我们的类名将依循驼峰命名法。在类定义中，我们定义了两个方法：`__init__` 构造函数和 `__call__` 方法。

当我们用一个类装饰一个函数时，该函数会自动作为 `__init__` 构造函数的第一个参数。我们将这个函数作为我们对象中的一个属性。如果我们现在将 `multiply_together` 打印出来，我们将会得到一个 `Power` 类的实例。

通过定义 `__call__` 方法，我们可以像之前一样调用 `multply_together` 函数。在这里可以看到我们将 2 乘以 2 并对结果求平方。

`__call__` 方法有两个参数（因为我们原来的 `multiply_together` 函数中有两个参数）。我们将 `self._arg` 设置为被装饰的函数（语法为 `object.attribute`）。我们通过传递两个值调用该函数，并将返回值保存到变量 `retval` 中。最后，我们对 `retval` 求平方并返回。

![img](https://miro.medium.com/max/485/1*RzUJ07s8E1-7L9BD7JOkFw.png)

`Power` 类扩展了原有 `multiply_together` 函数的功能。

此示例的代码如下所示：

```python
class Power(object):
	def __init__(self, arg):
		self._arg = arg

	def __call__(self, a, b):
		retval = self._arg(a, b)
		return retval ** 2


@Power
def multiply_together(a, b):
	return a * b


print(multiply_together)
print(multiply_together(2, 2))
```

## 扩展 `multiply_together` 函数的功能 —— 添加 `memory`

为了扩展上一节中介绍的示例，我们可以为我们的 `Power` 对象腾出存储返回值的空间。我们可以为我们的对象的 `_memory` 属性设置一个空列表，并在每次调用被装饰的函数时将返回值添加到该列表中。最后，我们可以定义一个名为 `memory` 的方法，用于返回存储在 `_memory` 列表中的值。

这样，我们进一步扩展了 `multiply_together` 函数的功能。 这个例子的代码可以在[这里](https://gist.github.com/StephenFordham/5389bc8700477a67a137da62cfc90832)找到。

![img](https://miro.medium.com/max/523/1*Q3b7nGxPlS86PYQhbg3JzA.png)

`_memory` 属性现在为了一个包含所有结果的列表。我们只需调用 `Power` 实例种的 `memory` 方法来检索结果。

## 可以接受参数的类装饰器

为了进一步增加示例的功能，让我们的类装饰器接受参数是再好不过的了。通过这种方式，我们可以自定义 `Power` 类的指数值。此外，如果没有参数传递给类装饰器，则使用默认的指数值。

## 将参数传递给类装饰器

当我们将参数传递给类装饰器时，该参数将会是 `__init__` 构造函数的参数（而**不是被装饰的函数**）。在示例中，我们将整数值 3 作为参数传递给 `Power` 类的构造函数。这个值被保存到类的 `_arg` 属性中。被装饰的函数将作为 `__call__` 方法的唯一参数。

因此，如果传递给 call 方法的参数个数等于 1，也就是被装饰的函数作为参数传递给类了，则 `__call__` 方法的第一个参数将被会是函数。之后，我们可以在 `__call__` 方法中定义一个内部函数，它接受两个参数，`a` 和 `b`。如果传递给 `__call__` 的参数个为 1，则 `__call__` 方法返回 `wrapper` 函数，我们可以通过传递两个值来调用此函数，最后将结果乘以最初作为参数传递给类的整数（存储在属性 `_arg` 中）（请参见下面的示例）。

为了给我们的 `__call__` 方法增加灵活性，我们使用  `*param_arg`。这意味着这个参数可以接受可变数量的参数。`param_arg` 将参数存储在元组中，这能让我们非常方便地检查参数的个数。

为了更好的描述过程，我附上了相应的示例：

![img](https://miro.medium.com/max/700/1*n-lPAKiCEP3alHFHk2vbQA.png)

## 不向类装饰器传递参数时

另一种情况是没有参数传递给类装饰器。在这个情况下，该函数会作为第一个函数传入 `__init__` 构造函数中。当我们调用被装饰的函数时，我们传入两个参数，因此 `__call__` 方法中第一个条件不成立，`else` 语句被执行。这里，默认值 2 被设置为指数。之后，存储在 `_arg` 属性中的函数被调用，返回值存储在变量 `retval` 中。最后，`retval` 乘以默认 `expo` 值并返回。

你可以在[此处](https://gist.github.com/StephenFordham/dc43293bc108cc503699caf4ded60277)以及下方找到两个示例的源代码。

现在两种情况都被满足了 —— 我们有一个可以接受或不接受参数的类装饰器。如果没有参数传递给类装饰器，则它将使用默认值。

![img](https://miro.medium.com/max/700/1*X2xRrLTnBrVsT0-btkjVbg.png)

```python
# 完整示例，附 docstring
class Power(object):
	def __init__(self, arg):
		self._arg = arg

	def __call__(self, *param_arg):
		"""If there are decorator arguments, __call__() is only called once
		as part of the decoration process. You can only give it a single argument,
		which is the function object.
		If there are no decorator arguments, the function
		to be decorated is passed to the constructor.
		"""
		if len(param_arg) == 1:
			def wrapper(a, b):
				retval = param_arg[0](a, b)
				return retval ** self._arg
			return wrapper
		else:
			expo = 2
			retval = self._arg(param_arg[0], param_arg[1])
			return retval ** expo
        
        
# @Power(3)
@Power
def multiply_together(a, b):
	return a * b


print(multiply_together(2, 2))
```

## 总结

上方代码的输出可以通过更简单的方式来实现，但是，本文重点在于介绍如何使用类装饰器，因此我更侧重于使用易于理解的示例。

函数可以用类装饰以扩展其功能。此外，装饰函数的类能接受参数，也可以在没有传递参数的情况下使用默认值。在本文中，我们示范了这两个用例，用于改进原始函数的功能。

