> [← 返回根目录](../CLAUDE.md) | **src/constants/**
>
> 本模块提供 Trellis 项目的常量定义。

## 概览

`src/constants/` 包含项目的常量定义。

## 模块索引

| 文件 | 导出 | 描述 |
| --- | --- | --- |
| `version.ts` | `VERSION`, `PACKAGE_NAME` | 版本和包名常量 |
| `paths.ts` | `DIR_NAMES` | 目录名称常量 |

## 关键常量

### version.ts

```typescript
// 当前版本
export const VERSION = "0.0.1";

// 包名
export const PACKAGE_NAME = "@fifine/aim-studio";
```

### paths.ts

```typescript
// AIM Studio 工作流目录名
export const DIR_NAMES = {
  WORKFLOW: ".aim-studio",
  WORKSPACE: "workspace",
  SPEC: "spec",
  TASKS: "tasks",
  SCRIPTS: "scripts",
} as const;
```

## 使用示例

```typescript
import { VERSION, PACKAGE_NAME } from "./constants/version.js";
import { DIR_NAMES } from "./constants/paths.js";

console.log(`Running Trellis ${VERSION}`);
const workflowPath = `./${DIR_NAMES.WORKFLOW}`;
```

## 相关模块

- [src/types/](../types/) - 类型定义
- [src/commands/](../commands/) - 命令实现
