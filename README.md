<p align="center">
  <img src="assets/trellis.png" alt="AIM Studio Logo" width="500" style="image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges;">
</p>

# AIM Studio (原 Trellis)

> **专注于 AI 漫剧与小说创作的智能 CLI 工作流工具**
>
> *让规范成为习惯，让创意无限延伸*

[![npm version](https://img.shields.io/npm/v/@fifine/aim-studio.svg?style=flat-square&color=blue)](https://www.npmjs.com/package/@fifine/aim-studio)
> **Note**: This is a specialized CLI tool for AI-assisted comic and drama creation.
[![license](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)

---

## 📖 简介

**AIM Studio** 是一个专为 AI 辅助创作（漫剧、小说、剧本）设计的 CLI 工具。它继承了 Trellis 的核心能力——**全自动上下文注入**，并针对创作场景进行了专门优化。

无论你是使用 Claude Code、Cursor 还是其他 AI 助手，AIM Studio 都能确保 AI 始终遵循你设定的世界观、角色档案和剧本格式，彻底解决 AI "写着写着就忘了设定" 的痛点。

## ✨ 核心特性

| 特性 | 解决的问题 |
| --- | --- |
| **全自动设定注入 (Spec Injection)** | 角色、世界观、剧本格式自动注入 AI 上下文。写一次，永久生效。 |
| **AI 漫剧主笔 (Story Agent)** | 专用的 AI 代理，懂得先完善设定再写剧本，严格遵守分镜规范。 |
| **一键启动 (Quick Start)** | `/aim:story` 指令一键初始化创作项目，零门槛上手。 |
| **多任务并行 (Parallel Sessions)** | 同时推进多个故事线，互不干扰。 |
| **持久化记忆 (Session Persistence)** | 自动记录创作日志，AI 永远记得上一次的剧情进展。 |

## 🚀 快速开始

### 1. 安装

```bash
npm i @fifine/aim-studio
```

### 2. 初始化项目

在你的创作目录下：

```bash
aim init -u 你的笔名
```

### 3. 开始创作

使用专用指令启动漫剧创作模式：

```bash
# 创建并启动一个新故事
/aim:story "由AI统治的古代王朝"
```

或者手动启动：

```bash
aim task create "第一章：觉醒" --type story
aim start
```

## 📚 创作工作流

### 第一步：完善设定 (World Building)

AIM Studio 会并在 `.aim-studio/spec/story/` 目录下生成标准模板：
- `character.md` (角色档案)
- `world.md` (世界观)
- `script.md` (剧本规范)

**AI 会自动读取这些文件**。你只需要告诉 AI："帮我完善主角'林风'的性格设定"，它就会基于模板进行填充。

### 第二步：剧本生成 (Scripting)

AI 将严格按照 `script.md` 定义的格式输出剧本，支持直接导出为分镜描述：

> **场次 1：废弃仓库 - 深夜 - 紧张**
> 
> 李明：(喘着粗气) 别过来！

### 第三步：AI 绘画对接 (Visualizing)

Story Agent 懂得将剧本描述转换为 Stable Diffusion 或 Midjourney 的提示词 (Prompts)，助力漫剧视觉化。

## � 指令参考手册

### 1. 终端命令 (CLI)
这些命令在你的系统终端（Terminal/PowerShell）中运行：

| 命令 | 说明 | 示例 |
| --- | --- | --- |
| `aim init` | 初始化一个新的 AIM Studio 项目 | `aim init -u 笔名` |
| `aim update` | 更新当前项目的配置和脚本到最新版本 | `aim update` |

### 2. AI Slash 命令
这些命令在 AI 助手（如 Claude Code）的对话框中运行：

| 命令 | 说明 | 使用场景 |
| --- | --- | --- |
| `/aim:story` | **[核心]** 启动漫剧/小说创作模式 | 创作新故事、开始新章节 |
| `/aim:visualize` | **[创作]** 生成分镜提示词 | 将剧本转换为 AI 绘画指令 |
| `/aim:check-story` | **[质检]** 检查剧情逻辑 | 检查 OOC、逻辑漏洞、设定冲突 |
| `/aim:export` | **[发布]** 导出排版 | 生成适合发布的最终文本 |
| `/aim:start` | 启动通用开发任务 | 日常创作、维护 |
| `/aim:finish-work` | 结束当前任务并生成进度日志 | 每次结束工作前必做 |
| `/aim:record-session` | 记录当前会话摘要（不结束任务） | 长时间工作的中途存档 |

> **提示**: 所有 Slash 命令本质上都是在调用 `.aim-studio/scripts/` 下的 Python 脚本或 Agent 指令。

## �💡 最佳实践示例：小说改漫剧

假设你想将小说**《我真没想重生啊》**改编为漫剧：

1.  **准备素材**:
    将小说原文保存为 TXT 文件，建议存放在 `.aim-studio/materials/` 目录下。
    > 例如：`.aim-studio/materials/wozhenmeixiangchongshengan.txt`

2.  **启动项目**:
    ```bash
    /aim:story "我真没想重生啊-漫剧版"
    ```

3.  **下达指令**:
    在 AI 会话中输入：
    > "请读取 `.aim-studio/materials/wozhenmeixiangchongshengan.txt` 的第一章内容。
    > 提取其中的核心冲突和陈汉升的性格特征，完善 `character.md`。
    > 然后将第一章改编为分镜剧本。"

AI 将会自动分析原文，提取“渣男”陈汉升的性格关键词（腹黑、痞气），并生成第一话的分镜脚本。

## 🛠️ 高级用法

### 并行创作

```bash
aim parallel
```
同时开启多个 AI 会话（Git Worktree 隔离），一边写大纲，一边写细纲，互不阻塞。

### 进度保存

```bash
/aim:finish-work
```
自动生成本次创作的小结，并更新进度索引。下次启动时 AI 会自动回顾。

## 🤝 参与贡献

欢迎提交 Issue 或 PR！

- [GitHub 仓库](https://github.com/five-five0909/aim-studio)
- [开发指南](CLAUDE.md)

## 📄 许可证

MIT License. Made by [AIM Studio](https://github.com/five-five0909).
