<p align="center">
  <img src="assets/aim-studio.png" alt="AIM Studio Logo" width="500" style="image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges;">
</p>

# AIM Studio

> **AI 驱动的智能漫剧创作 CLI 工具**
>
> *让创作更高效，让视频生成更简单*

[![npm version](https://img.shields.io/npm/v/@fifine/aim-studio.svg?style=flat-square&color=blue)](https://www.npmjs.com/package/@fifine/aim-studio)
[![license](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)

---

## 📖 简介

**AIM Studio** 是一个 AI 驱动的智能漫剧创作 CLI 工具，专注于帮助用户：

- **创作剧本**：使用 AI 辅助创作小说/漫画改编剧本
- **生成视频**：导出符合 Seedance 格式的提示词
- **保持一致**：AI 检查剧情一致性和角色设定
- **智能合规**：AI 自动检测并修复违规内容

无论你是创作者、UP主还是视频制作者，AIM Studio 都能帮助你快速生成 AI 视频内容。

## ✨ 核心特性

| 特性 | 解决的问题 |
| --- | --- |
| **AI 剧本创作** | 使用 AI 辅助创作，灵感不断 |
| **剧情一致性检查** | 自动检查角色行为、剧情逻辑是否一致 |
| **违规内容检测** | AI 检测并修复真人素材、版权内容、敏感内容 |
| **多风格支持** | 支持写实、邵氏武侠、好莱坞硬派等多种视频风格 |
| **一键导出** | 导出纯文本提示词，直接粘贴到 Seedance |

## 🚀 快速开始

### 1. 安装

```bash
npm i @fifine/aim-studio -g
```

### 2. 初始化项目

```bash
# 进入你的项目目录
cd my-story-project

# 初始化 AIM Studio
aim init -u 你的名字
```

### 3. 开始创作

```bash
# 在 Claude Code 中使用
/aim:start
```

## 📁 项目结构

初始化后，项目目录结构如下：

```
项目根目录/
├── aim-workspace/          # 你的工作空间（创作记录）
├── .aim-studio/           # 系统配置（自动生成）
│   ├── spec/              # 创作规范
│   │   └── story/         # 漫剧创作规范
│   │       ├── index.md      # 规范索引
│   │       ├── character.md  # 角色设定
│   │       ├── world.md      # 世界观设定
│   │       ├── script.md     # 剧本规范
│   │       └── style-guide.md # 视频风格配置
│   ├── tasks/             # 剧集存储
│   │   └── EP01/          # 第1集
│   │       └── 场景1.md    # 场景文件
│   ├── scripts/            # Python 脚本
│   │   └── export.py      # 导出脚本
│   └── workflow.md        # 工作流文档
└── ...
```

## 📚 工作流命令

### Slash 命令（在 AI 对话框中使用）

| 命令 | 说明 |
| --- | --- |
| `/aim:start` | 开始创作会话 |
| `/aim:story` | 启动漫剧创作模式 |
| `/aim:portrait` | 生成角色肖像提示词 |
| `/aim:visualize` | 生成场景图片提示词 |
| `/aim:check-story` | 检查剧情一致性 |
| `/aim:legitimize` | AI 检查并修复违规内容 |
| `/aim:export` | 导出 Seedance 视频提示词 |
| `/aim:finish-work` | 完成工作并记录 |

## 🎬 创作流程

```
1. aim init -u 名字              → 初始化项目
2. /aim:start                   → 开始会话
3. 设置视频风格                  → 选择风格（写实/武侠/好莱坞/日剧/韩剧）
4. /aim:story                   → 开始创作剧本
5. /aim:portrait 角色名          → 生成角色肖像
6. /aim:legitimize --check      → 检查违规内容
7. /aim:legitimize --fix        → 自动修复违规
8. /aim:check-story             → 检查剧情一致性
9. /aim:export --ep 1           → 导出视频提示词
10. 复制到 Seedance             → 生成视频
11. /aim:finish-work            → 完成记录
```

## 🎨 视频风格

| 风格 | 特点 | 适用场景 |
| --- | --- | --- |
| **正常/写实** | 真实自然、无滤镜 | 现代剧、现实主义 |
| **邵氏/港新武侠** | 武侠传统、动作想象 | 古装武侠、江湖 |
| **好莱坞硬派** | 真实打斗、英雄主义 | 动作片、超级英雄 |
| **日本时代剧** | 暴力美学、文化深度 | 武士片、历史剧 |
| **韩国犯罪片** | 写实暴力、社会批判 | 犯罪、悬疑、社会剧 |

## 🛠️ 终端命令

| 命令 | 说明 |
| --- | --- |
| `aim init -u <名字>` | 初始化漫剧创作项目 |
| `aim update` | 更新项目配置到最新版本 |

## 🤝 参与贡献

欢迎提交 Issue 或 PR！

- [GitHub 仓库](https://github.com/five-five0909/aim-studio)
- [开发指南](CLAUDE.md)

## 📄 许可证

MIT License. Made by [AIM Studio](https://github.com/five-five0909).
