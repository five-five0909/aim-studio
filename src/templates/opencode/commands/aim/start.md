# 开始会话

初始化 AIM Studio 漫剧创作会话，开始你的故事创作。

---

## 适用场景

- 首次开始漫剧创作
- 开始新的创作会话
- 想要了解当前项目状态

---

## 执行步骤

### 步骤 1：获取当前上下文

```bash
python3 .aim-studio/scripts/get_context.py
```

这会显示：
- 项目状态
- 最近的工作日志
- 待完成的任务（如有）

### 步骤 2：阅读工作流指南

```bash
cat .aim-studio/workflow.md
```

### 步骤 3：阅读创作规范

```bash
cat .aim-studio/spec/story/script.md       # 剧本规范
cat .aim-studio/spec/story/character.md    # 角色设定规范
cat .aim-studio/spec/story/world.md        # 世界观设定规范
```

### 步骤 4：开始工作

报告你了解到的内容，询问用户："您好！请问今天需要创作什么？"

---

## 漫剧创作流程

```
1. /aim:start              → 了解项目状态
2. /aim:story              → 开始创作
3. /aim:portrait <角色>   → 创建角色肖像
4. /aim:visualize          → 生成场景图片
5. /aim:check-story        → 检查剧情一致性
6. /aim:export             → 导出视频提示词
7. /aim:finish-work        → 完成工作并记录
```

---

## 相关命令

| 命令 | 用途 |
|------|------|
| `/aim:story` | 开始漫剧创作 |
| `/aim:portrait` | 生成角色肖像 |
| `/aim:visualize` | 生成场景图片 |
| `/aim:check-story` | 检查剧情一致性 |
| `/aim:export` | 导出视频提示词 |
| `/aim:finish-work` | 完成工作并记录 |

---

## 注意事项

1. **遵循规范**：创作前务必阅读 `spec/story/` 下的规范文件
2. **保持一致**：每次创作前回顾 character.md，确保角色行为符合人设
3. **记录进度**：完成工作后使用 `/aim:finish-work` 记录
