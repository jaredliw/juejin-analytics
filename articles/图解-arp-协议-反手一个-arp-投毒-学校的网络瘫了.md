---
theme: arknights
highlight: zenburn
---
这是我参与 2022 首次更文挑战的第 3 天，活动详情查看：[2022首次更文挑战](https://juejin.cn/post/7052884569032392740)。

## MAC 地址是什么？

MAC 地址，全称为媒体访问控制地址（Media Access Control address），是一个用来确认网络设备位置的唯一标识符。该地址**由 6 个字节的十六进制数组成**，大概长这样：

```text
// Windows
00-00-5E-00-53-AF

// Apple、Linux
00:00:5e:00:53:af

// Cisco
0000.5e00.53af
```

MAC 地址的前 3 个字节标识的是网卡（Network Interface Card，NIC）的制造商，称为**组织唯一标识符**（Organizational Unique Identifier，OUI）；后 3 个字节为制造商所分配的唯一序列号。

通过 OUI，我们能得知 NIC 制造商的相关信息，包含名称、国家、地区等等。

![MAC 地址的组成部分](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/8b9d065b14f44e95933c9e13b411d44e~tplv-k3u1fbpfcp-watermark.image?)

### IP 地址和 MAC 地址有什么区别？

1. 公共的 IP 地址是可以更改的，但 MAC 地址是永久的；
2. IP 地址为 32 位，MAC 地址为 48 位；
3. MAC 地址用于**识别设备**，IP 地址用于**定位设备**（待会儿会详细说说）；
4. IP 地址的分配基于网络拓扑，而 MAC 地址的分配则是基于制造商；
5. 在 OSI 七层模型中，IP 地址划分在网络层，而 MAC 地址则是在数据链路层。

   ![OSI 模型](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/12e6fac9ef774aaaa827e7c9a57cb1af~tplv-k3u1fbpfcp-watermark.image?)

## 通信……？

### 已经有了 IP 地址，为什么还需要 MAC 地址？

笼统上来说，设备相互**通信时最终使用的是 MAC 地址**，IP 地址只用于确定接收方是否在同一个局域网上。也就是说，IP 地址能高数我们数据需不需要通过路由器向外转发。

让我们看个例子。假设计算机 A 想要与计算机 C 通信：

![简单局域网](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/430bd64e2afc48a3abf850c26e0e2065~tplv-k3u1fbpfcp-watermark.image?)

首先，计算机 A 将检查计算机 C 的 IP 地址，确认对方是否在同一个网络上（同一个网络上的设备有相同的 IP 前缀，这与 TCP/IP 协议有关，希望下次有机会聊聊这个）。在开始通信之前，计算机 A 需要得到计算机 C 的 MAC 地址。这时，地址解析协议（ARP）就派上用场了……

### 什么是 ARP？

地址解析协议（Address Resolution Protocol，ARP）是一个通过**解析网络层地址**（即 IP 地址）来**找寻数据链路层地址**（即 MAC 地址）的网络传输协议。

该协议将向局域网内的所有设备**广播包含目标 IP 地址 ARP 数据帧**；作为应答，拥有这个 IP 地址的设备将返回自身的 MAC 地址。

![ARP 广播](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1f3b027f45f74915bcb2dd2d9188f6f2~tplv-k3u1fbpfcp-watermark.image?)

![ARP 响应](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/87ee709ab6b140d6a3fcc2d50d9bd90f~tplv-k3u1fbpfcp-watermark.image?)

（彩蛋：对话框里的句子是 Wireshark 对 ARP 的附加描述信息。）

**如果通信双方不在同一个网络里时怎么办？**

这时计算机 A 将会通过 ARP 获取默认网关（default gateway）的 MAC 地址，并将数据发送给网关。

> 默认网关是是一种将设备从一个网络转发到另一个网络的设备。在大多数情况下，默认网关就是路由器。

之后，网关将通过 IP 地址确认数据发送的最佳路径。它将发出一个 ARP 广播以获取下一个路由器的 MAC 地址，然后再将数据转发给它；由此往复，直到送达目的地为止。

### ARP 数据报格式

广播：

![ARP 广播数据报](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/cc762e32d12245889b8b700801cccc4d~tplv-k3u1fbpfcp-watermark.image?)

应答：

![ARP 响应数据报](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ef992aeddafc45928cf8223ded761678~tplv-k3u1fbpfcp-watermark.image?)


数据报由以下的这几个部分组成：

（建议与上图对照着理解~）

注：前三个字段为以太网（Ethernet）的报头，接下来的字段才是 ARP 的报文数据。

| 字段 | 长度（位） | 描述 |
| --- | --- | --- |
| 目标以太网地址 | 48 | 当前数据报接收方的 MAC 地址；`FF FF FF FF FF FF` 表示广播地址，局域网内的所有设备都会收到这个数据报。 |
| 源以太网地址 | 48 | 当前数据报发送方的 MAC 地址。 |
| 帧类型 | 16 | 表示数据类型；`08 06` 是 ARP，`08 00` 是 IPv4 等等。 |
| 硬件类型 | 16 | `00 01` 是以太网；完整列表见[这里](http://www.networksorcery.com/enp/protocol/arp.htm)。|
| 协议类型 | 16 | `08 00` 是 IPv4 协议；这也是目前为止 ARP 唯一支持的协议。 |
| 硬件地址长度 | 8 | MAC 地址的长度，即 6 个字节（`06`）。 |
| 协议地址长度 | 8 | IP 地址的长度，即 4 个字节（`04`）。|
| 操作码 | 16 | `00 01` 为 ARP 请求，`00 02` 为 ARP 应答。 |
| 源硬件地址 | 48 | 当前数据报发送方的 MAC 地址。 |
| 源协议地址 | 32 | 当前数据报发送方的 IP 地址。 |
| 目标硬件地址 | 48 | 当前数据报接收方的 MAC 地址；在 ARP 广播时，这个值是未知的，将填为 `00 00 00 00 00 00`。 |
| 目标协议地址 | 32 | 当前数据报接收方的 IP 地址。|

### ARP 缓存表

**每次通信都要 ARP 广播一次，这样岂不是非常低效？**

那是肯定的，一个网络里可以有几十甚至上百台设备，每发一个包就要广播一次那还得了。因此，这些协议地址和硬件地址是缓存在本机上的。你可以在命令行中执行 `arp -a` 来查看这个缓存表：

![命令行截图](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/01fca732d6634f7d819afb984a718ac9~tplv-k3u1fbpfcp-watermark.image?)

缓存里的项目分为动态（dynamic）和静态（static）两种。静态项目将一直保留在计算机中，而动态项目则会随时间推移自动删除。当然，你也可以手动清除所有缓存，命令是：`arp -d`。

## ARP 投毒（ARP poisoning）

说起来也挺巧，这几天在油管上看到了个关于 ARP 的视频，就想着写篇文章试试；边写边学嘛，挺好的。写着写着才发现：好家伙，这不是我第一次搞网络攻击的那玩意儿吗？！原来背后是这样个事儿！

那时上的初中，才刚懂一些渗透知识，自己用 U 盘装了一个 Kali 系统，琢磨琢磨几个现成的工具…… 其中一个就是 Ettercap：

![Ettercap](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1b7e17d3a8b54652b055e4eccc14b6c0~tplv-k3u1fbpfcp-watermark.image?)

回想起那天，在计算机实验室里上着课，老师在前面讲 PPT，某些（准确来说是大部分 xD）祖国的花朵则在后面抱团打网游……

“身为程序员的我，是时候该做些什么了。”

键盘啪啪几下，除我以外，全班的网页唰一下就全白了…… 事了拂衣去，深藏功与名。

![真男人从不回头看爆炸](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/79ca1225af144074980a9800ac953eb2~tplv-k3u1fbpfcp-watermark.image?)

（真 TM 屁孩~）

### 攻击原理

我们知道，一台主机要想连网，就得知道网关的 MAC 地址。要想知道 MAC 地址，它就得发出一个 ARP 广播。这时，攻击者能将自己伪造成网关，向受害主机发送虚假的 ARP 应答。

这样一来，受害主机的所有请求就导来我们这儿了，现在想做什么都随攻击者的便；他可以返回一个虚假的网页（从网址是看不出异样的），也可以什么也不做（这样它不就连不到网了嘛）。

总的来说，ARP 欺骗攻击就是中间人攻击（Man-in-the-Middle attack，MitM）的一种。攻击者可以通过欺骗局域网内的主机和网关来截取并伪造通信双方之间的数据。

### 防范措施

1. 使用静态 ARP 缓存表

   我们可以将网络中的所有 MAC 地址静态映射到其正确的 IP 地址（上方提到过静态 ARP 缓存）。
   
   这能有效地防止 ARP 投毒，但缺点是会很大地增加管理负担。网络的任何更改都需要我们手动更新所有主机的 ARP 表，这使得该方法对于大多数大型组织来说是不可行的。
   
2. 网络隔离

   ARP 协议是受限于本地网络内的，ARP 数据报是不可能通过网关的。只要我们良好地分割网络，整体上来说不太容易受到 ARP 缓存中毒的影响。
   
3. 不要连接公共 Wifi 或陌生的网络

   显而易见，这是一种自杀行为，你不能保证你现在所看到的所有内容不是由一个恶意的第三方伪造的。
   
4. DHCP snooping

   DHCP snooping 是 DHCP 的一种安全特性，主要应用在交换机上，作用是屏蔽接入网络中的非法的 DHCP 服务器。在开启 DHCP snooping 功能后，网络中的客户端只能从管理员指定的 DHCP 服务器获取 IP 地址。
   
   DHCP，全称为动态主机设置协议（Dynamic Host Configuration Protocol）；这又是另一个网络协议了…… 碍于篇幅的关系，下次有机会再聊聊吧~（点赞数将直接影响这篇文章的产出 xD）
   
写到这里我只想说：哪个家伙说网络都是理论概念的，拖出去斩了！

## 参考资料

1. https://youtu.be/cn8Zxh9bPio
2. https://youtu.be/TIiQiw7fpsU
3. https://juejin.cn/post/6844903542889660423
4. https://www.varonis.com/blog/arp-poisoning
5. https://baike.baidu.com/item/DHCP%20Snooping/5217371
6. http://www.networksorcery.com/enp/protocol/arp.htm
