> [← 返回根目录](../CLAUDE.md) | **src/configurators/**
>
> 本模块提供各 AI 开发工具的配置器实现。

## 概览

`src/configurators/` 包含对不同 AI 开发工具的配置支持：
- Claude Code
- Cursor
- OpenCode
- iFlow
- Codex
- Shared (共享配置)

## 模块索引

| 文件 | 导出 | 职责 |
| --- | --- | --- |
| `claude.ts` | `configureClaude()` | 配置 Claude Code |
| `cursor.ts` | `configureCursor()` | 配置 Cursor |
| `opencode.ts` | `configureOpenCode()` | 配置 OpenCode |
| `iflow.ts` | `configureIFlow()` | 配置 iFlow CLI |
| `codex.ts` | `configureCodex()` | 配置 Codex skills |
| `shared.ts` | `SharedConfig` | 共享配置常量 |
| `workflow.ts` | `configureWorkflow()` | 配置工作流 |
| `index.ts` | 聚合导出 | 统一导出所有配置器 |

## 依赖关系

```
src/configurators/
├── index.ts (主入口)
├── claude.ts    → .claude/{agents,commands,hooks}/
├── cursor.ts    → .cursor/commands/
├── opencode.ts  → .opencode/{agents,commands}/
├── iflow.ts     → iFlow 配置
├── codex.ts     → Codex skills
├── workflow.ts  → .aim-studio/workflow.md
└── shared.ts    → 共享配置
```

## 配置输出

### Claude Code 配置

```
.claude/
├── settings.json     # Hook 配置
├── agents/
│   ├── dispatch.md   # 调度 Agent
│   ├── implement.md # 实现 Agent
│   ├── check.md     # 检查 Agent
│   └── research.md  # 调研 Agent
├── commands/        # 斜杠命令
└── hooks/           # Hook 脚本
```

### Cursor 配置

```
.cursor/
└── commands/         # 短命令
```

### OpenCode 配置

```
.opencode/
├── agents/          # Agent 定义
└── commands/        # 命令
```

## 使用示例

```typescript
import { configureClaude, configureCursor } from "./configurators/index.js";

await configureClaude({
  user: "developer-name",
  commands: ["start", "parallel", "record-session"],
});

await configureCursor({
  user: "developer-name",
  commands: ["before-frontend-dev", "before-backend-dev"],
});
```

## 相关模块

- [src/commands/](../commands/) - 命令入口
- [src/templates/](../templates/) - 模板系统
- [src/utils/](../utils/) - 工具函数
