# 🔧 代码重构约束 Prompt — 精简为 Claude Code 唯一适配

> **角色**：你是一个 TypeScript 重构专家，当前任务是将 Trellis 项目从多平台 AI 开发框架精简为仅支持 Claude Code 的 AI 漫剧生成工作流工具。

---

## 一、重构铁律

1. **每一步修改后 `pnpm build` 必须编译通过** — 不允许中间态断裂
2. **不允许留下死代码** — 被删除模块的 import/export/引用必须全部清除
3. **保留核心架构骨架** — 模板系统、文件写入器、CLI 框架保留，内容替换
4. **Git 追踪** — 每完成一个 Phase 执行一次 commit

---

## 二、Phase 1 — 平台精简（删除非 Claude 代码）

### Step 1.1：删除配置器文件
```bash
# 删除以下文件
src/configurators/cursor.ts
src/configurators/iflow.ts
src/configurators/opencode.ts
src/configurators/codex.ts
```

### Step 1.2：删除模板目录
```bash
# 删除以下目录（整个目录）
src/templates/cursor/
src/templates/iflow/
src/templates/opencode/
src/templates/codex/
```

### Step 1.3：删除项目根目录的工具配置
```bash
# 删除以下目录
.cursor/
.opencode/
.agents/
```

### Step 1.4：修改类型定义 `src/types/ai-tools.ts`

```typescript
// 修改前
export type AITool = "claude-code" | "cursor" | "opencode" | "iflow" | "codex";
export type TemplateDir = "common" | "claude" | "cursor" | "opencode" | "iflow" | "codex";
export type CliFlag = "claude" | "cursor" | "opencode" | "iflow" | "codex";

// 修改后
export type AITool = "claude-code";
export type TemplateDir = "common" | "claude";
export type CliFlag = "claude";

// 删除 AI_TOOLS 中的 cursor / opencode / iflow / codex 条目
// 仅保留 "claude-code" 条目
```

### Step 1.5：修改配置器注册 `src/configurators/index.ts`

- 删除所有非 Claude 的 import
- PLATFORM_FUNCTIONS 仅保留 `"claude-code"` 条目
- 删除对 cursor/iflow/opencode/codex 模板的 import
- collectTemplates() 仅保留 Claude 相关逻辑

### Step 1.6：修改 CLI 入口 `src/cli/index.ts`

- 删除 `--cursor`、`--iflow`、`--opencode`、`--codex` 等 CLI 选项
- 默认仅配置 Claude Code（无需交互选择）

### Step 1.7：修改 init 命令 `src/commands/init.ts`

- 删除多工具选择逻辑
- InitOptions 中删除非 Claude 的 flag
- 初始化时默认且仅配置 Claude Code

### Step 1.8：修改 update 命令 `src/commands/update.ts`

- 删除多平台遍历逻辑
- 仅更新 Claude Code 模板

### Step 1.9：修改模板提取 `src/templates/extract.ts`

- 删除对非 Claude 模板路径的导出函数
- 保留 `getClaudeTemplatePath()`
- 保留通用模板路径函数（如 `getTrellisTemplatePath()`）

### Step 1.10：修改迁移逻辑 `src/migrations/`

- 检查是否有涉及 cursor/iflow/opencode/codex 的迁移脚本
- 删除不再适用的迁移

### Step 1.11：清理测试 `test/`

- 删除涉及被删平台的测试用例
- 确保 `pnpm test` 全部通过

### Step 1.12：编译验证

```bash
pnpm build
pnpm test
```

---

## 三、Phase 2 — 品牌重命名

### Step 2.1：修改 `package.json`

```diff
- "name": "@mindfoldhq/trellis",
+ "name": "@your-scope/aim-studio",
- "description": "AI capabilities grow like ivy — Trellis provides the structure...",
+ "description": "AI 漫剧 & 连续剧生成工作流 CLI — 从剧本到分镜到成片",
  "bin": {
-   "trellis": "./bin/trellis.js",
-   "tl": "./bin/trellis.js"
+   "aim": "./bin/aim.js"
  },
- "keywords": ["ai", "workflow", "cursor", "claude", ...],
+ "keywords": ["ai", "comic", "drama", "video-generation", "image-generation", "storyboard", "prompt", "claude"],
- "author": "Mindfold LLC",
+ "author": "你的作者名",
```

### Step 2.2：重命名 bin 文件

```bash
# 重命名
bin/trellis.js → bin/aim.js
```

更新 `bin/aim.js` 中的引用路径（如有）。

### Step 2.3：全局搜索替换

在所有源代码中执行以下替换（区分大小写）：

| 查找 | 替换为 | 作用域 |
| --- | --- | --- |
| `trellis` | `aim` | CLI 命令名、目录名 `.trellis/` → `.aim-studio/` |
| `Trellis` | `AIM Studio` | 项目显示名 |
| `@mindfoldhq/trellis` | `@your-scope/aim-studio` | npm 包名 |
| `mindfold-ai/Trellis` | five-five0909/aim-studio | Git URL |

> ⚠️ **注意**：这一步必须仔细审查每个替换，避免误改变量名或语义不同的 "trellis"。

### Step 2.4：更新常量定义 `src/constants/`

- 检查所有常量文件中的品牌/名称引用
- 更新为新品牌

---

## 四、Phase 3 — 模板内容转型

### Step 3.1：改造 Claude 模板目录

```
src/templates/claude/
├── agents/                    # 重写 agent 定义
│   ├── script-agent.md       # 剧本解析 Agent
│   ├── storyboard-agent.md   # 分镜设计 Agent
│   └── render-agent.md       # 渲染提示词 Agent
├── commands/                  # 重写 slash 命令
│   ├── new-project.md        # /aim:new-project
│   ├── new-episode.md        # /aim:new-episode
│   ├── parse-script.md       # /aim:parse-script
│   ├── generate-storyboard.md # /aim:generate-storyboard
│   ├── generate-prompts.md   # /aim:generate-prompts
│   └── export.md             # /aim:export
├── hooks/                     # 保留 hook 机制，修改注入内容
│   └── session-start.py      # 启动时注入漫剧创作上下文
├── skills/                    # ← 新增：Skill 文件
│   ├── image-prompt-optimizer.md
│   ├── video-prompt-optimizer.md
│   ├── script-parser.md
│   ├── storyboard-designer.md
│   ├── character-manager.md
│   ├── style-keeper.md
│   └── episode-manager.md
└── settings.json              # 更新 hook/命令配置
```

### Step 3.2：改造 Trellis 模板目录

```
src/templates/trellis/        # ← 重命名概念为 aim-studio 项目模板
├── workflow.md               # 漫剧创作工作流指南
├── project.yaml              # 项目元数据模板
├── characters/               # 角色档案模板
│   └── template-character.md
├── style/                    # 风格定义模板
│   └── global-style.md
└── episodes/                 # 集数模板
    └── template-episode/
        ├── script.md
        └── storyboard.md
```

---

## 五、Phase 4 — 文档重写

### 需要重写的文档清单

| 文件 | 新内容概述 |
| --- | --- |
| `README.md` | AI 漫剧生成工具介绍、安装使用指南、功能截图 |
| `README_CN.md` | 中文版 README |
| `CLAUDE.md` | 项目技术说明（面向 Claude Code 阅读） |
| `AGENTS.md` | Agent 定义说明（或删除） |
| `.trellis/workflow.md` | 漫剧创作工作流指南 |

### 删除不需要的文档

- `CONTRIBUTING.md` — 个人项目
- `CONTRIBUTING_CN.md` — 个人项目
- `docs/` 目录下不再适用的指南

---

## 六、Phase 5 — 验证清单

```bash
# 1. 编译
pnpm build

# 2. 测试
pnpm test

# 3. 本地打包测试
npm pack
# 检查生成的 .tgz 文件内容

# 4. 本地安装测试
npm install -g ./your-scope-aim-studio-0.1.0.tgz
aim init
# 验证是否正确创建 .aim-studio/ 和 .claude/ 目录

# 5. 验证 Claude Code 集成
# 在测试项目中启动 Claude Code，检查：
# - Skill 是否可见
# - Slash 命令是否可用
# - Hook 是否正常注入上下文
```

---

## 七、危险操作清单（需人工确认）

| 操作 | 风险 | 确认条件 |
| --- | --- | --- |
| 删除 .cursor/ 等目录 | 可能丢失本地自定义配置 | 确认无自定义内容 |
| 全局搜索替换 "trellis" | 可能误改变量名 | 逐一审查替换结果 |
| npm publish | 发布到公网 | 确认 scope/access 正确 |
| 删除 CONTRIBUTING.md | 永久删除 | 确认为个人项目 |

---

**本 Prompt 为代码重构的具体约束和执行步骤指南，配合总纲 Prompt 使用。**
