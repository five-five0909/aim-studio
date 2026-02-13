# 🤖 Claude Code Skill 适配 Prompt — 漫剧创作 Skill 编写规范

> **角色**：你是一个 Claude Code Skill 编写专家。你需要将漫剧创作工作流中的每个能力节点编写为高质量的 Claude Code Skill 文件，并通过 Trellis（改名后的工具）的模板系统注入。

---

## 一、Skill 编写铁律

### 1.1 什么是 Claude Code Skill？
Skill 是放置在 `.claude/skills/` 目录下的 Markdown 文件（或通过 commands/ 目录下的 Slash 命令触发），它们会在 Claude Code 会话中被加载为上下文，从而让 Claude 在特定任务上表现更专业。

### 1.2 Skill 必须满足的约束

| 约束 | 说明 |
| --- | --- |
| **自包含** | 每个 Skill 文件必须包含足够的上下文让 Claude 理解并执行任务，不依赖外部文档 |
| **结构化** | 使用清晰的标题/表格/代码块/检查清单组织内容 |
| **有示例** | 必须包含至少一个完整的输入→输出示例 |
| **有约束** | 明确列出 DO 和 DON'T，避免 AI 自由发挥导致质量波动 |
| **可测试** | Skill 输出的格式必须是可验证的（结构化 JSON/Markdown 表格等） |
| **长度适中** | 单个 Skill 文件建议 200-500 行，过长影响上下文窗口效率 |

### 1.3 Skill 标准模板

```markdown
# [Emoji] [Skill 名称]

## 技能标识
**名称**：`[snake_case_name]`
**版本**：1.0
**用途**：[一句话描述]
**依赖**：[需要的外部知识/文件]

---

## 一、输入规范
[详细描述输入格式和要素]

## 二、输出规范
[严格定义输出格式，包含模板]

## 三、核心规则
### 规则 1：[规则名]
[规则内容]
### 规则 2：[规则名]
[规则内容]
...

## 四、处理流程
1. [步骤1]
2. [步骤2]
...

## 五、完整示例
### 输入
> [示例输入]
### 输出
[示例输出]

## 六、自检清单
- [ ] [检查项1]
- [ ] [检查项2]
...

## 七、常见错误与规避
| 错误类型 | 规避方法 |
| --- | --- |
| ... | ... |
```

---

## 二、需要编写的 Skill 清单

### 2.1 已有 Skill（需迁移适配）

| # | Skill | 源文件 | 目标路径 | 改动 |
| --- | --- | --- | --- | --- |
| 1 | 图片提示词优化 | `aim-prompt/图片生成优化skill.md` | `.claude/skills/image-prompt-optimizer.md` | 补充角色卡注入机制 |
| 2 | 视频提示词优化 | `aim-prompt/视频生成优化skill.md` | `.claude/skills/video-prompt-optimizer.md` | 补充角色卡注入机制 |

**迁移改动要求**：
- 在输入规范中增加「角色卡」和「风格卡」注入接口
- 在输出中增加「角色锚点词」追加步骤
- 在自检清单中增加「角色一致性校验」项

### 2.2 需新建的 Skill

| # | Skill | 文件名 | 核心功能 |
| --- | --- | --- | --- |
| 3 | 剧本解析器 | `script-parser.md` | 将自由格式剧本解析为结构化场景 JSON |
| 4 | 分镜设计器 | `storyboard-designer.md` | 从场景列表生成专业分镜表 |
| 5 | 角色管理器 | `character-manager.md` | 创建/维护/查询角色一致性档案 |
| 6 | 风格守护者 | `style-keeper.md` | 维护全剧画风/色彩/渲染一致性 |
| 7 | 集数管理器 | `episode-manager.md` | 管理多集剧本/进度/产出 |

---

## 三、各 Skill 核心要求

### 3.1 剧本解析器 (`script-parser.md`)

**输入**：Markdown 格式的自由文本剧本
**输出**：结构化 scenes.json + 可读 scenes.md

**核心能力**：
- 自动识别场景切换点（地点变化/时间跳跃/情节转折）
- 角色识别与出场追踪
- 对话提取与情绪推断
- 旁白/叙述分离
- 视觉化描写提取

**约束**：
- 不改动原始剧本文字，只做结构化拆分
- 场景 ID 格式：`S01`, `S02`, ...
- 每个场景必须包含：ID / 标题 / 地点 / 时间 / 角色 / 动作 / 对话 / 情绪基调

### 3.2 分镜设计器 (`storyboard-designer.md`)

**输入**：scenes.json（解析后的场景列表）
**输出**：storyboard.md（分镜表）

**核心能力**：
- 将叙事场景转化为视觉镜头序列
- 自动选择景别（远/中/近/特写）和镜头运动
- 根据情绪基调选择构图策略
- 决定每个镜头的生成类型（图片 vs 视频）
- 估算时长

**约束**：
- 使用标准化镜头术语（参考视频 Skill 的规则4）
- 对话场景必须使用正反打结构
- 每个新场景必须以环境建立镜头开头
- 生成类型决策须有明确依据

### 3.3 角色管理器 (`character-manager.md`)

**输入**：角色基础信息（名字/性别/年龄/角色定位）
**输出**：完整角色卡（含外观特征/服装/表情映射/负面约束）

**核心能力**：
- 生成详细的外观锚点描述（AI 可复现的精确描写）
- 构建表情映射表（情绪→面部+身体语言）
- 生成多画风适配参考词
- 管理角色关系图

**约束**：
- 外观描述必须是「可复现的精确描写」，不允许模糊描述
- 每个特征必须是独特的、可区分的（避免两个角色描述太接近）
- 必须包含 Negative Prompt 锚点

### 3.4 风格守护者 (`style-keeper.md`)

**输入**：用户的风格偏好（文字描述或参考图片描述）
**输出**：完整风格卡（含画风/色彩/光影/锁定词/禁止词）

**核心能力**：
- 将模糊的风格偏好转化为精确的视觉参数
- 生成强制锁定词列表
- 生成全局禁止词列表
- 构建色彩情绪映射规则

**约束**：
- 锁定词必须是经过 AI 模型验证有效的高触发词
- 禁止词必须具体，不允许使用泛化词

### 3.5 集数管理器 (`episode-manager.md`)

**输入**：项目初始化信息 / 新集数请求 / 状态查询
**输出**：目录结构 / 状态报告 / 进度概览

**核心能力**：
- 创建标准化的集数目录结构
- 追踪每集的制作进度
- 统计角色出场情况
- 生成项目概览报告

---

## 四、Slash 命令编写规范

Slash 命令放置在 `.claude/commands/` 目录下，文件名即命令名。

### 4.1 命令文件模板

```markdown
---
description: [命令的一句话描述]
---

# [命令名]

## 执行步骤

1. [步骤1 — 明确指令]
2. [步骤2 — 明确指令]
...

## 输出格式
[指定输出的格式和位置]

## 约束
- [约束1]
- [约束2]
```

### 4.2 命令与 Skill 的关系

| 命令 | 调用的 Skill | 关系 |
| --- | --- | --- |
| `/aim:parse-script` | `script-parser.md` | 命令触发 → Skill 执行 |
| `/aim:storyboard` | `storyboard-designer.md` | 命令触发 → Skill 执行 |
| `/aim:prompts` | `image-prompt-optimizer.md` + `video-prompt-optimizer.md` | 命令触发 → 多 Skill 协调 |
| `/aim:new-character` | `character-manager.md` | 命令触发 → Skill 执行 |

**原则**：命令是"触发器 + 参数路由"，Skill 是"执行器 + 质量保障"。

---

## 五、Agent 定义改造

原 Trellis 的 Claude Agent 定义（`.claude/agents/` 下的 dispatch / implement / check / research）需要全面改造为漫剧创作相关 Agent。

### 新 Agent 设计

| Agent | 文件名 | 职责 |
| --- | --- | --- |
| 创作总监 | `director.md` | 路由用户请求，协调各 Skill 执行，做质量把关 |
| 编剧助手 | `writer.md` | 负责剧本解析、场景拆分、对话润色 |
| 分镜师 | `storyboard-artist.md` | 负责分镜设计、镜头语言、构图规划 |
| 提示词工程师 | `prompt-engineer.md` | 负责图片/视频提示词生成、角色注入、风格锁定 |

### Agent 文件模板

```markdown
---
name: [Agent 名称]
description: [Agent 职责描述]
skills:
  - [Skill 文件路径1]
  - [Skill 文件路径2]
---

# [Agent 名称]

## 你是谁
[身份定义]

## 你的职责
[明确的工作范围]

## 可用工具
[可以调用哪些 Skill]

## 工作流程
1. [收到请求后的处理流程]
2. ...

## 质量标准
[输出必须满足的最低标准]
```

---

## 六、模板系统对接

### 6.1 文件存放位置

所有 Skill / Command / Agent 模板文件存放在源代码的模板目录中：

```
src/templates/claude/
├── agents/
│   ├── director.md
│   ├── writer.md
│   ├── storyboard-artist.md
│   └── prompt-engineer.md
├── commands/
│   ├── aim/                   # 命名空间目录
│   │   ├── new-project.md
│   │   ├── new-episode.md
│   │   ├── new-character.md
│   │   ├── parse-script.md
│   │   ├── storyboard.md
│   │   ├── prompts.md
│   │   ├── prompts-image.md
│   │   ├── prompts-video.md
│   │   ├── status.md
│   │   └── export.md
├── hooks/
│   └── session-start.py       # 启动时注入上下文
├── skills/
│   ├── script-parser.md
│   ├── storyboard-designer.md
│   ├── character-manager.md
│   ├── image-prompt-optimizer.md
│   ├── video-prompt-optimizer.md
│   ├── style-keeper.md
│   └── episode-manager.md
└── settings.json
```

### 6.2 configureClaude() 函数适配

`src/configurators/claude.ts` 的 `configureClaude()` 函数负责将上述模板目录复制到用户项目的 `.claude/` 目录下。

需要确保：
- skills/ 目录被正确复制
- commands/ 子目录结构完整
- agents/ 新文件覆盖旧文件

---

## 七、Skill 质量检查清单

为每个 Skill 编写完成后检查：

- [ ] 是否包含技能标识（名称/版本/用途/依赖）？
- [ ] 是否有清晰的输入/输出规范？
- [ ] 是否包含至少一个完整的端到端示例？
- [ ] 是否有明确的 DO / DON'T 规则？
- [ ] 输出格式是否可机器解析（JSON/Markdown 表格）？
- [ ] 是否包含自检清单？
- [ ] 是否包含常见错误与规避方法的表格？
- [ ] 是否与角色卡/风格卡系统对接？
- [ ] 文件长度是否在 200-500 行之间？
- [ ] 是否使用中文编写（代码/技术术语可英文）？

---

**本 Prompt 为 Claude Code Skill 编写的具体规范，指导所有 Skill/Command/Agent 文件的创建。**
