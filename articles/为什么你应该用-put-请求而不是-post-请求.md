这是我参与 11 月更文挑战的第 7 天，活动详情查看：[2021最后一次更文挑战](https://juejin.cn/post/7023643374569816095/)。

> - 原文地址：[Why You Should Use a PUT Request Instead of a POST request](https://betterprogramming.pub/why-you-should-use-a-put-request-instead-of-a-post-request-13b593b6e67c)
> - 原文作者：[Dieter Jordens](https://dieterjordens.medium.com/)
> - 译文出自：[掘金翻译计划](https://juejin.cn/translate)

我收到过好几次这样的问题：为什么要用 PUT 请求而不是 POST 请求？

阅读这篇文章后你就会明白为什么了。你将能在 Python 中使用 FastAPI 实现 PUT 方法，并学习如何正确的测试它。

## PUT 请求和 POST 请求的差异

让我们从解释 PUT 请求的关键特征开始：**幂等性**。

如果您多次调用 PUT 请求，则结果不变。 因此，假设你创建了一个资源：一本书。如果你调用该方法两次，结果仍是相同的。更准确地说，在数据库中一本书只存在一次。每本书都是唯一的。

一个 POST 请求有些不同。如果你创建了一本书，然后再创建同一本书，你将拥有两本书。换句话说，第二次请求时你将会得到不同的结果。

两种方法各有千秋，但 PUT 方法在防止副作用方面非常好用。

为了给让你有个更清晰的概念，让我描述一个场景：Juliette 想购买三明治，她点击一个按钮。因为网店的响应有点慢，她再次按下了同一个按钮。同一个请求两次到达服务器。因为你已经使用 PUT 请求实现了该方法，所以它在第二次访问服务器时没有造成任何的影响。Juliette 不必吃两顿饭，她也省下了一笔钱。很棒，对吧？

在许多情况下，PUT 请求非常适合用于防止不必要的更新。

**备注**：注意，即使你使用 PUT 方法，你仍有可能违反幂等性。如果你用和 POST 方法一样的方式来实现 PUT 方法，两者之间将没有任何区别。这违反了 PUT 的原则。作为一个 API 开发人员，你有责任创建好一个有效的 PUT 请求。

## 如何创建 PUT 请求

首先，搭建你的 Python 环境。为此，你需要一些库：FastAPI、uvicorn、pydantic 和 requests。你可以使用任意的工具进行安装 —— 我个人最喜欢的是使用虚拟环境。

在本文中，您将从头开始构建 PUT 请求。我们将从一个空书集开始，并创建一本本的新书。我们在本教程中使用的数据类型非常简单：

```python
class Book:
    isbn: int
    title: str
```

我们尽量把事情变得简单，此时就不用数据库了。在更新数据方面，字典非常优秀，我们将使用它来代替数据库。

你的 PUT 请求将会创造一本新书。如果这本书不存在，它将在字典里创建一个新的。如果这本书存在，它将替换原有的书。 PUT 请求允许我们一次更新一整个对象。

在 FastAPI 中，代码结构长这样（这取决于你的底层的数据结构）：

```python
import fastapi
import uvicorn

from book import Book


app = fastapi.FastAPI()
books: dict[int, Book] = {}

@app.put("/books/")
def create_or_update_book(book: Book) -> Book:
    books[book.isbn] = book
```

现在，让我们回顾一下这里发生了什么。如果书本已经存在，我们替代原有的书。如果书本不存在，执行后字典就会多出一本书。最后，这个方法将返回新增至字典中的 `Book` 对象。

很棒吧？

PUT 方法与 POST 方法的主要区别在于更新相同的资源时的处理方式。如果你想用 POST 方法做同样的更新，当该键已经存在于字典中时，你应该抛出一个异常。

如果你的数据结构允许重复的值，则 POST 方法不会抛出异常。每次调用 POST 方法时，你都会创建一本新书。这在某些情况下也是合理的，例如在卖书的时候。

## 测试 PUT 请求

FastAPI 让编写单元测试和集成测试的工作变得简单。开始一个测试总是很困难，尤其是对于较新的框架。但随着你对 FastAPI 越来越熟悉，你也可以完美地完成 TDD。

第一个测试往往是最重要的一个测试。当你创建一本不存在的书时，你将会在你的收藏中得到一本新书。代码如下：

```python
@mock.patch('main.books', {})
def test_givenBook_whenCreateOrUpdateBook_thenBookIsAddedToCollection(self) -> None:
    expected_book = book_clean_code
    actual_book = create_or_update_book(book_clean_code)
    
    self.assertEqual(expected_book, actual_book)
```

因为我们用的是字典，我们不能允许一个元素出现两次。这就意味着为这种情况写一个测试是没有意义的。这里还有一种情况需要考虑。如果您更新了一本原有的书，你最终应该得到一本新书，如下所示：

```python
@mock.patch('main.books', {9780132350884: book_clean_code})
def test_givenUpdatedBook_whenCreateOrUpdateBook_thenBookIsUpdated(self) -> None:
    expected_book = Book(isbn=9780132350884, title='Cleaner Code')
    actual_book = create_or_update_book(expected_book)
    
    self.assertEqual(expected_book, actual_book)
```

最后，我们也可以编写集成测试。集成测试最重要的部分是看看我们是否得到了正确的 `200 OK` 响应。此测试与使用 Postman 调用我们的 API 相同，但更好的是你能将此类测试自动化。代码如下：

```python
class TestIntegrationMain(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    @mock.patch('main.books', {})
    def test_integration_givenValidBook_whenCreateOrUpdateBook_thenReturnCreatedBook(self) -> None:
        valid_book = {
            'isbn': 9780132350884,
            'title': 'Clean Code: A Handbook of Agile Software Craftsmanship'
        }
        response = self.client.put('/books/', json=valid_book)

        self.assertEqual(200, response.status_code)
        self.assertEqual(valid_book, response.json())
```

## 总结

阅读这篇文章后，你能看到 PUT 方法创建了一个稳定的 API。现在你应该明白什么是幂等性了，而且我相信你也能自己实现你的 PUT 方法。

FastAPI 让我们能简单地创建 PUT 请求，也让测试变得非常容易。从简单性这方面来说，这个框架很难被其他框架打败。什么？你还想继续学习 FastAPI？我之前关于 [GET](https://medium.com/p/ecdc794b0cf)、[POST](https://medium.com/p/3dbd017dd998) 和 [DELETE](https://medium.com/p/b4577f9bcb77) 方法的文章可能对你所帮助，去看看吧~

感谢你阅读这篇文章！