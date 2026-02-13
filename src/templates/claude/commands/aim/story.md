---
name: story
description: 启动漫剧创作模式
---

# 漫剧创作

启动漫剧创作模式，开始你的故事创作。

---

## 适用场景

- 创作全新的漫剧项目
- 开始新剧集的创作
- 为现有项目添加新角色或新情节

---

## 完整工作流程

### 流程概览

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        漫剧创作完整流程                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. 初始化 ──────────────────────────────────────────────────────→     │
│     aim init -u <你的名字>                                              │
│                                                                         │
│  2. 开始工作 ────────────────────────────────────────────────────→     │
│     /aim:start                                                        │
│                                                                         │
│  3. 创作阶段 ────────────────────────────────────────────────────→     │
│     │                                                                  │
│     ├─→ /aim:story              启动漫剧创作                           │
│     │                                                                  │
│     ├─→ /aim:portrait <角色>   创建角色肖像（可选，可多次）            │
│     │                                                                  │
│     ├─→ /aim:visualize          生成场景图片（可选，可多次）           │
│     │                                                                  │
│     └─→ /aim:check-story       检查剧情一致性（可选，可多次）          │
│                                                                         │
│  4. 导出阶段 ────────────────────────────────────────────────────→     │
│     │                                                                  │
│     └─→ /aim:export            导出 Seedance 视频提示词              │
│                                                                         │
│  5. 完成工作 ────────────────────────────────────────────────────→     │
│     /aim:finish-work                                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 详细步骤

### 步骤 1：初始化项目

```bash
# 在你的项目目录中
aim init -u 你的名字
```

这会创建以下结构：

```
项目目录/
├── .aim-studio/              # 系统配置
│   ├── spec/story/          # 创作规范
│   │   ├── script.md        # 剧本规范
│   │   ├── character.md     # 角色设定
│   │   └── world.md         # 世界观设定
│   └── tasks/               # 任务存储
├── aim-workspace/           # 工作日志（你的创作记录）
└── ...
```

### 步骤 2：开始工作

```bash
/aim:start
```

AI 会：
1. 读取项目状态
2. 查看最近的工作日志
3. 询问你今天要做什么

### 步骤 3：开始创作

#### 3.1 启动创作模式

```bash
/aim:story
```

AI 会询问你想要创作什么。

#### 3.2 创建角色（可选但推荐）

当你创作了新角色后，使用：

```bash
/aim:portrait 角色名
```

**示例**：
```
/aim:portrait 慕容天
/aim:portrait 沈安在
/aim:portrait 女主角
```

这会生成角色的 AI 绘画提示词，你可以保存下来用于后续生成角色图片。

#### 3.3 生成场景图片（可选）

当你写完一个场景后，想要生成对应的图片：

```bash
/aim:visualize
```

这会将当前剧本段落转换为 Qwen-Image 优化的绘画提示词。

#### 3.4 检查剧情一致性（推荐）

完成一段创作后，检查是否有前后不一致：

```bash
/aim:check-story
```

这会检查：
- 角色行为是否符合人设
- 剧情逻辑是否连贯
- 场景描述是否一致

### 步骤 4：导出视频提示词

当你完成一集或几集的创作后，准备生成视频：

```bash
/aim:export
```

实际上是在终端执行：

```bash
python3 .aim-studio/scripts/export.py --ep 1
```

#### 4.1 选择导出集数

```bash
# 导出第1集
python3 .aim-studio/scripts/export.py --ep 1

# 导出1-3集
python3 .aim-studio/scripts/export.py --ep 1-3

# 导出全部
python3 .aim-studio/scripts/export.py --all
```

#### 4.2 选择视频时长

根据场景复杂度选择：

```bash
# 5秒（简单对话）
python3 .aim-studio/scripts/export.py --ep 1 --duration 5

# 10秒（默认，通用）
python3 .aim-studio/scripts/export.py --ep 1 --duration 10

# 15秒（中等复杂度）
python3 .aim-studio/scripts/export.py --ep 1 --duration 15

# 30秒（复杂场景）
python3 .aim-studio/scripts/export.py --ep 1 --duration 30

# 45秒或60秒（长场景）
python3 .aim-studio/scripts/export.py --ep 1 --duration 45
python3 .aim-studio/scripts/export.py --ep 1 --duration 60
```

#### 4.3 违规检测

导出时会自动检查违规内容：

| 违规类型 | 检测内容 | 风险等级 |
|----------|----------|----------|
| 真人素材 | 明星、网红、真实照片 | ⚠️ 高风险 |
| 版权内容 | 金庸小说、漫威、哈利波特 | ⚠️ 中风险 |
| 敏感内容 | 暴力、血腥、政治 | ⚠️ 中风险 |

如果检测到违规，系统会提示你选择处理方式：

```
请选择处理方式（输入数字）：
  1. 修改角色设定 - 使用虚构角色替代真人
  2. 替换版权内容 - 使用原创元素
  3. 简化敏感描述 - 移除敏感描述
  4. 强制导出 - 仍要导出（风险自负）
  5. 退出 - 不导出
```

#### 4.4 完整导出示例

```bash
# 最常用：导出第1集，10秒，自动打开文件夹
python3 .aim-studio/scripts/export.py --ep 1 --open

# 完整参数：导出第1集，30秒，seedance格式
python3 .aim-studio/scripts/export.py --ep 1 --duration 30 --format seedance

# 批量导出：1-3集，15秒
python3 .aim-studio/scripts/export.py --ep 1-3 --duration 15
```

#### 4.5 仅检查违规

如果你只想检查内容是否合规，不导出：

```bash
python3 .aim-studio/scripts/export.py --check
```

### 步骤 5：完成工作

```bash
/aim:finish-work
```

这会：
1. 检查内容完整性
2. 检查格式是否符合规范
3. 可选：运行剧情一致性检查
4. 记录工作内容

#### 5.1 记录会话（可选单独使用）

```bash
# 记录本次工作
python3 ./.aim-studio/scripts/add_session.py \
  --title "第1集创作" \
  --summary "完成第1集前5场的创作"
```

---

## 常见场景

### 场景 1：全新项目，从零开始

```
1. aim init -u 我的名字
2. /aim:start
3. /aim:story
   → 告诉 AI 要创作什么类型的故事
4. 创作角色和剧情...
5. /aim:portrait 角色1
6. /aim:portrait 角色2
7. 继续创作...
8. /aim:check-story
9. /aim:export --ep 1 --open
10. /aim:finish-work
```

### 场景 2：继续之前的创作

```
1. /aim:start
   → AI 会读取之前的进度
2. 继续创作...
3. /aim:check-story
4. /aim:export --ep 2 --duration 15
5. /aim:finish-work
```

### 场景 3：修改角色设定

```
1. /aim:portrait 角色名
   → 生成新的肖像提示词
2. 手动更新 character.md
3. /aim:check-story
   → 检查修改后是否一致
```

### 场景 4：生成宣传图片

```
1. /aim:visualize
   → 将剧本场景转换为图片提示词
2. 复制提示词到 AI 绘画工具
3. 生成图片
```

---

## 参数速查表

### export.py 完整参数

| 参数 | 必填 | 可选值 | 默认值 | 说明 |
|------|------|--------|--------|------|
| `--ep` | 是 | `1`, `1-3`, `all` | 无 | 导出集数 |
| `--format` | 否 | `seedance`, `simple` | `seedance` | 格式 |
| `--duration` | 否 | `5/10/15/30/45/60` | `10` | 时长(秒) |
| `--output` | 否 | 目录名 | `export` | 输出目录 |
| `--open` | 否 | 开关 | 关闭 | 导出后打开 |
| `--check` | 否 | 开关 | 关闭 | 仅检查违规 |
| `--force` | 否 | 开关 | 关闭 | 强制导出 |

### add_session.py 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--title` | 是 | 会话标题 |
| `--summary` | 是 | 工作摘要 |
| `--commit` | 否 | Git 提交哈希 |

---

## 注意事项

1. **先检查后导出**：建议先运行 `--check` 确认无违规
2. **选择合适时长**：复杂场景用 15-30 秒，简单对话用 5-10 秒
3. **保持角色一致**：每次创作前回顾 character.md
4. **记录工作进度**：完成后使用 finish-work 记录，便于后续继续

---

## 相关命令

| 命令 | 用途 |
|------|------|
| `/aim:start` | 开始会话 |
| `/aim:story` | 开始创作 |
| `/aim:portrait` | 生成角色肖像 |
| `/aim:visualize` | 生成场景图片 |
| `/aim:check-story` | 检查剧情一致性 |
| `/aim:export` | 导出视频提示词 |
| `/aim:finish-work` | 完成工作 |
