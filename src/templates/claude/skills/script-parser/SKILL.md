---
name: script-parser
description: 剧本解析器 — 将自由格式文本转换为标准结构化剧本
---

# Script Parser（剧本解析器）

将用户的自由格式剧本文本解析为 AIM Studio 标准剧本格式，支持复杂场景和特殊叙事结构。

## 输入类型

任意格式的剧本文本，包括但不限于：
- 纯对话文本（Novel style）
- 只有大纲的描述（Outline style）
- 混合格式（Hybrid style）
- 已有格式但不统一的剧本（Legacy scripts）

## 输出格式

###Markdown 标准格式

```markdown
# 第X集：集名

## 场次 1：[地点] - [时间] - [气氛]

### 场景描述
[环境、气氛、画面描写]

### 角色
- [角色名]：[本场状态/情绪]

### 内容

**[角色名]**：（[动作/表情]）"台词"

[旁白/动作描述]

> [特殊镜头指令：如淡入、黑屏、特写]

---
```

### JSON 数据格式 (可选)

```json
{
  "episode": 1,
  "title": "集名",
  "scenes": [
    {
      "scene_number": 1,
      "location": "地点",
      "time": "时间",
      "atmosphere": "气氛",
      "description": "场景描述",
      "characters": ["角色A", "角色B"],
      "content": [
        {
          "type": "dialogue",
          "character": "角色A",
          "parenthetical": "动作/表情",
          "text": "台词"
        },
        {
          "type": "action",
          "text": "动作描述"
        }
      ]
    }
  ]
}
```

## 解析规则与模式识别

### 1. 场景切分 (Scene Analysis)

使用正则表达式识别场景转换：
*   **地点标识**：`/(INT\.|EXT\.|内景|外景|地点：|场景：).+/i`
*   **时间标识**：`/(DAY|NIGHT|MORNING|EVENING|日|夜|清晨|黄昏)/i`
*   **特殊转场**：`/(CUT TO:|FADE IN:|DISSOLVE TO:|切至|淡入|溶接).+/i`

### 2. 角色与对白提取 (Character & Dialogue)

*   **角色名识别**：全大写英文或以冒号结尾的中文名。
    *   Pattern: `/^([A-Z\s]+|[\u4e00-\u9fa5]{2,4}[：:])$/`
*   **括号内容**：解析为 `parenthetical`（动作/表情）。
    *   Pattern: `/\((.*?)\)|（(.*?)）/`

### 3. 特殊结构处理

*   **闪回 (Flashback)**：标注 `[FLASHBACK]` 或 `[回忆]`。
*   **蒙太奇 (Montage)**：将一系列短镜头合并为一个序列，或拆分为独立子场次。
*   **分屏 (Split Screen)**：标注 `[SPLIT SCREEN]`，分别描述左右画面。
*   **画外音 (V.O./O.S.)**：在角色名后识别 `(V.O.)` 或 `(O.S.)`，标注为画外音。

## 使用方式

```
请将以下文本解析为标准剧本格式：
[粘贴文本]
```

```
请将以下文本解析为 JSON 格式：
[粘贴文本]
```

## 注意事项

- **保留原意**：严禁修改原文的对话和核心动作。
- **补全信息**：如果原文缺失时间或气氛，根据上下文合理推断并标注 `[推断]`。
- **统一标点**：将英文标点转换为中文标点（引号、省略号、破折号）。
- **格式校验**：确保所有输出符合 `.aim-studio/spec/story/script.md` 规范。
