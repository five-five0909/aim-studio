---
name: export
description: 导出剧本用于AI视频生成（纯文本格式）
---

# 导出剧本

将剧本导出为可直接粘贴到 AI 视频生成工具（如 Seedance）的**纯文本格式**。

---

## 核心功能

本命令生成**不带任何 Markdown 符号**的纯文本文件，可直接复制粘贴到 Seedance 的视频生成输入框。

---

## 使用方法

### 基本用法

```bash
# 导出第1集
python3 .aim-studio/scripts/export.py --ep 1

# 导出多集
python3 .aim-studio/scripts/export.py --ep 1-3

# 导出全部集数
python3 .aim-studio/scripts/export.py --all

# 导出后打开文件夹
python3 .aim-studio/scripts/export.py --ep 1 --open
```

### 导出格式

| 格式 | 说明 | 用途 |
|------|------|------|
| `seedance` | 完整格式，包含角色、环境、上下文（默认） | 推荐用于 Seedance |
| `simple` | 极简格式，只有场景描述和对话 | 快速复制 |

```bash
# 使用简单格式
python3 .aim-studio/scripts/export.py --ep 1 --format simple
```

---

## 输出文件

导出会生成纯文本文件到 `export/` 目录：

```
export/
├── EP01_场景1.txt      # 可直接粘贴
├── EP01_场景2.txt      # 可直接粘贴
├── EP02_场景1.txt
└── ...
```

---

## Seedance 纯文本格式

导出的文件内容示例（无任何 Markdown 符号）：

```
=== 场景1: 青云峰主殿 ===

[CHARACTERS]
沈安在: 白衣中年男子, 两鬓霜白, 面容俊俏
慕容天: 少年身形, 目光坚定

[ENVIRONMENT]
青云峰主殿: 破旧大殿, 阳光洒落, 萧条冷清

[PREVIOUS CONTEXT]
慕容天决定下山离开

[SCENE]
场次 1: 青云峰主殿内 - 清晨 - 萧条落寞 - 30秒

白衣中年沈安在瘫坐在太师椅上，神情苦涩。

慕容天：(低沉) 师父，弟子不孝，今日便要下山！

沈安在听到声音，却懒得出门。镜头推进他的脸，苦涩中带着自嘲。

[STYLE]
xianxia, chinese fantasy, cinematic lighting, melancholic atmosphere
```

---

## 快速使用流程

### 步骤 1：导出

```bash
python3 .aim-studio/scripts/export.py --ep 1 --open
```

### 步骤 2：复制

打开 `export/` 文件夹，选择对应场次的 `.txt` 文件，**直接全选复制**。

### 步骤 3：粘贴到 Seedance

将复制的内容**直接粘贴**到 Seedance 的 prompt 输入框中，点击生成。

---

## 保持一致性的技巧

### 1. 角色描述一致性

每次导出时，脚本会自动从 `spec/story/character.md` 提取角色信息。确保角色设定文件中的描述保持一致。

### 2. 视觉风格关键词

在世界观文件 `spec/story/world.md` 中定义统一的视觉风格关键词，导出会自动包含这些关键词。

### 3. 上下文衔接

每集导出时会包含 `[PREVIOUS CONTEXT]` 部分，帮助 Seedance 理解剧情连续性。

---

## 常见问题

### Q: 导出文件有乱码？

确保使用 `--format seedance`（默认）格式，这是为 Seedance 优化的纯文本格式。

### Q: 如何只导出一个场景？

目前脚本按集导出。如果需要单场景，可以手动编辑导出的文件。

### Q: 导出的内容太长？

Seedance 对 prompt 长度有限制。可以使用 `--format simple` 获得更简洁的版本。

---

## 与其他命令配合

```
1. /aim:story              → 创作剧本
2. /aim:check-story        → 检查剧情一致性
3. /aim:export --ep 1      → 导出第1集
4. 复制到 Seedance         → 生成视频
```

---

## 注意事项

1. **纯文本格式**：导出的文件不包含任何 `#`、`*`、`[]` 等 Markdown 符号
2. **字符编码**：文件使用 UTF-8 编码，确保 Seedance 能正确识别
3. **首次使用**：建议先导出单集测试，确认格式符合预期
