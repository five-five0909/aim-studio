# 导出剧本

将剧本导出为可直接粘贴到 AI 视频生成工具（如 Seedance）的**纯文本格式**。

---

## 核心功能

本命令生成**不带任何 Markdown 符号**的纯文本文件，可直接复制粘贴到 Seedance 的视频生成输入框。

### 新增功能

- ✅ **违规检测** - 自动检测真人素材、版权内容、敏感内容
- ✅ **时长选择** - 支持 5s/10s/15s/30s/45s/60s 多种时长
- ✅ **智能处理** - 检测到违规时提供多种处理选项

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

### 时长选择

支持以下视频时长：

```bash
# 5秒短视频
python3 .aim-studio/scripts/export.py --ep 1 --duration 5

# 10秒（默认）
python3 .aim-studio/scripts/export.py --ep 1 --duration 10

# 15秒
python3 .aim-studio/scripts/export.py --ep 1 --duration 15

# 30秒
python3 .aim-studio/scripts/export.py --ep 1 --duration 30

# 45秒
python3 .aim-studio/scripts/export.py --ep 1 --duration 45

# 60秒
python3 .aim-studio/scripts/export.py --ep 1 --duration 60
```

### 违规检测

导出时会自动检查以下违规内容：

| 违规类型 | 检测内容 | 风险 |
|----------|----------|------|
| **真人素材** | 明星、公众人物、网红、真实照片等 | 平台禁止 |
| **版权内容** | 哈利波特、漫威、金庸小说、IP等 | 侵权风险 |
| **敏感内容** | 暴力、血腥、政治、宗教等 | 审核风险 |

```bash
# 仅检查违规，不导出
python3 .aim-studio/scripts/export.py --check

# 强制导出（忽略违规警告）
python3 .aim-studio/scripts/export.py --ep 1 --force
```

---

## 违规检测流程

### 自动检测

执行导出命令时，系统会自动：

1. **扫描角色设定** - 检查 `spec/story/character.md`
2. **扫描世界观** - 检查 `spec/story/world.md`
3. **扫描所有场景** - 检查 `tasks/EP*/` 下的所有文件

### 检测结果示例

```
============================================================
🚨 违规检测报告
============================================================

⚠️  检测到以下潜在违规内容：

【真人素材风险】
  - 关键词: 明星
  - 关键词: 刘德华

【版权风险】
  - 关键词: 金庸

============================================================
💡 建议处理方式：
  1. 修改角色设定 - 使用虚构角色替代真人
  2. 替换版权内容 - 使用原创元素替代受版权保护的内容
  3. 简化敏感描述 - 移除可能引发争议的描述
  4. 强制导出 - 仍要导出（风险自负）
============================================================
```

### 用户选择

检测到违规后，用户可以选择：

| 选项 | 说明 |
|------|------|
| 1 | 修改角色设定 - 提示用户手动修改角色文件 |
| 2 | 替换版权内容 - 提示用户修改版权相关内容 |
| 3 | 简化敏感描述 - 提示用户移除敏感描述 |
| 4 | 强制导出 - 忽略警告，继续导出 |
| 5 | 退出 - 不导出 |

---

## 输出文件

导出会生成纯文本文件到 `export/` 目录：

```
export/
├── EP01_场景1.txt      # 可直接粘贴，包含时长
├── EP01_场景2.txt      # 可直接粘贴
├── EP02_场景1.txt
└── ...
```

### 输出格式示例

```
=== 场景1: 青云峰主殿 ===

[DURATION: 10s]

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

### 步骤 1：导出（带检测）

```bash
python3 .aim-studio/scripts/export.py --ep 1 --duration 10 --open
```

### 步骤 2：处理违规（如有）

根据检测结果选择处理方式

### 步骤 3：复制

打开 `export/` 文件夹，选择对应场次的 `.txt` 文件，**直接全选复制**。

### 步骤 4：粘贴到 Seedance

将复制的内容**直接粘贴**到 Seedance 的 prompt 输入框中，点击生成。

---

## 与其他命令配合

```
1. /aim:story              → 创作剧本
2. /aim:check-story        → 检查剧情一致性
3. /aim:export --ep 1      → 导出第1集（10秒）
4. 复制到 Seedance         → 生成视频
```

---

## 完整参数说明

### 所有参数一览表

| 参数 | 必填 | 可选值 | 默认值 | 说明 |
|------|------|--------|--------|------|
| `--ep` | 是 | `1`, `1-3`, `all` | 无 | 指定导出的集数 |
| `--format` | 否 | `seedance`, `simple` | `seedance` | 导出格式 |
| `--duration` | 否 | `5`, `10`, `15`, `30`, `45`, `60` | `10` | 视频时长（秒） |
| `--output` | 否 | 任意目录名 | `export` | 输出目录名称 |
| `--open` | 否 | 开关 | 关闭 | 导出后自动打开文件夹 |
| `--check` | 否 | 开关 | 关闭 | 仅检查违规，不导出 |
| `--force` | 否 | 开关 | 关闭 | 强制导出，忽略违规警告 |

### 参数详细说明

#### `--ep` (必填)
指定要导出的集数：
- `1` - 导出第1集
- `1-3` - 导出第1集到第3集
- `all` - 导出所有集数

示例：
```bash
python3 .aim-studio/scripts/export.py --ep 1       # 导出第1集
python3 .aim-studio/scripts/export.py --ep 1-3     # 导出1到3集
python3 .aim-studio/scripts/export.py --ep all      # 导出全部
```

#### `--format` (可选)
导出内容的格式：
- `seedance`（默认）- 完整格式，包含角色、环境、上下文、风格等所有信息
- `simple` - 极简格式，只有场景描述和对话

示例：
```bash
python3 .aim-studio/scripts/export.py --ep 1 --format seedance
python3 .aim-studio/scripts/export.py --ep 1 --format simple
```

#### `--duration` (可选)
生成的视频时长（秒）：
- `5` - 5秒短视频
- `10` - 10秒（**默认值**）
- `15` - 15秒
- `30` - 30秒
- `45` - 45秒
- `60` - 60秒

示例：
```bash
python3 .aim-studio/scripts/export.py --ep 1 --duration 5   # 5秒
python3 .aim-studio/scripts/export.py --ep 1 --duration 30  # 30秒
```

#### `--output` (可选)
指定输出目录的名称，默认值为 `export`

示例：
```bash
python3 .aim-studio/scripts/export.py --ep 1 --output my-videos
# 输出到 my-videos/ 目录
```

#### `--open` (可选)
导出完成后自动打开输出文件夹（仅 Windows/Mac/Linux）

示例：
```bash
python3 .aim-studio/scripts/export.py --ep 1 --open
```

#### `--check` (可选)
只检查违规内容，不进行导出。检查结果会显示是否有违规，但不会生成文件。

示例：
```bash
python3 .aim-studio/scripts/export.py --check
# 输出违规报告，不导出任何文件
```

#### `--force` (可选)
强制导出，即使检测到违规内容也会继续导出。**注意：使用此参数风险自负！**

示例：
```bash
python3 .aim-studio/scripts/export.py --ep 1 --force
```

### 组合使用示例

```bash
# 完整示例：导出第1集，30秒时长，导出后打开文件夹
python3 .aim-studio/scripts/export.py --ep 1 --duration 30 --open

# 导出1-3集，15秒，简单格式
python3 .aim-studio/scripts/export.py --ep 1-3 --duration 15 --format simple

# 仅检查违规
python3 .aim-studio/scripts/export.py --check

# 强制导出（忽略警告）
python3 .aim-studio/scripts/export.py --ep 1 --force
```

---

## 注意事项

1. **纯文本格式**：导出的文件不包含任何 `#`、`*`、`[]` 等 Markdown 符号
2. **字符编码**：文件使用 UTF-8 编码，确保 Seedance 能正确识别
3. **时长选择**：根据场景复杂度选择合适时长，复杂场景建议 15-30 秒
4. **违规检测**：建议先检查违规，修改后再导出，确保内容合规
5. **强制导出**：使用 `--force` 会忽略警告，风险由用户自行承担
