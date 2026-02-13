<p align="center">
  <img src="assets/aim-studio.png" alt="AIM Studio Logo" width="500" style="image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges;">
</p>

# AIM Studio

> **AI 驱动的智能开发工作流 CLI 工具**
>
> *让规范成为习惯，让开发更高效*

[![npm version](https://img.shields.io/npm/v/@fifine/aim-studio.svg?style=flat-square&color=blue)](https://www.npmjs.com/package/@fifine/aim-studio)
[![license](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)

---

## 📖 简介

**AIM Studio** 是一个 AI 驱动的智能开发工作流 CLI 工具，专注于解决 AI 辅助开发中的核心痛点：

- **思考先于编码**：通过 Thinking Guides 和 Ralph Loop 避免"修 A 坏 B"的循环
- **上下文持久化**：通过 Spec Injection 将规则注入每个任务，而非依赖记忆
- **跨层思考**：通过 Cross-Layer Guide 梳理数据流和模块边界

无论你是使用 Claude Code、Cursor 还是其他 AI 助手，AIM Studio 都能确保 AI 始终遵循你项目的开发规范，彻底解决 AI "写着写着就忘了约定" 的痛点。

## ✨ 核心特性

| 特性 | 解决的问题 |
| --- | --- |
| **全自动规范注入 (Spec Injection)** | 项目规范自动注入 AI 上下文。写一次，永久生效。 |
| **多类型项目支持** | 支持 CLI、前端、后端、全栈、漫剧创作等多种项目类型 |
| **智能项目识别** | 自动检测项目类型，生成对应的规范模板 |
| **任务持久化** | 自动记录工作日志，AI 永远记得上一次的进度 |
| **多 Agent 协作** | 支持 Plan-Implement-Check 分离，复杂任务更可靠 |

## 🚀 快速开始

### 1. 安装

```bash
npm i @fifine/aim-studio -g
```

### 2. 初始化项目

```bash
# 进入你的项目目录
cd my-project

# 初始化 AIM Studio
aim init -u 你的名字
```

### 3. 开始工作

```bash
# 在 Claude Code 中使用
/aim:start
```

## 📁 项目结构

初始化后，项目目录结构如下：

```
项目根目录/
├── aim-workspace/          # 你的工作空间（创作内容存放处）
├── .aim-studio/           # 系统配置（自动生成）
│   ├── spec/              # 项目规范
│   │   ├── cli/           # CLI 开发规范
│   │   ├── frontend/      # 前端开发规范
│   │   ├── backend/       # 后端开发规范
│   │   └── story/         # 漫剧创作规范
│   ├── tasks/             # 任务追踪
│   ├── scripts/           # 自动化脚本
│   └── workflow.md        # 工作流文档
└── ...
```

## 📚 工作流命令

### Slash 命令（在 AI 对话框中使用）

| 命令 | 说明 | 适用场景 |
| --- | --- | --- |
| `/aim:start` | 开始工作会话 | 日常开发、维护 |
| `/aim:story` | 漫剧创作模式 | 创作新故事（仅 story 项目） |
| `/aim:portrait` | 生成角色肖像 | 创建角色形象（仅 story 项目） |
| `/aim:visualize` | 生成图片提示词 | 分镜描述转 AI 绘画（仅 story 项目） |
| `/aim:check-story` | 检查剧情一致性 | 剧情审核（仅 story 项目） |
| `/aim:export` | 导出剧本 | 导出为 Seedance 格式（仅 story 项目） |
| `/aim:finish-work` | 完成工作并记录 | 每次结束工作前必做 |

> **注意**：漫剧相关命令（story/portrait/visualize/check-story/export）仅在 `story` 类型项目中可用。

## 🎯 项目类型

AIM Studio 支持自动检测以下项目类型：

| 类型 | 检测特征 | 规范目录 |
| --- | --- | --- |
| CLI | `bin/` 目录 | `spec/cli/` |
| 前端 | `package.json`、前端框架 | `spec/frontend/` |
| 后端 | `requirements.txt`、`go.mod` 等 | `spec/backend/` |
| 全栈 | 既有前端又有后端 | `spec/frontend/` + `spec/backend/` |
| 漫剧创作 | `spec/story/` | `spec/story/` |

## 🛠️ 终端命令

| 命令 | 说明 |
| --- | --- |
| `aim init` | 初始化 AIM Studio 项目 |
| `aim update` | 更新项目配置到最新版本 |
| `aim task create <name>` | 创建新任务 |

## 🤝 参与贡献

欢迎提交 Issue 或 PR！

- [GitHub 仓库](https://github.com/five-five0909/aim-studio)
- [开发指南](CLAUDE.md)

## 📄 许可证

MIT License. Made by [AIM Studio](https://github.com/five-five0909).
