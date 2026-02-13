---
name: start
description: 开始 AIM Studio 开发会话
---

# 开始会话

初始化 AIM Studio 开发会话，开始你的开发工作。

---

## 适用场景

- 首次开始项目开发
- 开始新的开发会话
- 想要了解当前项目状态

---

## 使用步骤

### 步骤 1：理解工作流

首先阅读工作流指南：

```bash
cat .aim-studio/workflow.md
```

**遵循 workflow.md 中的指导**，包含：
- 核心原则（先读后写、遵循规范等）
- 文件系统结构
- 开发流程
- 最佳实践

### 步骤 2：获取当前上下文

```bash
python3 .aim-studio/scripts/get_context.py
```

或者查看项目状态：

```bash
python3 .aim-studio/scripts/task.py status
```

显示：项目状态、当前任务（如有）、活跃任务列表。

### 步骤 3：阅读开发规范

根据项目类型，阅读相应的规范：

**如果是 CLI 项目**：
```bash
cat .aim-studio/spec/cli/index.md           # CLI 开发规范
cat .aim-studio/spec/cli/directory-structure.md
```

**如果是前端项目**：
```bash
cat .aim-studio/spec/frontend/index.md     # 前端开发规范
cat .aim-studio/spec/frontend/component-guidelines.md
```

**如果是后端项目**：
```bash
cat .aim-studio/spec/backend/index.md      # 后端开发规范
cat .aim-studio/spec/backend/directory-structure.md
```

**如果是全栈项目**：
```bash
cat .aim-studio/spec/frontend/index.md
cat .aim-studio/spec/backend/index.md
```

**如果是漫剧创作项目**：
```bash
cat .aim-studio/spec/story/script.md       # 剧本与分镜规范
cat .aim-studio/spec/story/character.md    # 角色设定规范
cat .aim-studio/spec/story/world.md        # 世界观设定规范
```

### 步骤 4：检查当前任务

查看是否有待完成的任务：

```bash
python3 .aim-studio/scripts/task.py list
```

如果有任务，查看任务详情：
```bash
python3 .aim-studio/scripts/task.py show <任务名>
```

### 步骤 5：开始工作

报告你了解到的内容，询问用户："您好！请问今天需要做什么？"

---

## 任务分类

当用户描述任务时，进行分类：

| 类型 | 标准 | 处理方式 |
|------|------|----------|
| 问题 | 用户询问关于项目的问题 | 直接回答 |
| 简单修改 | 小改动 | 直接处理 |
| 开发任务 | 需要多步骤完成的任务 | 创建任务并执行 |
| 漫剧创作 | 创作新故事、角色等（仅限 story 项目） | 使用 `/aim:story` |

---

## 项目类型检测

根据项目结构自动识别项目类型：

| 项目类型 | 特征 | 规范目录 |
|----------|------|----------|
| CLI 工具 | 有 `bin/` 目录 | `spec/cli/` |
| 前端 | 有 `package.json`、前端框架 | `spec/frontend/` |
| 后端 | 有 `requirements.txt`、`go.mod` 等 | `spec/backend/` |
| 全栈 | 既有前端又有后端 | `spec/frontend/` + `spec/backend/` |
| 漫剧创作 | 有 `spec/story/` | `spec/story/` |

---

## 组合使用方案

### 方案一：日常开发

```
1. /aim:start              → 阅读工作流和项目状态
2. 讨论需求...
3. /aim:finish-work        → 完成工作并记录
```

### 方案二：漫剧创作（仅限 story 项目）

```
1. /aim:start              → 了解项目状态
2. /aim:story              → 开始创作
3. /aim:portrait <角色名>  → 创建角色肖像
4. /aim:visualize          → 生成图片提示词
5. /aim:check-story        → 检查剧情一致性
6. /aim:finish-work         → 完成工作并记录
```

---

## 核心原则

> **规范是注入的，不是记忆的。**
>
> 开发工作流确保 AI 接收相关规范。这比希望 AI "记住"规范更可靠。

---

## 相关命令（根据项目类型使用）

| 命令 | 用途 | 适用项目 |
|------|------|----------|
| `/aim:start` | 开始会话 | 所有 |
| `/aim:story` | 漫剧创作模式 | story |
| `/aim:portrait` | 生成角色肖像 | story |
| `/aim:visualize` | 生成图片提示词 | story |
| `/aim:check-story` | 检查剧情一致性 | story |
| `/aim:finish-work` | 完成工作并生成日志 | 所有 |

---

## 注意事项

1. **漫剧命令仅限 story 项目**：如果项目不是漫剧创作类型，`/aim:story` 等命令不可用
2. **遵循项目规范**：开发前务必阅读 `spec/` 目录下的规范文件
3. **记录工作进度**：完成工作后使用 `/aim:finish-work` 记录
