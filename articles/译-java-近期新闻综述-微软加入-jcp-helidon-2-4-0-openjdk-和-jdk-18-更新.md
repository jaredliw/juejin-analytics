这是我参与 11 月更文挑战的第 9 天，活动详情查看：[2021最后一次更文挑战](https://juejin.cn/post/7023643374569816095/ "https://juejin.cn/post/7023643374569816095/")。

> - 原文地址：[Java News Roundup: Microsoft Joins JCP, Helidon 2.4.0, OpenJDK and JDK 18 Updates](https://www.infoq.com/news/2021/11/java-news-roundup-nov01-2021/)
> - 原文作者：[Michael Redlich](https://www.infoq.cn/profile/416A67CDBAA4DC/publish)
> - 译文出自：[掘金翻译计划](https://juejin.cn/translate)

本周（2021 年 11 月 1 日）的 Java 综述包含 OpenJDK JEP，JDK 18，Helidon 2.4.0，Open Liberty 21.0.0.12-beta，Spring Cloud 和其相关子项目的小数点发布，Quarkus 2.4.1.Final，Hibernate Reactive 1.0.1，WildFly 25.0.1 和 JReleaser 0.8.0 的新闻。

### OpenJDK

在审查结束后，JEP 418，[网络地址解析 SPI](https://openjdk.java.net/jeps/418)，已从 **Proposed to Target** 状态[提升](https://mail.openjdk.java.net/pipermail/jdk-dev/2021-November/006239.html)至 **Targeted** 状态。该 JEP 建议为主机名和地址解析定义一个服务供给接口（SPI），以便 **[`java.net.InetAddress`](https://docs.oracle.com/en/java/javase/16/docs/api/java.base/java/net/InetAddress.html)** 类可以利用默认内置 OpenJDK 解析器以外的解析器。

JEP 421，[弃用与废除对象终止机制](https://openjdk.java.net/jeps/421)，已从 **Draft** 状态[提升](https://mail.openjdk.java.net/pipermail/jdk-dev/2021-November/006200.html)至 **Candidate** 状态。此 JEP 弃用了在 JDK 1.0 中首次引入的对象终止机制，以便在未来的 JDK 版本中移除。虽然对象终止机制旨在避免资源泄漏，但它存在一些严重缺陷，例如不可预期的延迟、不受约束的行为和线程，并且还始终默认启用。

### JDK 18

JDK 18 [早期访问版本（early access release）](https://jdk.java.net/18/)的 [Build 22](https://github.com/openjdk/jdk/releases/tag/jdk-18%2B22) 在上周发布了，内容包括对 Build 21 的[更新](https://github.com/openjdk/jdk/compare/jdk-18%2B21...jdk-18%2B22)，解决了上个版本中的各个 [issue](https://bugs.openjdk.java.net/browse/JDK-8273704?jql=project%20%3D%20JDK%20AND%20fixversion%20%3D%2018%20and%20%22resolved%20in%20build%22%20%3D%20b22%20order%20by%20component%2C%20subcomponent)。更多细节可以在[发行说明](https://jdk.java.net/18/release-notes)中找到。

[JDK 18](https://openjdk.java.net/projects/jdk/18/) 目前的特性集合如下：

-   JEP 400：[默认字符集为UTF-8](https://openjdk.java.net/jeps/400)；
-   JEP 408：[简便 Web 服务器](https://openjdk.java.net/jeps/408)；
-   JEP 413：[Java API 文档中的代码片段](https://openjdk.java.net/jeps/413)；
-   JEP 416:：[使用方法句柄重新实现核心反射机制](https://openjdk.java.net/jeps/416)；
-   JEP 417：[Vector API（第三个孵化器）](https://openjdk.java.net/jeps/417)；
-   JEP 418：[网络地址解析 SPI](https://openjdk.java.net/jeps/418)；

开发者可通过 [Java Bug Database](https://bugreport.java.com/bugreport/) 提交漏洞。

### 微软加入  Java Community Process（JCP）

作为他们对 Java 编程语言持续贡献的其中一步，微软[宣布](https://devblogs.microsoft.com/java/microsoft-deepens-its-investments-in-java/)已经签署了 [Java 规范参与协议（JSPA）](https://jcp.org/aboutJava/communityprocess/JSPA2.pdf) 并加入 [Java Community Process（JCP）](https://www.jcp.org/en/home/index)。Oracle JCP 项目主席兼主任，[Heather VanCura](https://www.linkedin.com/in/heather-vancura-400395/) 表示：

> 我们很高兴欢迎微软加入 JCP 计划，它继续代表充满活力的 Java 生态系统，我们期待看到微软的贡献。

在此之前，作为 [Adoptium Working Group](https://www.eclipse.org/org/workinggroups/adoptium-charter.php) 的[创始成员](https://www.infoq.com/news/2021/03/eclipse-adoptium-established/)之一，微软[引入](https://www.infoq.com/news/2021/04/microsoft-build-of-openjdk/)了自己的 OpenJDK 下游发行版：Microsoft Build of OpenJDK。

### Helidon

Oracle [发布了](https://medium.com/helidon/helidon-2-4-0-released-18370c0ebc5e) Helidon 2.4.0 版本，内容包括：支持 JDK 17 和 MicroProfile 的 [Long Running Actions（LRA）](https://github.com/eclipse/microprofile-lra/blob/master/README.adoc) 和 [Config](https://github.com/eclipse/microprofile-config/blob/master/README.adoc) 规范；[与 MicroStream 6.0 集成](https://microstream.one/resources/blog/article/microstream-is-now-part-of-helidon/)；在本机映像构建中支持 Oracle [通用连接池](https://www.oracle.com/database/technologies/universal-connection-pool-faq.html#ucp)；[JEP 290](https://openjdk.java.net/jeps/290) 传入流的序列化过滤；和更多的改进功能。更多细节可以在[发行说明](https://github.com/oracle/helidon/releases/tag/2.4.0)中找到。

### Open Liberty

IBM [发布了](https://openliberty.io/blog/2021/11/02/microprofile-jakarta-210012-beta.html) Open Liberty 21.0.0.12-beta 版本，支持即将发布的 MicroProfile 5.0 中的一些功能，跟上 Jakarta EE 9.1 的步伐。[All Beta Features](https://openliberty.io/blog/2021/11/02/microprofile-jakarta-210012-beta.html#allbeta) 包包含对 MicroProfile 规范的升级。[Jakarta EE 9 Beta Features](https://openliberty.io/blog/2021/11/02/microprofile-jakarta-210012-beta.html#jakarta) 包是个轻量级的包，仅包含 [Jakarta EE 9](https://jakarta.ee/) 中的特性。

### Spring 框架

在忙碌的两周之后，Spring 团队发布了 Spring Cloud 和其子项目的小数点版本（point release），度过了相对清静的一周。

在迈向 [Spring Cloud](https://spring.io/projects/spring-cloud) 2021.0.0 的道路上，[第一个候选发行版](https://spring.io/blog/2021/11/03/spring-cloud-2021-0-0-rc1-codename-jubilee-has-been-released)（代号 Jubilee）发布了，对各种 Spring Cloud 子项目的依赖升级和修复，其中包括 [Spring Cloud Sleuth](https://spring.io/projects/spring-cloud-sleuth)，[Spring Cloud Gateway](https://spring.io/projects/spring-cloud-gateway) 和 [Spring Cloud Kubernetes](https://spring.io/projects/spring-cloud-kubernetes)。Spring Cloud 21.0.0-RC1 与 Spring Boot 2.6.0-RC1 兼容。

[Spring Cloud Gateway](https://spring.io/projects/spring-cloud-gateway) 2.2.10.RELEASE 和 3.0.5 版本已[发布](https://spring.io/blog/2021/11/04/spring-cloud-gateway-versions-2-2-10-release-and-3-0-5-are-now-available)，解决了 [CVE-2021-22051](https://tanzu.vmware.com/security/cve-2021-22051) 漏洞。使用 Spring Cloud Gateway 的应用程序容易受到恶意请求的攻击，这些请求可能会对下游服务发出额外请求。

[Spring Cloud Data Flow](https://spring.io/projects/spring-cloud-dataflow) 2.9.1 和 2.8.4 版本已[发布](https://spring.io/blog/2021/11/05/spring-cloud-data-flow-2-8-4-and-2-9-1-released)，作为 [2.9.0](https://github.com/spring-cloud/spring-cloud-dataflow/releases/tag/v2.9.0) 和 [2.8.3 版本](https://github.com/spring-cloud/spring-cloud-dataflow/releases/tag/v2.8.3)的缺陷修复。更多细节可以在 [2.9.1](https://github.com/spring-cloud/spring-cloud-dataflow/releases/tag/v2.9.1) 和 [2.8.4 版本](https://github.com/spring-cloud/spring-cloud-dataflow/releases/tag/v2.8.4)的发行说明中找到。

### Quarkus

Red Hat [发布](https://quarkus.io/blog/quarkus-2-4-1-final-released/)了 Quarkus 2.4.1.Final 维护版本，修复原有缺陷，更新文档，并将依赖升级为 Hibernate ORM 5.6.1，Hibernate Reactive 1.0.1.Final，SmallRye Health 3.1.2 和 SmallRye GraphQL 1.3.5。更多细节可以在[更新日志](https://github.com/quarkusio/quarkus/releases/tag/2.4.1.Final)中找到。

### Hibernate

在 [Hibernate Reactive](https://hibernate.org/reactive/) 1.0 [一般可用（GA）版本](https://in.relation.to/2021/10/27/hibernate-reactive-1/)发布后不到一周，第一个[维护版本](https://in.relation.to/2021/11/01/hibernate-reactive-1_0_1_Final/) —— 1.0.1.Final，以改进性能为特色发布了。更多细节可以在 [issue 列表](https://github.com/hibernate/hibernate-reactive/milestone/14?closed=1)中找到。

### WildFly

Red Hat 发布了 WildFly 25 的[维护版本](https://www.wildfly.org/news/2021/11/04/WildFly2501-Released/)。25.0.1 版本的依赖升级为 [Jandex](https://github.com/wildfly/jandex/blob/master/README.md) 2.4.1.Final 和 [Elytron Web](https://github.com/wildfly-security/elytron-web/blob/1.x/README.md) 1.10.0.Final。更多细节可以在 [issue 列表](https://issues.redhat.com/secure/ReleaseNote.jspa?projectId=12313721&version=12375434)中找到。

### JReleaser

[JReleaser](https://jreleaser.org/) 0.8.0 版本[发布](https://foojay.io/today/jreleaser-0-8-0-released/)了，内容包含：支持国际化，支持将发行工件上传至 AWS S3 上的功能，并提供一个用于创建 ZIP/Tar 发行版的新归档汇编器。更多细节可以在[更新日志](https://github.com/jreleaser/jreleaser/releases/tag/v0.8.0)中找到。

