---
name: record-session
description: 记录创作会话
---

# 记录会话

将本次创作工作记录到工作日志中，便于后续回顾和继续。

---

## 适用场景

- 完成一个创作阶段
- 结束创作会话
- 需要记录重要决策

---

## 使用方法

### 基本用法

```bash
# 简单记录
python3 ./.aim-studio/scripts/add_session.py \
  --title "第1集第3场创作" \
  --summary "完成慕容天与沈安在的对手戏"

# 详细记录
python3 ./.aim-studio/scripts/add_session.py \
  --title "创作第1集" \
  --commit "abc123" \
  --summary "完成第1集前5场的创作"
```

### 参数说明

| 参数 | 说明 | 必需 |
|------|------|------|
| `--title` | 会话标题 | 是 |
| `--summary` | 工作摘要 | 是 |
| `--commit` | Git 提交哈希 | 否 |

---

## 执行步骤

### 步骤 1：获取上下文

```bash
python3 ./.aim-studio/scripts/get_context.py
```

获取当前项目状态和最近的工作内容。

### 步骤 2：记录会话

```bash
python3 ./.aim-studio/scripts/add_session.py \
  --title "<工作标题>" \
  --summary "<工作摘要>"
```

---

## 组合使用方案

### 完整工作流程

```
1. 创作中...
2. /aim:finish-work       → 完成检查
3. /aim:record-session    → 记录工作
```

### 会话结束流程

```
1. /aim:finish-work       → 完成当前工作
2. /aim:record-session    → 记录会话
→ 结束会话
```

---

## 相关命令

| 命令 | 用途 |
|------|------|
| `/aim:finish-work` | 完成工作 |
| `/aim:start` | 开始新会话 |
