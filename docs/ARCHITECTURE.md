# AIM Studio 架构设计文档

> 本文档详细记录 AIM Studio 项目的核心架构设计、巧妙实现和完整目录结构。

---

## 目录

1. [项目概览](#项目概览)
2. [架构设计亮点](#一架构设计亮点)
3. [完整项目结构](#二完整项目结构)
4. [关键设计决策](#三关键设计决策)
5. [扩展指南](#四扩展指南)
6. [测试策略](#五测试策略)
7. [命令与 Agent 参考](#六命令与-agent-参考)
8. [总结](#七总结)

---

## 项目概览

AIM Studio 是一个专为 AI 辅助漫剧/小说创作设计的 CLI 工具，支持多平台 AI 工具（Claude Code、OpenCode）。

**核心功能**：
- 🎬 漫剧/小说创作工作流
- 🤖 多 Agent 协作支持
- 📝 AI 绘画提示词生成
- ✅ 剧本逻辑检查与合规化
- 🔄 版本迁移与模板更新

---

## 一、架构设计亮点

### 1. 平台注册表模式 (Platform Registry Pattern)

**核心思想**：单一数据源驱动所有平台行为

```typescript
// src/types/ai-tools.ts - 平台配置注册表
export const AI_TOOLS: Record<AITool, AIToolConfig> = {
  "claude-code": {
    name: "Claude Code",
    templateDirs: ["common", "claude"],  // 模板目录顺序
    configDir: ".claude",                 // 项目中的配置目录
    cliFlag: "claude",                    // CLI 标志 --claude
    defaultChecked: true,                 // init 时默认选中
    hasPythonHooks: true,                 // 是否有 Python hooks
  },
  opencode: {
    name: "OpenCode",
    templateDirs: ["common", "opencode"],
    configDir: ".opencode",
    cliFlag: "opencode",
    defaultChecked: false,
    hasPythonHooks: false,
  },
};
```

**巧妙之处**：
- 所有平台元数据集中在一处定义
- 衍生功能自动生成，无需重复维护
- 新增平台只需添加配置，无需修改业务逻辑

**自动衍生的工具函数**：

```typescript
// src/configurators/index.ts - 从注册表自动派生
export const PLATFORM_IDS = Object.keys(AI_TOOLS) as AITool[];
export const CONFIG_DIRS = PLATFORM_IDS.map((id) => AI_TOOLS[id].configDir);
export const ALL_MANAGED_DIRS = [".aim-studio", ...CONFIG_DIRS];

// 检测已配置的平台
export function getConfiguredPlatforms(cwd: string): Set<AITool> {
  const platforms = new Set<AITool>();
  for (const id of PLATFORM_IDS) {
    if (fs.existsSync(path.join(cwd, AI_TOOLS[id].configDir))) {
      platforms.add(id);
    }
  }
  return platforms;
}

// CLI 标志解析
export function resolveCliFlag(flag: string): AITool | undefined {
  return PLATFORM_IDS.find((id) => AI_TOOLS[id].cliFlag === flag);
}
```

---

### 2. 模板哈希追踪系统 (Template Hash Tracking)

**核心思想**：精确区分"用户修改"与"模板更新"

```
┌─────────────────────────────────────────────────────────────┐
│                    Hash 追踪决策树                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  文件内容 vs 模板内容                                        │
│       │                                                     │
│       ├── 相同 → unchangedFiles (跳过)                      │
│       │                                                     │
│       └── 不同 → 检查存储的 Hash                            │
│                    │                                        │
│                    ├── Hash 匹配 → autoUpdateFiles (自动更新)│
│                    │   (用户未修改，模板已更新)              │
│                    │                                        │
│                    └── Hash 不匹配 → changedFiles (需确认)  │
│                        (用户已修改，需用户决策)              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**实现细节** (`src/utils/template-hash.ts`)：

```typescript
// 存储 Hash 的文件位置
const HASHES_FILE = ".template-hashes.json";

// 计算 SHA256 Hash
export function computeHash(content: string): string {
  return createHash("sha256").update(content, "utf-8").digest("hex");
}

// 检测文件是否被用户修改
export function isTemplateModified(
  cwd: string,
  relativePath: string,
  hashes: TemplateHashes,
): boolean {
  const storedHash = hashes[relativePath];
  if (!storedHash) return true; // 无记录则保守处理（视为已修改）
  
  const currentHash = computeHash(fs.readFileSync(fullPath, "utf-8"));
  return currentHash !== storedHash;
}

// 初始化 Hash（在 aim init 后调用）
export function initializeHashes(cwd: string): number {
  const hashes: TemplateHashes = {};
  for (const dir of TEMPLATE_DIRS) {
    const files = collectFiles(cwd, dir);
    for (const relativePath of files) {
      const content = fs.readFileSync(fullPath, "utf-8");
      // 路径标准化（Windows 兼容）
      const portablePath = relativePath.split(path.sep).join("/");
      hashes[portablePath] = computeHash(content);
    }
  }
  saveHashes(cwd, hashes);
  return Object.keys(hashes).length;
}
```

**排除追踪的文件**：

```typescript
const EXCLUDE_FROM_HASH = [
  ".template-hashes.json",  // Hash 文件本身
  ".version",               // 版本文件
  ".gitignore",             // Git 忽略文件
  ".developer",             // 开发者身份文件
  "workspace/",             // 工作区（用户数据）
  "tasks/",                 // 任务数据（用户数据）
  ".current-task",          // 当前任务标记
  "spec/frontend/",         // 前端规范（用户填写）
  "spec/backend/",          // 后端规范（用户填写）
  ".backup-",               // 备份目录
];
```

**巧妙之处**：
- 解决了 CLI 工具更新时的"冲突检测"难题
- 用户修改过的文件会被保护，未修改的自动更新
- 支持 Windows/macOS/Linux 跨平台路径兼容
- 首次更新时提示用户，避免误判

---

### 3. 版本迁移系统 (Version Migration System)

**核心思想**：声明式迁移清单，自动聚合执行

```
src/migrations/
├── index.ts              # 迁移引擎
└── manifests/            # 版本迁移清单 (JSON)
    ├── 0.0.1.json
    ├── 0.1.9.json
    ├── 0.2.0.json
    ├── 0.2.12.json
    ├── 0.2.13.json
    ├── 0.2.14.json
    ├── 0.2.15.json
    ├── 0.3.0-beta.0.json
    ├── 0.3.0-beta.1.json
    ├── ... (更多 beta 版本)
    ├── 0.3.0-rc.0.json
    └── 0.3.0-rc.1.json
```

**迁移清单结构** (`manifests/*.json`)：

```json
{
  "version": "0.2.0",
  "changelog": "重命名 traces 文件为 journal",
  "breaking": true,
  "recommendMigrate": true,
  "migrationGuide": "将 workspace/*/traces-*.md 重命名为 journal-*.md",
  "aiInstructions": "检查 workspace 目录下的所有 traces 文件...",
  "migrations": [
    { "type": "rename", "from": "old/path.md", "to": "new/path.md" },
    { "type": "delete", "from": "deprecated/file.py" },
    { "type": "rename-dir", "from": "old/dir", "to": "new/dir" }
  ]
}
```

**迁移类型**：

| 类型 | 说明 | 示例 |
|------|------|------|
| `rename` | 重命名单个文件 | 旧路径 → 新路径 |
| `delete` | 删除废弃文件 | 删除指定文件 |
| `rename-dir` | 重命名整个目录 | 包含所有子文件 |

**迁移引擎核心逻辑** (`src/migrations/index.ts`)：

```typescript
// 获取版本区间内的所有迁移
export function getMigrationsForVersion(
  fromVersion: string,
  toVersion: string
): MigrationItem[] {
  const manifests = loadManifests();
  const versions = Object.keys(manifests).sort(compareVersions);
  
  // 筛选：fromVersion < v <= toVersion
  const applicableVersions = versions.filter((v) => {
    const afterFrom = compareVersions(v, fromVersion) > 0;
    const atOrBeforeTo = compareVersions(v, toVersion) <= 0;
    return afterFrom && atOrBeforeTo;
  });
  
  // 聚合所有迁移项
  return applicableVersions.flatMap(v => manifests[v].migrations);
}

// 获取迁移元数据（changelog、breaking 等）
export function getMigrationMetadata(fromVersion: string, toVersion: string) {
  // 聚合所有版本的 changelog、breaking 状态、迁移指南
  return {
    changelog: string[],           // 变更日志
    breaking: boolean,             // 是否有破坏性变更
    recommendMigrate: boolean,     // 是否推荐使用 --migrate
    migrationGuides: Array<{       // 迁移指南
      version: string;
      guide: string;
      aiInstructions?: string;
    }>;
  };
}
```

**迁移分类执行**：

```typescript
// 迁移分类
interface ClassifiedMigrations {
  auto: MigrationItem[];      // 自动执行（未修改的文件）
  confirm: MigrationItem[];   // 需确认（用户修改过）
  conflict: MigrationItem[];  // 冲突（新旧都存在）
  skip: MigrationItem[];      // 跳过（旧文件不存在）
}

// 执行顺序：rename-dir → rename/delete
// 按路径深度排序：深层目录优先
export function sortMigrationsForExecution(migrations: MigrationItem[]) {
  return [...migrations].sort((a, b) => {
    if (a.type === "rename-dir" && b.type === "rename-dir") {
      const aDepth = a.from.split("/").length;
      const bDepth = b.from.split("/").length;
      return bDepth - aDepth; // 深层优先
    }
    if (a.type === "rename-dir") return -1;
    if (b.type === "rename-dir") return 1;
    return 0;
  });
}
```

**孤儿迁移检测**：

```typescript
// 检测上次未执行的迁移
const orphanedMigrations = allMigrations.filter((item) => {
  const sourceExists = fs.existsSync(oldPath);
  const targetExists = fs.existsSync(newPath);
  const alreadyPending = pendingMigrations.some(
    (m) => m.from === item.from && m.to === item.to
  );
  
  // 源存在 && 目标不存在 && 未在待处理列表
  return sourceExists && !targetExists && !alreadyPending;
});
```

**巧妙之处**：
- 跳版本升级自动聚合所有中间版本的迁移
- 孤儿迁移检测：发现未执行的迁移并补全
- 迁移分类：自动/确认/冲突/跳过
- 支持语义化版本（beta、rc 等）

---

### 4. 动态模板加载 (Dynamic Template Loading)

**核心思想**：约定优于配置，自动发现模板文件

```typescript
// src/templates/claude/index.ts
export function getAllCommands(): CommandTemplate[] {
  const commands: CommandTemplate[] = [];
  const files = listFiles("commands/aim"); // 自动扫描目录

  for (const file of files) {
    if (file.endsWith(".md")) {
      const name = file.replace(".md", "");      // 文件名即命令名
      const content = readTemplate(`commands/aim/${file}`);
      commands.push({ name, content });
    }
  }
  return commands;
}

export function getAllAgents(): AgentTemplate[] {
  const agents: AgentTemplate[] = [];
  const files = listFiles("agents");

  for (const file of files) {
    if (file.endsWith(".md")) {
      const name = file.replace(".md", "");
      const content = readTemplate(`agents/${file}`);
      agents.push({ name, content });
    }
  }
  return agents;
}

// Skills 使用目录结构
export function getAllSkills(): SkillTemplate[] {
  const skills: SkillTemplate[] = [];
  const skillDirs = listFiles("skills");

  for (const dir of skillDirs) {
    const skillFile = `skills/${dir}/SKILL.md`;
    try {
      const content = readTemplate(skillFile);
      skills.push({ name: dir, content });
    } catch {
      // 跳过没有 SKILL.md 的目录
    }
  }
  return skills;
}
```

**巧妙之处**：
- 新增命令/Agent 只需添加文件，无需修改代码
- 文件名即命令名（`start.md` → `/aim:start`）
- 构建时通过 `scripts/copy-templates.js` 自动打包到 dist

---

### 5. 多平台格式适配 (Multi-Platform Format Adaptation)

**核心发现**：Claude Code 与 OpenCode 使用不同的模板格式

| 特性 | Claude Code | OpenCode |
|------|-------------|----------|
| **Commands frontmatter** | 需要 `name` + `description` | 不需要 |
| **Agents frontmatter** | `name`, `description`, `tools`, `model` | `description`, `mode`, `permission` |
| **Hooks** | Python 脚本 (`*.py`) | JavaScript (`*.js`) |
| **配置文件** | `settings.json` | `lib/` + `plugin/` |

**解决方案**：独立模板目录，格式各不相同

```
templates/
├── common/           # 共享资源（暂未使用）
├── claude/           # Claude Code 格式
│   ├── commands/aim/ # 带 frontmatter
│   ├── agents/       # Claude frontmatter 格式
│   ├── hooks/        # Python hooks
│   ├── skills/       # 技能定义
│   └── settings.json # 设置模板
└── opencode/         # OpenCode 格式
    ├── commands/aim/ # 无 frontmatter
    ├── agents/       # OpenCode frontmatter 格式
    ├── lib/          # JavaScript 库
    └── plugin/       # JavaScript 插件
```

**Claude Code Command 格式**：

```markdown
---
name: start
description: 开始 AIM Studio 漫剧创作会话
---

# 开始会话

初始化 AIM Studio 漫剧创作会话...
```

**OpenCode Command 格式**（无 frontmatter）：

```markdown
# 开始会话

初始化 AIM Studio 漫剧创作会话...
```

**Claude Code Agent 格式**：

```markdown
---
name: director
description: 总导演 Agent
tools: Read, Write, Bash
model: opus
---

# 总导演

负责整体创作方向和风格把控...
```

**OpenCode Agent 格式**：

```markdown
---
description: 总导演 Agent
mode: primary
permission:
  read: allow
  write: allow
  bash: allow
---

# 总导演

负责整体创作方向和风格把控...
```

---

### 6. 智能更新流程 (Smart Update Flow)

**核心思想**：三层防护 + 智能决策

```
┌─────────────────────────────────────────────────────────────┐
│                    Update 执行流程                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 版本检查                                                │
│     ├── CLI < npm → 提示更新 CLI                            │
│     ├── CLI < project → 禁止降级（除非 --allow-downgrade）  │
│     └── CLI > project → 执行升级                            │
│                                                             │
│  2. 迁移分析                                                │
│     ├── 加载版本区间内的所有迁移                            │
│     ├── 检测孤儿迁移（上次未执行的）                        │
│     └── 分类：auto/confirm/conflict/skip                    │
│                                                             │
│  3. 变更分析 (Hash 追踪)                                     │
│     ├── 新文件 → 直接添加                                   │
│     ├── 未修改 + 模板更新 → 自动更新                        │
│     └── 用户修改 → 交互确认                                 │
│                                                             │
│  4. 备份机制                                                │
│     └── 创建时间戳备份目录 .backup-{timestamp}/             │
│                                                             │
│  5. 执行变更                                                │
│     ├── 添加新文件                                          │
│     ├── 自动更新模板                                        │
│     ├── 处理用户确认（overwrite/skip/create-new）          │
│     └── 更新 Hash 记录                                      │
│                                                             │
│  6. 创建迁移任务（如有破坏性变更）                           │
│     └── 在 tasks/ 目录创建迁移指南                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**更新命令选项**：

```bash
aim update                  # 交互式更新
aim update --dry-run        # 预览变更
aim update -f               # 强制覆盖所有
aim update -s               # 跳过所有冲突
aim update -n               # 创建 .new 副本
aim update --migrate        # 执行迁移
aim update --allow-downgrade # 允许降级
```

**变更分析核心逻辑** (`src/commands/update.ts`)：

```typescript
function analyzeChanges(
  cwd: string,
  hashes: TemplateHashes,
  templates: Map<string, string>,
): ChangeAnalysis {
  const result: ChangeAnalysis = {
    newFiles: [],        // 新文件
    unchangedFiles: [],  // 未变更
    autoUpdateFiles: [], // 自动更新（用户未修改）
    changedFiles: [],    // 需确认（用户修改过）
    protectedPaths: [],  // 保护路径
  };

  for (const [relativePath, newContent] of templates) {
    const exists = fs.existsSync(fullPath);
    
    if (!exists) {
      result.newFiles.push(change);
    } else {
      const existingContent = fs.readFileSync(fullPath, "utf-8");
      if (existingContent === newContent) {
        result.unchangedFiles.push(change);
      } else {
        const storedHash = hashes[relativePath];
        const currentHash = computeHash(existingContent);
        
        if (storedHash && storedHash === currentHash) {
          // Hash 匹配：用户未修改，模板更新了
          result.autoUpdateFiles.push(change);
        } else {
          // Hash 不匹配：用户修改过
          result.changedFiles.push(change);
        }
      }
    }
  }
  return result;
}
```

---

### 7. Python 脚本系统 (Python Script System)

**核心设计**：模块化 Python 工具库

```
src/templates/aim/scripts/
├── __init__.py              # 包初始化
├── common/                  # 共享工具模块
│   ├── __init__.py
│   ├── paths.py            # 路径常量
│   ├── developer.py        # 开发者身份管理
│   ├── git_context.py      # Git 上下文获取
│   ├── worktree.py         # Git Worktree 管理
│   ├── task_queue.py       # 任务队列
│   ├── task_utils.py       # 任务工具函数
│   ├── phase.py            # 开发阶段管理
│   ├── registry.py         # 注册表
│   └── cli_adapter.py      # CLI 适配器
├── multi_agent/             # 多 Agent 协作
│   ├── __init__.py
│   ├── start.py            # 启动 Agent
│   ├── cleanup.py          # 清理环境
│   ├── status.py           # 状态查询
│   ├── create_pr.py        # 创建 PR
│   └── plan.py             # 任务规划
└── *.py                     # 主脚本
    ├── get_developer.py    # 获取当前开发者
    ├── init_developer.py   # 初始化开发者
    ├── task.py             # 任务管理
    ├── get_context.py      # 获取上下文
    ├── add_session.py      # 添加会话记录
    ├── create_bootstrap.py # 创建引导脚本
    └── export.py           # 导出功能
```

**Python 与 TypeScript 交互**：

```typescript
// src/configurators/shared.ts
export function resolvePlaceholders(content: string): string {
  // 解析 {{PYTHON_CMD}} 占位符
  const pythonCmd = process.platform === "win32" ? "python" : "python3";
  return content.replace(/\{\{PYTHON_CMD\}\}/g, pythonCmd);
}
```

**Windows 编码处理**：

```python
# scripts/common/cli_adapter.py
import sys

# Windows 控制台编码修复
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
```

**巧妙之处**：
- TypeScript CLI 调用 Python 脚本实现复杂逻辑
- 模块化设计便于复用和测试
- 支持 Windows Python 编码自动检测

---

### 8. 远程模板支持 (Remote Template Support)

**核心思想**：支持从远程仓库拉取项目模板

```typescript
// src/commands/init.ts
import { downloadTemplate } from "giget";

async function downloadRemoteTemplate(templateName: string, targetDir: string) {
  // 支持 GitHub、GitLab 等多种源
  const { dir } = await downloadTemplate(
    `gh:aim-studio/templates/${templateName}`,
    { dir: targetDir, force: true }
  );
  return dir;
}
```

**使用方式**：

```bash
aim init -t electron-fullstack  # 拉取 electron 全栈模板
aim init -t nextjs-saas         # 拉取 Next.js SaaS 模板
aim init -t flask-api           # 拉取 Flask API 模板
```

**模板选项**：

| 选项 | 说明 |
|------|------|
| `-t, --template <name>` | 使用远程模板 |
| `--overwrite` | 覆盖现有 spec 目录 |
| `--append` | 只添加缺失文件 |

---

## 二、完整项目结构

```
aim-studio/
├── 📁 src/                          # 源代码目录
│   │
│   ├── 📁 cli/                      # CLI 入口
│   │   └── 📄 index.ts              # Commander 命令定义
│   │       └── 命令: aim init, aim update
│   │       └── 版本检查、更新提示
│   │
│   ├── 📁 commands/                 # 命令实现
│   │   ├── 📄 init.ts               # aim init 实现
│   │   │   ├── 交互式平台选择
│   │   │   ├── 远程模板下载
│   │   │   ├── 开发者身份初始化
│   │   │   └── Hash 初始化
│   │   └── 📄 update.ts             # aim update 实现
│   │       ├── 版本比较
│   │       ├── 迁移分析
│   │       ├── 变更分析
│   │       ├── 备份创建
│   │       └── 迁移任务生成
│   │
│   ├── 📁 configurators/            # 平台配置器
│   │   ├── 📄 index.ts              # 平台注册表 (核心!)
│   │   │   ├── PLATFORM_FUNCTIONS
│   │   │   ├── getConfiguredPlatforms()
│   │   │   ├── configurePlatform()
│   │   │   └── collectPlatformTemplates()
│   │   ├── 📄 claude.ts             # Claude Code 配置
│   │   │   └── configureClaude()
│   │   ├── 📄 opencode.ts           # OpenCode 配置
│   │   │   └── configureOpencode()
│   │   ├── 📄 shared.ts             # 共享工具
│   │   │   └── resolvePlaceholders()
│   │   └── 📄 workflow.ts           # 工作流配置
│   │
│   ├── 📁 templates/                # 模板文件 (核心!)
│   │   │
│   │   ├── 📁 aim/                  # AIM 工作流模板
│   │   │   ├── 📁 scripts/          # Python 脚本
│   │   │   │   ├── 📁 common/       # 共享模块 (10个文件)
│   │   │   │   ├── 📁 multi_agent/  # 多 Agent 脚本 (6个文件)
│   │   │   │   └── 📄 *.py          # 主脚本 (7个文件)
│   │   │   ├── 📁 tasks/            # 任务目录模板
│   │   │   ├── 📄 workflow.md       # 工作流指南
│   │   │   ├── 📄 worktree.yaml     # Worktree 配置
│   │   │   └── 📄 gitignore.txt     # Git 忽略规则
│   │   │
│   │   ├── 📁 claude/               # Claude Code 模板
│   │   │   ├── 📁 commands/aim/     # 命令模板 (10个)
│   │   │   │   ├── 📄 start.md      # 开始会话
│   │   │   │   ├── 📄 story.md      # 漫剧创作
│   │   │   │   ├── 📄 finish-work.md
│   │   │   │   ├── 📄 portrait.md   # 角色肖像
│   │   │   │   ├── 📄 visualize.md  # 场景图片
│   │   │   │   ├── 📄 check-story.md
│   │   │   │   ├── 📄 export.md
│   │   │   │   ├── 📄 legitimize.md
│   │   │   │   ├── 📄 onboard.md
│   │   │   │   └── 📄 record-session.md
│   │   │   ├── 📁 agents/           # Agent 模板 (5个)
│   │   │   │   ├── 📄 director.md   # 总导演
│   │   │   │   ├── 📄 writer.md     # 编剧
│   │   │   │   ├── 📄 storyboard-artist.md
│   │   │   │   ├── 📄 prompt-engineer.md
│   │   │   │   └── 📄 story.md
│   │   │   ├── 📁 hooks/            # Python Hooks (2个)
│   │   │   │   ├── 📄 inject-subagent-context.py
│   │   │   │   └── 📄 session-start.py
│   │   │   ├── 📁 skills/           # 技能定义 (7个)
│   │   │   │   ├── 📁 character-manager/
│   │   │   │   ├── 📁 episode-manager/
│   │   │   │   ├── 📁 image-prompt-optimizer/
│   │   │   │   ├── 📁 script-parser/
│   │   │   │   ├── 📁 storyboard-designer/
│   │   │   │   ├── 📁 style-keeper/
│   │   │   │   └── 📁 video-prompt-optimizer/
│   │   │   ├── 📄 settings.json     # 设置模板
│   │   │   └── 📄 index.ts          # 模板加载器
│   │   │
│   │   ├── 📁 opencode/             # OpenCode 模板
│   │   │   ├── 📁 commands/aim/     # 命令模板 (10个，同 claude)
│   │   │   ├── 📁 agents/           # Agent 模板 (5个)
│   │   │   ├── 📁 lib/              # JavaScript 库
│   │   │   │   └── 📄 aim-context.js
│   │   │   ├── 📁 plugin/           # JavaScript 插件
│   │   │   │   └── 📄 session-start.js
│   │   │   └── 📄 index.ts          # 模板加载器
│   │   │
│   │   ├── 📁 markdown/             # Markdown 模板
│   │   │   ├── 📁 spec/story/       # Story 规范模板
│   │   │   │   ├── 📄 index.md.txt
│   │   │   │   ├── 📄 character.md.txt
│   │   │   │   ├── 📄 world.md.txt
│   │   │   │   ├── 📄 script.md.txt
│   │   │   │   └── 📄 style-guide.md.txt
│   │   │   ├── 📄 workspace-index.md
│   │   │   ├── 📄 agents.md
│   │   │   └── 📄 index.ts
│   │   │
│   │   ├── 📄 index.ts              # 模板入口
│   │   ├── 📄 extract.ts            # 模板提取工具
│   │   └── 📄 CLAUDE.md             # Claude 模板说明
│   │
│   ├── 📁 migrations/               # 迁移系统
│   │   ├── 📄 index.ts              # 迁移引擎
│   │   │   ├── loadManifests()
│   │   │   ├── getMigrationsForVersion()
│   │   │   ├── getMigrationMetadata()
│   │   │   └── getAllMigrations()
│   │   └── 📁 manifests/            # 版本迁移清单 (27个)
│   │       ├── 📄 0.0.1.json
│   │       ├── 📄 0.1.9.json
│   │       ├── 📄 0.2.0.json
│   │       ├── ...
│   │       └── 📄 0.3.0-rc.1.json
│   │
│   ├── 📁 utils/                    # 工具函数
│   │   ├── 📄 template-hash.ts      # Hash 追踪系统
│   │   │   ├── computeHash()
│   │   │   ├── loadHashes()
│   │   │   ├── saveHashes()
│   │   │   ├── isTemplateModified()
│   │   │   └── initializeHashes()
│   │   ├── 📄 compare-versions.ts   # 版本比较
│   │   ├── 📄 file-writer.ts        # 文件写入
│   │   ├── 📄 project-detector.ts   # 项目检测
│   │   └── 📄 template-fetcher.ts   # 模板获取
│   │
│   ├── 📁 types/                    # 类型定义
│   │   ├── 📄 ai-tools.ts           # AI 工具类型
│   │   │   ├── AITool
│   │   │   ├── AIToolConfig
│   │   │   └── AI_TOOLS (注册表)
│   │   └── 📄 migration.ts          # 迁移类型
│   │       ├── MigrationItem
│   │       ├── MigrationManifest
│   │       ├── ClassifiedMigrations
│   │       └── TemplateHashes
│   │
│   ├── 📁 constants/                # 常量定义
│   │   ├── 📄 paths.ts              # 路径常量
│   │   │   ├── DIR_NAMES
│   │   │   └── PATHS
│   │   └── 📄 version.ts            # 版本常量
│   │       ├── VERSION
│   │       └── PACKAGE_NAME
│   │
│   └── 📄 index.ts                  # 包入口
│
├── 📁 bin/                          # CLI 入口
│   └── 📄 aim.js                    # #!/usr/bin/env node
│
├── 📁 scripts/                      # 构建脚本
│   ├── 📄 copy-templates.js         # 复制模板到 dist
│   ├── 📄 create-manifest.js        # 创建 manifest
│   └── 📄 release.sh                # 发布脚本
│
├── 📁 test/                         # 测试文件
│   ├── 📄 template-hash.test.ts
│   ├── 📄 migrations.test.ts
│   └── ... (16个测试文件)
│
├── 📁 docs/                         # 文档目录
│   └── 📄 ARCHITECTURE.md           # 本文档
│
├── 📁 dist/                         # 编译输出
│
├── 📄 package.json                  # 包配置
├── 📄 tsconfig.json                 # TypeScript 配置
├── 📄 vitest.config.ts              # 测试配置
├── 📄 eslint.config.js              # ESLint 配置
├── 📄 pyrightconfig.json            # Python 类型检查配置
├── 📄 README.md                     # 项目说明
├── 📄 CLAUDE.md                     # Claude Code 说明
├── 📄 CONTRIBUTING.md               # 贡献指南
└── 📄 LICENSE                       # 许可证
```

---

## 三、关键设计决策

### 1. 为什么选择 TypeScript + Python 混合架构？

| 技术 | 用途 | 原因 |
|------|------|------|
| **TypeScript** | CLI 核心 | 类型安全、npm 生态、跨平台、Commander.js |
| **Python** | 复杂脚本 | AI 工具原生支持、文本处理能力强、Git 操作便捷 |

**调用方式**：

```
TypeScript CLI  ──调用──>  Python 脚本
     │                         │
     │                         ├── 复杂的 Git 操作
     │                         ├── 文本解析与生成
     │                         └── AI 工具集成
     │
     └── 控制流程、用户交互、模板管理
```

### 2. 为什么模板不能共享？

两个平台的格式差异太大：

| 差异点 | Claude Code | OpenCode |
|--------|-------------|----------|
| **Commands** | 需要 frontmatter | 不需要 frontmatter |
| **Agents 权限** | `tools` + `model` | `mode` + `permission` |
| **Hooks** | Python (`*.py`) | JavaScript (`*.js`) |
| **配置** | `settings.json` | `lib/` + `plugin/` |

强行共享会导致代码复杂度急剧上升，维护两套模板更清晰。

### 3. 为什么使用 JSON 存储迁移清单？

- ✅ 可读性好，易于人工编辑
- ✅ 版本控制友好（diff 清晰）
- ✅ 无需重新编译即可添加新迁移
- ✅ 便于自动化工具生成
- ✅ 支持注释以外的所有 JSON 特性

### 4. 为什么使用 Hash 追踪而不是 Git diff？

| 方案 | 优点 | 缺点 |
|------|------|------|
| **Git diff** | 原生支持 | 依赖 Git、无法区分模板版本 |
| **Hash 追踪** | 精确检测、跨版本 | 需要额外存储 |

Hash 追踪可以精确区分：
- 用户修改了文件
- 模板更新了但用户未修改
- 两者都修改了

---

## 四、扩展指南

### 添加新的 AI 平台

1. **在 `src/types/ai-tools.ts` 添加类型**：

```typescript
export type AITool = "claude-code" | "opencode" | "new-tool";
export type CliFlag = "claude" | "opencode" | "new-tool";
```

2. **在 `src/types/ai-tools.ts` 添加配置**：

```typescript
export const AI_TOOLS: Record<AITool, AIToolConfig> = {
  // ... 现有平台
  "new-tool": {
    name: "New Tool",
    templateDirs: ["common", "new-tool"],
    configDir: ".new-tool",
    cliFlag: "new-tool",
    defaultChecked: false,
    hasPythonHooks: false,
  },
};
```

3. **创建模板目录** `src/templates/new-tool/`

4. **创建配置器** `src/configurators/new-tool.ts`

5. **在 `src/configurators/index.ts` 注册**

### 添加新命令

1. 在 `src/templates/claude/commands/aim/` 创建 `{name}.md`（带 frontmatter）
2. 在 `src/templates/opencode/commands/aim/` 创建 `{name}.md`（无 frontmatter）
3. 构建后自动可用

### 添加新 Agent

同命令流程，放到 `agents/` 目录。

### 添加新迁移

在 `src/migrations/manifests/` 创建 `{version}.json`：

```json
{
  "version": "0.4.0",
  "changelog": "描述变更内容",
  "breaking": false,
  "recommendMigrate": false,
  "migrations": [
    { "type": "rename", "from": "old/path", "to": "new/path" }
  ]
}
```

---

## 五、测试策略

```bash
pnpm test              # 运行所有测试
pnpm test:watch        # 监听模式
pnpm test:coverage     # 覆盖率报告
```

**测试文件** (`test/`)：

| 文件 | 测试内容 |
|------|----------|
| `template-hash.test.ts` | Hash 计算、修改检测 |
| `migrations.test.ts` | 迁移聚合、版本比较 |
| `compare-versions.test.ts` | 版本比较逻辑 |
| `init.test.ts` | init 命令流程 |
| `update.test.ts` | update 命令流程 |

---

## 六、命令与 Agent 参考

### 命令列表

| 命令 | 描述 | 分类 |
|------|------|------|
| `/aim:start` | 开始 AIM Studio 漫剧创作会话 | 工作流 |
| `/aim:story` | 启动漫剧创作模式 | 工作流 |
| `/aim:finish-work` | 完成创作并记录工作 | 工作流 |
| `/aim:portrait` | 生成角色肖像提示词 | 内容生成 |
| `/aim:visualize` | 生成场景图片提示词 | 内容生成 |
| `/aim:check-story` | 检查剧情一致性与逻辑 | 质量检查 |
| `/aim:legitimize` | 检查并合法化剧本 | 质量检查 |
| `/aim:export` | 导出剧本用于AI视频生成 | 导出 |
| `/aim:onboard` | 项目入门引导 | 协作 |
| `/aim:record-session` | 记录创作会话 | 协作 |

### Agent 列表

| Agent | 描述 | 技能 |
|-------|------|------|
| `director` | 总导演 | 整体方向、风格把控 |
| `writer` | 编剧 | 剧本创作、对话设计 |
| `storyboard-artist` | 分镜师 | 分镜设计、镜头语言 |
| `prompt-engineer` | 提示词工程师 | AI 提示词优化 |
| `story` | 故事 Agent | 故事结构、情节发展 |

### Skill 列表 (Claude Code)

| Skill | 描述 |
|-------|------|
| `character-manager` | 角色管理 |
| `episode-manager` | 剧集管理 |
| `image-prompt-optimizer` | 图片提示词优化 |
| `script-parser` | 剧本解析 |
| `storyboard-designer` | 分镜设计 |
| `style-keeper` | 风格保持 |
| `video-prompt-optimizer` | 视频提示词优化 |

---

## 七、总结

AIM Studio 的核心设计理念：

| 设计原则 | 实现方式 | 价值 |
|----------|----------|------|
| **单一数据源** | 平台注册表驱动 | 易扩展、无冗余 |
| **智能变更检测** | Hash 追踪 | 保护用户修改 |
| **声明式迁移** | JSON 清单 | 版本升级无痛 |
| **约定优于配置** | 自动发现模板 | 零配置添加功能 |
| **平台适配隔离** | 独立模板目录 | 清晰维护边界 |

这些设计使得 AIM Studio 具有良好的：
- ✅ **可扩展性**：新增平台/命令只需添加配置和文件
- ✅ **可维护性**：模块化设计，职责清晰
- ✅ **用户体验**：智能检测、安全更新、友好提示
- ✅ **跨平台**：Windows/macOS/Linux 一致体验
