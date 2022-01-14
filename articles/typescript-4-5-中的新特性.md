这是我参与 11 月更文挑战的第 11 天，活动详情查看：[2021最后一次更文挑战](https://juejin.cn/post/7023643374569816095/)。

> - 原文地址：[What’s New in TypeScript 4.5?](https://betterprogramming.pub/whats-new-in-typescript-4-5-57d6b88b1e72)
> - 原文作者：[Jose Granja](https://dioxmio.medium.com)
> - 译文出自：[掘金翻译计划](https://juejin.cn/translate)

TypeScript 4.5 版本在 11 月 17 日发布了🎉！距离上次 TypeScript “满载”的发布已经有一段时间了。这个消息非常令人振奋。

这是将 ES 模块带入 Node.js 世界的第一次尝试（仍在实验版本阶段）。

然而，这不是唯一受到关注的地方。TypeScript 在导入方面也有诸多改进。可读性提高了，我们在导入类型/变量方面也有更多的控制权。

下面让我们看看这个版本的主要变化。

## `Awaited` 类型

在此版本之前，你必须使用 `infer` 关键字来获取 `Promise` 返回类型，如下所示：

```typescript
type Unwrap<T> = T extends PromiseLike<infer U> ? U : T;

const resultPromise = Promise.resolve(true);
// ✅ resultUnwrapType is boolean 
type resultUnwrapType = Unwrap<typeof resultPromise>;
```

这个版本的 TypeScript 发布了一种新类型 —— `Awaited`。你不再需要像上面代码段那样自定义 `Unwrap` 映射类型了。我们可以简单地执行以下操作：

```typescript
type resultUnwrapType = Awaited<typeof resultPromise>;
```

Awaited 类型功能如下：

- 递归解包；
- 不依赖 `PromiseLike`，提高撸棒性；
-  `Thenable` 解析为 `never`；
- 借助已有的 `Awaited<T>`，为 `Promise.all`，`Promise.race`，`Promise.allSettled` 和 `Promise.any` 添加重载。

让我们看一些不同的用例：

```typescript
// ✅ string 类型
type basic = Awaited<Promise<string>>;

// ✅ string 类型
type recursive = Awaited<Promise<Promise<string>>>;

// ✅ boolean 类型
type nonThenObj = Awaited<boolean>;

// ✅ string | Date 类型
type unions = Awaited<Date | Promise<Promise<string>>>;

type FakePromise = { then: () => string };
// ✅ never 类型
type fake = Awaited<FakePromise>;
```

## 关闭导入省略

在编译阶段，TypeScript 会检测模块是否将在导出的 JavaScript 中使用。如果模块未使用或用作类型注释，则导出的代码中不会导入该模块。这种导入省略是一个很好的性能优化。

这通常不会有什么问题。但在某些情况下，此功能可能会妨碍我们。什么情况？ 例如，在使用 Svelte 等框架及其特定文件格式时。为了解决这个问题，TypeScript 4.5 引进了一个新的 flag —— `--preserveValueImports`。

```html
<script>
    import { bookAppointment } from "./appointment.js";
</script>

<button on:click={bookAppointment}>Book</button>
```

在上面的例子中，TypeScript 将删除 `bookAppointment` 的导入，因为它只能“看到”包含在 `<script>` 标签中的代码。

## 导入语句支持 `type` 修饰词

这是我在这个发布中最喜欢的功能。从版本 3.8 开始，你可以通过将 `type` 附加到 `import` 关键字上来显式地使用类型导入。这将告诉 TSC 编译器此导入仅包含 TypeScript 类型。

```typescript
import { FC, useEffect } from 'react';
```

如果你想具体说明你导入的类型，你可以这样做：

```typescript
import type { FC } from 'react';
import { useEffect } from 'react';
```

但你牺牲了一点可读性。从版本 4.5 开始，你可以混合使用它们。

```typescript
import { type FC, useEffect } from 'react';
```

这样一来代码更加清晰了，我们也无需添加任何额外的代码。

## 导入断言

此功能是 ECMAScript 提案 —— [导入断言（import assertions）](https://github.com/tc39/proposal-import-assertions) 的实现。它目前处于 ECMAScript 流程的第 3 阶段。

它有什么用处？它能确保导入的东西具有预期的格式。

```typescript
// ✅ 常规导入
import students from "./students.json" assert { type: "json" };

// ✅ 动态导入
const students = await import("./students.json", {
    assert: { type: "json" }
})
```

在这种情况下，TypeScript 不会做任何事情，它将留给浏览器和运行时处理。

## Node.js 的测试性 ECMAScript 模块支持

**⚠️仅在 nightly 版本可用，在未来可能会发生变化。**

的基础模块一直都是 CommonJS。随着应用程序转变为多态，支持 ECMAScript 模块的呼声也在增长。在过去的几年里，Node.js 一直在在努力地尝试支持 ES 模块。从 Node 12 版本开始，Node.js 对 ES 模块的支持是广泛可用的。

现在有两个新的 `module` 配置：`nodenext` 和 `node12`。

```json
{
  "compilerOptions": {
    "module": "nodenext"
  }
}
```

### `package.json` 中的 `type` 属性

`type` 属性定义了 Node 将用于所有 `.js` 文件（该 `package.json` 文件必须是其最近的父文件）的模块格式。你可以在 `module`（ ES 模块）或 `commonjs`（传统 CommonJS 模块）这两个值之间进行选择。

对于 `.ts` 文件，TypeScript 使用与 Node 相同的系统行为。当 TypeScript 找到一个 `.ts/.tsx/.js/.jsx` 时，它会查看离它最近的 `package.json` 文件来确定它的模块风格。

### 文件模块系统

如何确定单个文件的模块系统？只需更改其文件扩展名。

- `.cjs/.cjx`: 无论最近的父 `type` 配置如何，文件都将以 CommonJS 格式导入。
- `.cts/.ctx/.d.cts`：无论父 `type` 配置如何，文件都将以 CommonJS 格式导入。当导出文件时，它将输出其对应的 `.cjs`、`.cjx` 或带有 `.d.cts` 扩展名的声明文件。
- `.mjs/.mts/.mtx/.d.mts`：无论父 `type` 配置如何，文件都将以 ECMAScript 模块格式导入。当导出文件时，它将输出其对应的 `.mjs`、`.mjx` 或带有 `.d.mts` 扩展名的声明文件。

### 互操作性

你现在可以通过调整文件系统来导入不同的模块类型，但它们都需要协同工作。对于 ES 模块来说很简单，因为这只是一个转译的问题。对于 ES 模块导入 CommonJS，它们将被视为默认导出。

让我们看看这个例子：

```typescript
// ./foo.cts
export function test() {
  console.log('it works');
}
```

```typescript
// ./bar.mts
import { helper } from './foo.cjs';

// 打印 'it works'
helper();
```

### ES  模块的特点

ES 模块带来了哪些特性？我们应该注意什么？汇总如下：

- **特性**：使用 `import/export` 语句语法；
- **特性**：`nodenext` 支持顶层 `await`；
- **注意事项**：由于现在有不同的模块策略，ES 模块的相对导入需要完整的文件扩展名：`import Fade from ./utils.js`；
- **互操作性**：一些全局关键字，如 `require` 在 ES 模块上不起作用；
- **互操作性**：CommonJS 会转义 ES 特性，如 `import/export` 语法。

## 解析 `node_modules` 中的 `@typescript[lib]`

TypeScript 打包了一些库，以确保它们能与 JavaScript 很好地协同工作。但是，你可能希望将它们更改为另一种类型的库实现。

- `lib.dom.d.ts` -> `@typescript/dom`
- `lib.dom.iterable.d.ts` -> `@typescript/dom/iterable`
- `lib.es2015.symbol.wellknown.d.ts` -> `@typescript/es2015/symbol-wellknown`

举个例子，我们想选择一个不同版本的 `@typescript/dom`。你现在只需执行以下操作即可：

```json
{
  "dependencies": {
    "@typescript/lib-dom": "npm:@types/web"
  }
}
```

它与 `@types` 的行为类似，你现在可以选择合适的类型定义了。

## ES2022 模块

TypeScript 现在支持新的模块设置：`es2022`。它最显着的特点是顶层 `await`。由此一来我们便能够在 `async` 函数之外使用 `await`。

在此之前，它是通过使用 `nodenext` 来支持的，`es2022` 只是一个稳定的 target 版本。

## JSX 属性自动补全

当编写包含 JSX 语法的组件时，TypeScript 不会自动补全代码。现在，这个问题被解决了。你将能在 React 应用程序中编写组件时使用自动补全功能。

代码补全示例：

![img](https://miro.medium.com/max/700/1*JhyClBkB_KHUKtgJRDwZwg.png)


## 模板字符串类型作为判别式

模板字符串是一项自发布以来都一直在不断完善的功能。作为这个新版本的一部分，我们现在可以使用模板字符串类型作为判别式。在以前的版本中，代码可以运行，但什么也不会发生。

```typescript
export interface Event {
    type: `${string}Event`;
    read: () => void;
}
export interface Listener {
    type: `${string}Listener`;
    listen: () => void;
}

export function handler(item: Event | Listener) {
    if (item.type === "PushEvent") {
        // ✅ 在这个作用域内，item 属于 Event 类型
        item.read();
    }
}
```

## 总结

尽管在 Node.js 在支持 ES Modules 方面付出了巨大的努力，但还是有点太仓促了。该功能仍然需要更多的代码来实现。通过实验版本，TypeScript 团队将有机会收集早期反馈。这可能会在下一个版本中正式推送。

我很高兴看到模板字符串类型仍在进步。`type` 修饰词也非常有用。在此之前，为导入添加特定的类型会使得代码过于冗长。

升级 TypeScript 应该相当容易。截至 11 月 6 日，TypeScript 没有太多重大的变化。