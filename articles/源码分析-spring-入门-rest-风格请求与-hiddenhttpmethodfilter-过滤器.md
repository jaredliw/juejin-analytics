---
theme: hydrogen
highlight: ascetic
---

这是我参与 2022 首次更文挑战的第 4 天，活动详情查看：[2022首次更文挑战](https://juejin.cn/post/7052884569032392740)。

HTML 中的 `form` 表单仅支持 GET 和 POST 请求，而 PUT、DELETE 等其他的请求方法则没法直接通过 HTML 发送。`method` 属性的值只能是 `get`、`post` 或 `dialog`（`dialog` 的作用：如果表单在 `<dialog>` 元素中，提交时关闭对话框），其他值则默认当成 GET 请求发送。

为了能变相解决这个问题，Spring 3.0 中添加了一个过滤器 —— `HiddenHttpMethodFilter`。该过滤器会使用表单中的 `_method` 值来覆盖原本的 HTTP 请求方法（也就是 POST），之后才交由处理器映射器（HandlerMapping）去寻找相对应的 Controller 方法。

```html
<form action="..." method="post">
    <input type="hidden" name="_method" value="put" />
    ...
</form>
```

## ​`doFilterInternal` 方法

`HiddenHTTPMethodFilter` 继承自 `OncePerRequestFilter`，实现了 `doFilterInternal` 这个抽象方法。

```java
protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
    HttpServletRequest requestToUse = request;
    if ("POST".equals(request.getMethod()) && request.getAttribute("javax.servlet.error.exception") == null) {
        String paramValue = request.getParameter(this.methodParam);
        if (StringUtils.hasLength(paramValue)) {
            String method = paramValue.toUpperCase(Locale.ENGLISH);
            if (ALLOWED_METHODS.contains(method)) {
                requestToUse = new HiddenHttpMethodFilter.HttpMethodRequestWrapper(request, method);
            }
        }
    }

    filterChain.doFilter((ServletRequest)requestToUse, response);
}
```

通过上方的几个 `if`，我们能清楚地了解到只有当……

1. 请求方法为 `POST`；
2. `javax.servlet.error.exception` 属性为 `null`（可以暂时不管它，一般情况下都为 `null`）；
3. `methodParam` 的值在 `ALLOW_METHODS` 中（也就是 `PUT`、`DELETE` 和 `PATCH`），不区分大小写；
    ```java
    private static final List<String> ALLOWED_METHODS;
    ...
    static {
        ALLOWED_METHODS = Collections.unmodifiableList(Arrays.asList(HttpMethod.PUT.name(), HttpMethod.DELETE.name(), HttpMethod.PATCH.name()));
    }
    ```

时，请求才会被 `HttpMethodRequestWrapper` 类包装。

> 注：上方的 `StringUtils.haslength` 是一个 Spring 的工具方法，用于保证 `paramValue` 不为 `null`，且至少包含一个非空白字符。

## `HttpMethodRequestWrapper` 包装类

`HiddenHTTPMethodFilter` 内定义了一个私有静态类 —— `HttpMethodRequestWrapper`，重写了 `HttpServletRequestWrapper` 类的 `getMethod` 方法。

原先 `HttpMethodRequestWrapper` 返回的是被包装的 `HttpServletRequest` 请求对象的默认 `getMethod` 方法。

```java
public class HttpServletRequestWrapper extends ServletRequestWrapper implements HttpServletRequest {
    ...
    private HttpServletRequest _getHttpServletRequest() {
        return (HttpServletRequest)super.getRequest();
    }
    ...
    public String getMethod() {
        return this._getHttpServletRequest().getMethod();
    }
    ...
}
```

`HttpMethodRequestWrapper` 源码：

```java
private static class HttpMethodRequestWrapper extends HttpServletRequestWrapper {
    private final String method;

    public HttpMethodRequestWrapper(HttpServletRequest request, String method) {
        super(request);
        this.method = method;
    }

    public String getMethod() {
        return this.method;
    }
}
```

有了上面这个带 `method` 参数的构造器后，`getMethod` 的返回值将固定为初始化时给定的值。简单来说就是这个包装器“另辟蹊径”，直接将 `method` 属性交由上方的 `doFilterInternal` 方法固定为一个值（也就是 `PUT`、`PATCH` 或 `DELETE`）；之后寻找 Controller 时用的也就是这个值。

## 更改 `_method` 参数名

方法参数名可通过 `setMethodParam` 设置。

```java
public void setMethodParam(String methodParam) {
    Assert.hasText(methodParam, "'methodParam' must not be empty");
    this.methodParam = methodParam;
}
```

> 注：`Assert.hasText` 也是一个 Spring 工具方法，源码中调用了 `StringUtils.hasText`（上方提到过），只不过是添加了断言的功能而已。
> 
> ```java
> public static void hasText(@Nullable String text, String message) {
>     if (!StringUtils.hasText(text)) {
>         throw new IllegalArgumentException(message);
>     }
> }
> ```

## 参考资料

1. https://docs.spring.io/spring-framework/docs/3.2.2.RELEASE_to_4.0.0.M1/Spring%20Framework%204.0.0.M1/org/springframework/web/filter/HiddenHttpMethodFilter.html
2. https://blog.csdn.net/geloin/article/details/7444321
3. https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/form
