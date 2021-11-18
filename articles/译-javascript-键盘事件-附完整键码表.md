这是我参与 11 月更文挑战的第 10 天，活动详情查看：[2021最后一次更文挑战](https://juejin.cn/post/7023643374569816095/)。

> - 原文地址：[JavaScript Keycode List – Keypress Event Key Codes for Enter, Space, Backspace, and More](https://www.freecodecamp.org/news/javascript-keycode-list-keypress-event-key-codes/)
> - 原文作者：[Tapas Adhikary](https://www.freecodecamp.org/news/author/tapas/)
> - 译文出自：[掘金翻译计划](https://juejin.cn/translate)

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d5f6f586fdcf4426a2e3e43ddb145131~tplv-k3u1fbpfcp-zoom-1.image) 

**JavaScript 键盘事件可帮助你捕获用户与键盘的交互。**

与许多其他的 JavaScript 事件一样，`KeyboardEvent` 接口提供了所有必要的属性和方法来处理用户的每次击键。

现今网络上已有很多关于 `KeyboardEvent` 原理和使用教程。但与此同时，[W3.org](https://www.w3.org/TR/uievents/#events-keyboardevents) 也在通过引入新属性、弃用现有属性以及将某些代码标记为“遗留代码（legacy code）“来不断更新规范。

因此，Web 开发者必须不断更新有关 `KeyboardEvent` 接口的知识，以了解哪些东西应该使用，哪些东西已经过时。

在这篇文章中我们会学习：

- `KeyboardEvent` 接口；
- 我们需要关注的键盘事件类型；
- 那些我们可能永远都不需要的键盘事件类型；
- 在实践中需要的属性和不同的浏览器处理它们的方式；
- 哪些已被弃用，哪些仍能使用；
- 一个能让我们在学习时尝试事物的游乐场；
- 最后是当前的键码表，供参考用。

希望你会喜欢这篇文章。

## `KeyboardEvent` 接口和事件类型

`KeyboardEvent` 接口提供了一些常量、属性和一个方法（截至 2021 年 1 月）。它能为我们提供关于键盘事件的的有用信息。`KeyboardEvent` 扩展了 `UIEvent` 接口，也间接地扩展了 `Event` 接口。

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/5b7be8b51a5049a1ad23ed3b1ad11c95~tplv-k3u1fbpfcp-zoom-1.image)


键盘事件类型主要有三种：`keydown`、`keypress` 和 `keyup`。我们可以从 `KeyboardEvent` 接口的属性和方法中获取有关这些事件的上下文信息。

你可以使用 `addEventListener` 将这些事件绑定到 HTML 元素或 `document` 对象上。下方的示例展示了如何监听 `id` 为 `type-here` 的元素的 `keydown`事件。

```javascript
let elem = document.getElementById('type-here');

elem.addEventListener("keydown", function (event) {
    // event 参数的类型为 KeyboardEvent
  	addRow(event);
});
```

你也可以通过使用 `onKeydown(event)`，`onKeyup(event)`，`onKeypress(event)` 处理函数来监听键盘事件。下方的示例展示了如何监听一个 `input` 元素的 `keyup` 事件。

```html
<input type="text" id="type-here" onkeyup="doSomething(event)">
```

如果你在浏览器的控制台中打印 `event` 事件对象，你将看到它的所有属性和方法，其中的一些是从 `UIEvent` 和 `Event` 接口继承的。

这是当我按下 `a` 键时的 `keyup` 事件：

![`a` 键的 `keyup` 事件](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/86ef8903520b432ea757ee14c3148c95~tplv-k3u1fbpfcp-zoom-1.image)

## 试试这个交互式键盘事件游乐场

在我们继续之前，让我们试试一个游乐场吧。你可以在该游乐场中探索所有键盘事件，属性，特征扽等。我认为将它与本文及其他文章一起使用是件很棒的事。

你只需要输入任意键即可查看有关它的上下文信息。

你也可以通过页面上方的复选框来过滤事件。[试试吧](https://js-keycodes.stackblitz.io/)：

![截图](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/61b879f75f40456ca2be18f927eb69b6~tplv-k3u1fbpfcp-watermark.image?)

> 如果你在访问上方游乐场时遇到任何问题，你可以直接在此处访问此工具：[https://keyevents.netlify.app/](https://keyevents.netlify.app/)  
>   
> 你可以在这里找到上方 demo 的源代码：[https://github.com/atapas/js-keyevents-demo](https://github.com/atapas/js-keyevents-demo)

## `keydown`，`keypress`，`keyup` —— 我应该选择哪个？

键盘事件包含：

- `keydown`：当任意按键被按下时触发；
- `keypress`: 它仅在产生[字符值](https://www.w3.org/TR/uievents/#character-value)的键被按下时触发。举例来说，如果你按下键 `a`，此事件将会触发，因为 `a` 键产生了字符值 `97` 。当你按下 `shift` 键时不会触发此事件，因为它不会产生任何字符值；
- `keyup`：当任意按键被松开时触发。

如果所有三个事件都绑定到到一个 DOM 元素，则触发顺序为：

1. 首先，`keydown`；
2. 接着，`keypress`（视上方条件而触发）；
3. 最后，`keyup`。

在这些事件中，最常用的（或者说应该成为最常用的）键盘事件是 `keydown`，因为：

- `keydown` 事件覆盖最多的键，能生成有用的上下文信息。`keypress` 事件仅包含部分的键。你无法通过 `keypress` 事件捕获 `Alt`、`Ctrl`、`Shift`、`Meta` 等其他类似的事件。这也意味着  `Ctrl z`，`Shift Tab` 等组合无法触发 `keypress` 事件。
- 此外，[`keypress` 事件](https://www.w3.org/TR/uievents/#event-type-keypress)已被弃用。这个理由已经足够让你避免使用它了。
- 虽然 `keydown` 和 `keyup` 事件都涵盖了所有的键，并且被大多数浏览器支持，但它们之间仍有一些不同之处，使得 `keydown` 更胜于 `keyup`。`keydown` 事件在浏览器处理键之前触发，而 `keyup` 事件在浏览器处理键之后触发。如果你取消了 `keydown` 事件（例如使用 `event.preventDefault()`），浏览器的操作将被取消。在 `keyup` 事件的情况下，即使你取消了该事件，浏览器的操作也不会被取消。

在下方的示例中，我们在 `keydown` 或 `keyup` 事件触发时使用 `event.preventDefault()`。在 `keydown` 的情况下，浏览器不会执行将字符写入文本框的操作，但 `keyup` 则不受影响。

[`keydown` 与 `keyup` 的对比：](https://stackblitz.com/edit/js-key-down-up-test?devtoolsheight=33&embed=1&file=index.html)

![截图](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ad3423afd6f844489c391b8f10709130~tplv-k3u1fbpfcp-watermark.image?)

根据所有的这些解释，显然 `keydown` 事件赢了。它应该成为最流行（最常用）的键盘事件类型。

## 如何在实践中使用 `KeyboardEvent` 属性

这个问题很重要，但却不那么好回答。简短的答案是：视情况而定。什么情况？这取决于：

- 浏览器对应用程序的支持；
- 应用程序代码的遗留程度如何？你愿意重构多少？

在讨论这个话题之前，让我们先预览一下 `KeyboardEvent` 接口中的一些有用的属性和方法。

| 属性/方法                 | 描述                                                         | 弃用/已过时 |
| ------------------------- | ------------------------------------------------------------ | ----------- |
| altKey                    | 返回布林值。当 `Alt` 键按下时值为 `true`。                   | 否          |
| ctrlKey                   | 返回布林值。当 `Control` 键按下时值为 `true`。               | 否          |
| shiftKey                  | 返回布林值。当 `Shift` 键按下时值为 `true`。                 | 否          |
| metaKey                   | 返回布林值。当任意一个 `Meta` 键按下时值为 `true`。          | 否          |
| code                      | 物理键的键码值。                                             | 否          |
| key                       | 按下的键的实际值。                                           | 否          |
| `getModifierState()` 方法 | 返回布林值。`true`  值表示这些键处于 `on`  状态：`CapsLock`，`NumLock`，`Alt`，`Control`，`Shift`，`Meta` 等等 | 否          |
| charCode                  | 返回 Unicode 值。已被弃用，我们应改用 `key` 属性。           | 是          |
| keyCode                   | 返回按下键的数字代码。已被弃用，我们应改用 `key` 属性。      | 是          |
| which                     | 返回按下键的数字代码。已被弃用，我们应改用 `key` 属性。      | 是          |

最后三个属性已被弃用，你应该改用 `key` 属性。`key` 属性有[最广泛的浏览器支持](https://caniuse.com/?search=Keyboardevent.key)。

以下的浏览器支持 `key` 属性：

- Microsoft Edge：版本 >= 79
- Firefox：版本 >= 29
- Google Chrome：版本 >= 51
- Safari：版本 >= 10.1

只要你使用的不是那些老旧的浏览器，`event.key` 属性足用于识别一个键。如果你必须支持较旧的浏览器，较好的替代属性是 `event.which`。

```javascript
window.addEventListener("keydown", function (event) {
  
  if (event.key !== undefined) {
    //使用 KeyboardEvent.key 处理事件
  } else if (event.which !== undefined) {
    // 使用 KeyboardEvent.which 处理事件
  }
});
```

如果你的代码使用了任何已弃用的属性，并且你还机会去重构它们，那么就别等了吧。

## 修饰键

修饰键是键盘上的特殊键，用于修改其他键的默认行为。`Control`、`Shift` 和 `Alt` 是修饰键的一些例子。我们可以通过结合一个修饰键与另一个键来执行不同的操作。

举例来说，如果你按下  `z` 键，它应该返回 z 字母的 `key` 和 `code`。如果你将它与 `Control` 修饰键组合，按下 `Control z`，你很可能会得到一个撤销操作。下一小节中我们将会看到更多的例子。

`event.altKey`，`event.ctrlKey`，`event.shiftKey` 等属性有助于检测是否按下了修饰键。

## 按键组合

我们可以组合多个键并根据键组合执行操作。下面的代码片段展示了如何结合 `Control` 和 `z` 键来定义一个动作：

```javascript
document.getElementById("to_focus").addEventListener("keydown", function(event) {
    if (event.ctrlKey && event.key === "z") {
        // 做些事，可以是一个“撤销”操作
    }
});
```

这是另一个演示组合键的示例。[试一试](https://js-key-combinations.stackblitz.io/)吧：

![截图](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/cf189bc3b22843c1bfe9d6f0ac171e43~tplv-k3u1fbpfcp-watermark.image?)

## 键盘事件值的完整列表

下表显示了所有的键和对应的 `event.which`，`event.key` 和 `event.code` 值。

| Key Name | `event.which` | `event.key` | `event.code` | Notes |
| --- | --- | --- | --- | --- |
| backspace | 8 | Backspace | Backspace |  |
| tab | 9 | Tab | Tab |  |
| enter | 13 | Enter | Enter |  |
| shift(left) | 16 | Shift | ShiftLeft | `event.shiftKey` 为 `true` |
| shift(right) | 16 | Shift | ShiftRight | `event.shiftKey` 为 `true` |
| ctrl(left) | 17 | Control | ControlLeft | `event.ctrlKey` 为 `true` |
| ctrl(right) | 17 | Control | ControlRight | `event.ctrlKey` 为 `true` |
| alt(left) | 18 | Alt | AltLeft | `event.altKey` 为 `true` |
| alt(right) | 18 | Alt | AltRight | `event.altKey` 为 `true` |
| pause/break | 19 | Pause | Pause |  |
| caps lock | 20 | CapsLock | CapsLock |  |
| escape | 27 | Escape | Escape |  |
| space | 32 |  | Space | `event.key` 的值是一个空格 |
| page up | 33 | PageUp | PageUp |  |
| page down | 34 | PageDown | PageDown |  |
| end | 35 | End | End |  |
| home | 36 | Home | Home |  |
| left arrow | 37 | ArrowLeft | ArrowLeft |  |
| up arrow | 38 | ArrowUp | ArrowUp |  |
| right arrow | 39 | ArrowRight | ArrowRight |  |
| down arrow | 40 | ArrowDown | ArrowDown |  |
| print screen | 44 | PrintScreen | PrintScreen |  |
| insert | 45 | Insert | Insert |  |
| delete | 46 | Delete | Delete |  |
| 0-9 | 48-57 | 0-9 | Digit0-Digit9 |  |
| a-z | 65-90 | a-z | KeyA-KeyZ |  |
| left window key | 91 | Meta | MetaLeft | `event.metaKey` 为 `true` |
| right window key | 92 | Meta | MetaRight | `event.metaKey` 为 `true` |
| select key (Context Menu) | 93 | ContextMenu | ContextMenu |  |
| numpad 0-9 | 96-105 | 0-9 | Numpad0-Numpad9 |  |
| multiply | 106 | \* | NumpadMultiply |  |
| add | 107 | + | NumpadAdd |  |
| subtract | 109 | \- | NumpadSubtract |  |
| decimal point | 110 | . | NumpadDecimal |  |
| divide | 111 | / | NumpadDivide |  |
| f1-f12 | 112-123 | F1-F12 | F1-F12 |  |
| num lock | 144 | NumLock | NumLock |  |
| scroll lock | 145 | ScrollLock | ScrollLock |  |
| audio volume mute | 173 | AudioVolumeMute |  | ⚠️ 在 Firefox 中，`event.which` 的值是 181，`event.code` 的值是 `VolumeMute` |
| audio volume down | 174 | AudioVolumeDown |  | ⚠️ 在 Firefox 中，`event.which` 的值是 182，`event.code` 的值是  `VolumeDown` |
| audio volume up | 175 | AudioVolumeUp |  | ⚠️ 在 Firefox 中，`event.which` 的值是 183，`event.code` 的值是  `VolumeUp` |
| media player | 181 | LaunchMediaPlayer |  | ⚠️ 在 Firefox 中，`event.which` 的值是 0（无值），`event.code` 的值是 `MediaSelect` |
| launch application 1 | 182 | LaunchApplication1 |  | ⚠️ 在 Firefox 中，`event.which` 的值是 0（无值），`event.code` 的值是 `LaunchApp1` |
| launch application 2 | 183 | LaunchApplication2 |  | ⚠️ 在 Firefox 中，`event.which` 的值是 0（无值），`event.code` 的值是 `LaunchApp2` |
| semi-colon | 186 | ; | Semicolon | ⚠️ `event.which` 的值在 Firefox 中是 59 |
| equal sign | 187 | = | Equal | ⚠️ `event.which` 的值在 Firefox 中是 61 |
| comma | 188 | , | Comma |  |
| dash | 189 | \- | Minus | ⚠️ `event.which` 的值在 Firefox 中是 173 |
| period | 190 | . | Period |  |
| forward slash | 191 | / | Slash |  |
| Backquote/Grave accent | 192 | \` | Backquote |  |
| open bracket | 219 | \[ | BracketLeft |  |
| back slash | 220 | \\ | Backslash |  |
| close bracket | 221 | \] | BracketRight |  |
| single quote | 222 | ' | Quote |  |

请注意：

- `event.which` 已被弃用（或者说已经过时了）。
- 小写字母（a）和大写字母（A）的 `event.code` 值相同，但 `event.key` 值表示的是实际输入的字母。
- 等号（`=`），分号（`;`）和减号（`-`）的 `event.which` 值在 Firefox 和其他浏览器是不同的。

## 虚拟键盘的事件

那么虚拟键盘呢，比如手机、平板电脑或任何其他输入设备？

[规范上说](https://w3c.github.io/uievents/#code-virtual-keyboards)，如果虚拟键盘的布局和功能与标准键盘相似，则它必然会返回恰当的 `code` 属性。否则，它将不会返回正确的值。

## 总结

总的来说，

- 你可以使用 `KeyboardEvent` 来捕获用户和键盘之间的交互；
- 主要有三种键盘事件：`keydown`，`keypress` 和 `keyup`；
- 我们应该尽可能多地使用 `keydown` 事件因为他能满足绝大多数的用例；
- `keypress` 事件类型已被弃用；
- `event.which`属性已被弃用，尽可能使用 `event.key`；
- 如果你必须支持较旧的浏览器，请使用适当的属性替代；
- 我们可以组合多个键并执行操作；
- 只要布局和功能与标准键盘相似，以上所有事件在虚拟键盘上是支持的。
