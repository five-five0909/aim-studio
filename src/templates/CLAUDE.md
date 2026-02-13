> [← 返回根目录](../../CLAUDE.md) | **src/templates/**
>
> 本模块提供 AIM Studio 的模板系统，用于生成各种 AI 工具的配置文件。

## 概览

`src/templates/` 包含各 AI 开发工具的配置模板和模板处理逻辑。

## 模块索引

| 目录/文件 | 导出 | 职责 |
| --- | --- | --- |
| `extract.ts` | `extractFrontmatter()` | 提取 Markdown 前后置元数据 |
| `claude/` | `ClaudeTemplates` | Claude Code 模板 |
| `aim/` | `AimTemplates` | Python 脚本模板 |
| `markdown/` | `MarkdownTemplates` | Markdown 模板 |

## 依赖关系

```
src/templates/
├── extract.ts        (元数据提取工具)
├── claude/           → .claude/{agents,commands,hooks}/
├── aim/              → .aim-studio/scripts/*.py
└── markdown/         → .aim-studio/spec/*.md
```

## 模板结构

每个工具的模板目录通常包含：

```
templates/{tool}/
├── {agent}.md        # Agent 定义
├── {command}.md      # 命令定义
├── {hook}.py         # Hook 脚本
└── spec/             # 规范文件
```

## 关键 API

### 模板渲染

```typescript
import { renderTemplate } from "./templates/index.js";

const rendered = renderTemplate("claude/implement.md", {
  user: "developer-name",
  project: "my-project",
});
```

### 前后置元数据

```typescript
import { extractFrontmatter } from "./templates/extract.ts";

interface Frontmatter {
  title?: string;
  description?: string;
  tags?: string[];
}

const { frontmatter, content } = extractFrontmatter(markdownString);
```

## 相关模块

- [src/commands/](../commands/) - 命令入口
- [src/configurators/](../configurators/) - 配置器
- [src/utils/](../utils/) - 工具函数
