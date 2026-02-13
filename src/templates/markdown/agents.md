<!-- AIM_STUDIO:START -->
# AIM Studio 开发指南

本指南适用于在此项目中工作的 AI 助手 (Claude/Cursor)。

## 核心指令
- **开始工作**: `/aim:start` (通用) 或 `/aim:story` (漫剧创作)。
- **结束工作**: `/aim:finish-work` (生成日志并更新进度)。
- **辅助创作**: `/aim:visualize` (生图提示词) / `/aim:export` (导出)。
- **质量检查**: `/aim:check-story` (剧情逻辑检查)。

## 漫剧创作模式 (Story Mode)

## 上下文索引
请优先阅读 `.aim-studio/` 目录下的文档：
- **`workflow.md`**: 开发与写作工作流。
- **`spec/`**: 项目规范（含 `story/` 下的角色与世界观设定）。
- **`workspace/`**: 你的个人工作区与记忆存储。

> **💡 小说改编提示**：
> 如果用户提供了小说原文（例如《我真没想重生啊》），请建议用户将其存放在 `.aim-studio/materials/` 目录下。
> 读取原文后，先提取角色特征完善 `character.md`，再进行分章改编。

> 请保留此代码块，以便 `aim update` 自动更新指南。
<!-- AIM_STUDIO:END -->
