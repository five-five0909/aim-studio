# 🎯 项目转型总纲 Prompt — Trellis → AI 漫剧/连续剧生成工作流工具

> **目标**：将 `@mindfoldhq/trellis`（一个面向 AI 编码的开发工作流框架）完整转型为 **AI 漫剧 & 连续剧生成工作流 CLI 工具**，仅保留 Claude Code 适配，发布至 npm 供个人使用。

---

## 一、项目身份重定义

### 1.1 原始身份（删除）
- AI 开发工作流框架
- 支持 Claude Code / Cursor / iFlow / OpenCode / Codex 五大平台
- 自动注入编码规范、工作流、上下文
- 并行 AI 编码会话管理

### 1.2 新身份（建立）
| 维度 | 新定义 |
| --- | --- |
| **项目名称** | `@your-scope/aim-studio`（或自选名称，建议含 "aim" 或 "comic" 关键字） |
| **一句话定义** | AI 漫剧 & 连续剧生成工作流 CLI —— 从剧本到分镜到成片的全链路 AI 创作框架 |
| **核心场景** | AI 漫画剧集、AI 连续剧、AI 短剧、AI 绘本、AI 故事可视化 |
| **工具定位** | 基于 Claude Code 的 AI 创作 Skill/Workflow 注入器 —— 通过注入专业 prompt skill 让 Claude 成为你的漫剧制作 AI 助手 |
| **目标用户** | 你自己（个人使用、npm 发布） |

### 1.3 品牌元素
- **包名**：替换 `@mindfoldhq/trellis` → 你的 npm scope/包名
- **CLI 命令名**：替换 `trellis` / `tl` → 新命令名（如 `aim`、`aimstudio`）
- **描述语**：`AI 能力如藤蔓生长` → `从剧本到画面，AI 让故事活起来`（或自定义）
- **Logo/Banner**：更新 `assets/` 目录下的所有图片资源

---

## 二、架构精简原则

### 2.1 仅保留 Claude Code 适配
| 保留 | 删除 |
| --- | --- |
| `src/configurators/claude.ts` | `src/configurators/cursor.ts` |
| `src/templates/claude/` | `src/configurators/iflow.ts` |
| `.claude/` 配置目录 | `src/configurators/opencode.ts` |
| | `src/configurators/codex.ts` |
| | `src/templates/cursor/` |
| | `src/templates/iflow/` |
| | `src/templates/opencode/` |
| | `src/templates/codex/` |
| | `.cursor/` `.opencode/` `.agents/` 目录 |

### 2.2 类型系统精简
```typescript
// 原始 AITool 类型
type AITool = "claude-code" | "cursor" | "opencode" | "iflow" | "codex";

// 精简为
type AITool = "claude-code";
```

### 2.3 CLI 命令精简
- 保留 `init` / `update` 核心命令
- 删除多平台选择逻辑（无需交互式选择工具）
- 删除 `parallel` 并行会话管理（编码特有功能）

---

## 三、功能转型方向

### 3.1 核心能力矩阵

| 能力模块 | 说明 | 实现方式 |
| --- | --- | --- |
| **剧本解析** | 解析用户的文字剧本 → 结构化场景列表 | Claude Code Skill |
| **分镜设计** | 每个场景 → 画面构图/镜头语言描述 | Claude Code Skill |
| **角色一致性** | 维护角色外观/服装/表情特征档案 | 角色 spec 文件 + 上下文注入 |
| **图片提示词** | 结构化图片生成提示词（适配 Qwen-Image/FLUX 等） | 图片生成优化 Skill（已有） |
| **视频提示词** | 结构化视频生成提示词（适配 Seedance/可灵等） | 视频生成优化 Skill（已有） |
| **风格锁定** | 维护全剧统一画风/色彩/渲染风格 | 风格 spec 文件 |
| **集数管理** | 管理连续剧多集剧本/分镜/产出 | 项目目录结构 + 元数据 |
| **产出组织** | 组织生成的图片/视频/字幕文件 | 输出目录规范 |

### 3.2 Skill 体系设计

取代原有的"开发规范 spec"，新增以下 AI 创作 Skill：

```
.claude/skills/
├── script-parser.md          # 剧本解析 Skill
├── storyboard-designer.md    # 分镜设计 Skill
├── character-manager.md      # 角色一致性管理 Skill
├── image-prompt-optimizer.md # 图片提示词优化 Skill（来自 aim-prompt/图片生成优化skill.md）
├── video-prompt-optimizer.md # 视频提示词优化 Skill（来自 aim-prompt/视频生成优化skill.md）
├── style-keeper.md           # 风格统一 Skill
└── episode-manager.md        # 集数管理 Skill
```

### 3.3 项目目录结构设计

```
.aim-studio/                    # 替代原 .trellis/
├── workflow.md                # 漫剧创作工作流指南
├── project.yaml               # 项目元数据（名称/类型/总集数等）
├── characters/                # 角色档案
│   ├── 主角-角色A.md
│   └── 配角-角色B.md
├── style/                     # 画风/风格定义
│   └── global-style.md
├── episodes/                  # 按集管理
│   ├── ep01/
│   │   ├── script.md          # 剧本
│   │   ├── storyboard.md      # 分镜表
│   │   ├── prompts/           # 生成的提示词
│   │   └── output/            # 生成的图片/视频
│   └── ep02/
└── templates/                 # 提示词模板
```

---

## 四、文件增删清单

### 4.1 需要删除的文件/目录
- `src/configurators/cursor.ts`
- `src/configurators/iflow.ts`
- `src/configurators/opencode.ts`
- `src/configurators/codex.ts`
- `src/templates/cursor/`（整个目录）
- `src/templates/iflow/`（整个目录）
- `src/templates/opencode/`（整个目录）
- `src/templates/codex/`（整个目录）
- `.cursor/`（整个目录）
- `.opencode/`（整个目录）
- `.agents/`（整个目录）
- `.github/`（如不需要）
- `CONTRIBUTING.md` / `CONTRIBUTING_CN.md`（个人项目不需要）
- `pyrightconfig.json`（Python 类型检查配置）

### 4.2 需要大幅修改的文件
- `package.json` — 改名/描述/keywords/bin 命令名
- `src/types/ai-tools.ts` — 精简为仅 Claude Code
- `src/configurators/index.ts` — 删除所有非 Claude 平台
- `src/commands/init.ts` — 简化初始化逻辑
- `src/commands/update.ts` — 简化更新逻辑
- `src/cli/index.ts` — 修改 CLI 入口
- `src/templates/extract.ts` — 精简模板提取
- `README.md` / `README_CN.md` — 全面重写
- `CLAUDE.md` — 重写为漫剧工具说明
- `AGENTS.md` — 重写或删除
- `bin/trellis.js` → 重命名为新 CLI 名称

### 4.3 需要新增的文件
- `.claude/skills/script-parser.md`
- `.claude/skills/storyboard-designer.md`
- `.claude/skills/character-manager.md`
- `.claude/skills/image-prompt-optimizer.md`
- `.claude/skills/video-prompt-optimizer.md`
- `.claude/skills/style-keeper.md`
- `.claude/skills/episode-manager.md`
- `src/templates/aim-studio/` — 新项目模板目录
- 新的 workflow.md 模板

### 4.4 保留但需调整内容的文件
- `src/configurators/claude.ts` — 保留结构，修改模板源
- `src/configurators/shared.ts` — 保留
- `src/configurators/workflow.ts` — 修改工作流内容
- `src/utils/` — 大部分保留（通用工具函数）
- `vitest.config.ts` — 保留
- `tsconfig.json` — 保留
- `eslint.config.js` — 保留
- `.prettierrc` — 保留

---

## 五、NPM 发布配置

```json
{
  "name": "@your-scope/aim-studio",
  "version": "0.1.0",
  "description": "AI 漫剧 & 连续剧生成工作流 CLI — 从剧本到分镜到成片",
  "bin": {
    "aim": "./bin/aim.js"
  },
  "keywords": [
    "ai", "comic", "drama", "video-generation", "image-generation",
    "storyboard", "prompt-engineering", "claude", "workflow"
  ],
  "files": ["dist", "bin", "README.md", "LICENSE"]
}
```

---

## 六、执行顺序建议

```
Phase 1 — 精简：删除非 Claude 平台代码  →  编译通过
Phase 2 — 改名：修改包名/CLI 命令/品牌  →  npm 可发布
Phase 3 — 注入：将 Skill 文件集成到模板系统  →  init 后可用
Phase 4 — 重写：README/CLAUDE.md/workflow  →  文档完整
Phase 5 — 验证：npm pack + 本地安装测试  →  确认可用
```

---

## 七、约束条件

1. **仅保留 Claude Code**：所有其他工具适配代码必须清除干净，不留死引用
2. **TypeScript 编译通过**：每次修改后 `pnpm build` 必须无错误
3. **测试更新**：删除涉及被删除平台的测试用例，补充新功能测试
4. **保留核心架构**：模板注入机制、init/update 命令、文件写入系统保留
5. **Skill 文件质量**：每个 Skill 必须是经过验证的、可直接注入 Claude 上下文的高质量 prompt
6. **中文优先**：所有面向用户的内容使用中文（代码注释可双语）

---

**本文档为项目转型的顶层指导，所有后续的具体 prompt 均基于本文档展开。**
