# 📋 Prompt 文档索引 — Trellis → AI 漫剧工具 转型指南

> 本目录包含将 `@mindfoldhq/trellis`（AI 开发框架）转型为 **AI 漫剧/连续剧生成工作流 CLI 工具** 的全套 Prompt 文档。

---

## 文档清单

| # | 文件 | 用途 | 阅读顺序 |
| --- | --- | --- | --- |
| 0 | [00-项目转型总纲prompt.md](./00-项目转型总纲prompt.md) | **顶层指导**：项目身份重定义、架构精简、功能转型、文件增删清单 | ⭐ 第一个读 |
| 1 | [01-代码重构约束prompt.md](./01-代码重构约束prompt.md) | **代码层面**：5 Phase 精确执行步骤（精简→改名→模板→文档→验证） | 第二个读 |
| 2 | [02-漫剧工作流设计prompt.md](./02-漫剧工作流设计prompt.md) | **创意核心**：剧本→分镜→角色→提示词→生成的全链路流水线设计 | 第三个读 |
| 3 | [03-ClaudeCode-Skill适配prompt.md](./03-ClaudeCode-Skill适配prompt.md) | **Skill 编写**：Skill/Command/Agent 的编写规范和标准模板 | 第四个读 |
| 4 | [04-NPM发布与使用prompt.md](./04-NPM发布与使用prompt.md) | **发布上线**：package.json 配置、打包验证、发布流程 | 最后读 |

---

## 现有资产

| 文件 | 状态 | 说明 |
| --- | --- | --- |
| [图片生成优化skill.md](./图片生成优化skill.md) | ✅ 已有 | Qwen-Image 提示词优化 Skill，可直接迁移 |
| [视频生成优化skill.md](./视频生成优化skill.md) | ✅ 已有 | Seedance 视频提示词优化 Skill，可直接迁移 |

---

## 执行总览

```
📖 阅读总纲(00) → 理解全局
       ↓
🔧 按代码约束(01) → Phase 1-5 逐步执行
       ↓
🎬 参考工作流(02) → 设计 Skill 内容
       ↓
🤖 按 Skill 规范(03) → 编写每个 Skill 文件
       ↓
📦 按发布指南(04) → npm pack & publish
```
