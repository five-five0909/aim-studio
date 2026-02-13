> [← 返回根目录](../CLAUDE.md) | **src/types/**
>
> 本模块提供 Trellis 项目的 TypeScript 类型定义。

## 概览

`src/types/` 包含项目的类型定义文件。

## 模块索引

| 文件 | 导出 | 描述 |
| --- | --- | --- |
| `ai-tools.ts` | `AITool` | AI 开发工具枚举和类型 |
| `migration.ts` | `Migration` | 配置迁移类型 |

## 关键类型

### AITool

```typescript
type AITool =
  | "claude"    // Claude Code
  | "cursor"    // Cursor
  | "opencode"  // OpenCode
  | "iflow"     // iFlow CLI
  | "codex";    // Codex Skills
```

### Migration

```typescript
interface Migration {
  id: string;           // 迁移 ID
  fromVersion: string;  // 源版本
  toVersion: string;    // 目标版本
  apply(): Promise<void>;  // 应用迁移
  rollback(): Promise<void>; // 回滚迁移
}
```

## 使用示例

```typescript
import type { AITool, Migration } from "./types/index.js";

const tool: AITool = "claude";

const migration: Migration = {
  id: "v0.2-migrate-hooks",
  fromVersion: "0.1.0",
  toVersion: "0.2.0",
  async apply() { /* ... */ },
  async rollback() { /* ... */ },
};
```

## 相关模块

- [src/constants/](../constants/) - 常量定义
- [src/commands/](../commands/) - 命令实现
