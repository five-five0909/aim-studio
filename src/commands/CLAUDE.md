> [← 返回根目录](../CLAUDE.md) | **src/commands/**
>
> 本模块提供 AIM Studio CLI 的核心命令实现。

## 概览

`src/commands/` 包含 AIM Studio CLI 的两个核心命令：
- **init.ts** - 初始化新项目配置
- **update.ts** - 更新现有配置

## 入口文件

| 文件 | 导出 | 职责 |
| --- | --- | --- |
| `init.ts` | `init(options)` | 初始化 AIM Studio 配置，支持多种 AI 工具 |
| `update.ts` | `update(options)` | 更新配置，处理文件迁移和版本兼容 |

## 依赖关系

```
src/commands/
├── init.ts
│   ├── src/configurators/*   (配置各 AI 工具)
│   ├── src/templates/*        (模板处理)
│   └── src/utils/*            (工具函数)
└── update.ts
    ├── src/configurators/*
    └── src/utils/*
```

## 关键类型

### InitOptions

```typescript
interface InitOptions {
  cursor?: boolean;      // 包含 Cursor 命令
  claude?: boolean;      // 包含 Claude Code 命令
  iflow?: boolean;       // 包含 iFlow CLI 命令
  opencode?: boolean;    // 包含 OpenCode 命令
  codex?: boolean;       // 包含 Codex skills
  yes?: boolean;         // 跳过提示使用默认值
  user?: string;         // 开发者标识
  force?: boolean;       // 覆盖现有文件
  skipExisting?: boolean; // 跳过现有文件
  template?: string;     // 远程模板名称
  overwrite?: boolean;   // 覆盖现有规范目录
  append?: boolean;       // 仅添加缺失文件
}
```

### UpdateOptions

```typescript
interface UpdateOptions {
  dryRun?: boolean;       // 预览变更
  force?: boolean;         // 强制覆盖
  skipAll?: boolean;      // 跳过所有变更
  createNew?: boolean;     // 创建 .new 副本
  allowDowngrade?: boolean; // 允许降级
  migrate?: boolean;       // 应用迁移
}
```

## 使用示例

```typescript
// 直接调用 init
import { init } from "./commands/init.js";

await init({
  user: "developer-name",
  cursor: true,
  claude: true,
  force: true,
});

// 直接调用 update
import { update } from "./commands/update.js";

await update({
  dryRun: true,  // 预览模式
});
```

## 相关模块

- [src/configurators/](../configurators/) - AI 工具配置器
- [src/utils/](../utils/) - 工具函数
- [src/templates/](../templates/) - 模板系统
