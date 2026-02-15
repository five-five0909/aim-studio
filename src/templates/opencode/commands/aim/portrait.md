# 角色肖像生成

为故事角色生成 AI 绘画提示词，用于创建角色形象。

---

## 适用场景

- 创建新角色的视觉形象
- 为现有角色生成多个姿态
- 需要角色不同场景的服装/表情

---

## 使用方法

### 基本用法

```
/aim:portrait <角色名>
```

### 示例

```
/aim:portrait 慕容天
/aim:portrait 沈安在
/aim:portrait 女主角
```

---

## 执行步骤

### 1. 读取角色设定

首先读取角色设定文件：

```bash
cat .aim-studio/spec/story/character.md
```

### 2. 分析角色特征

根据角色设定，提取以下信息：
- 外观描述（年龄、性别、体型）
- 服装风格
- 发型，配饰
- 性格特征（影响表情）

### 3. 生成提示词

为每个角色生成以下变体：

| 变体类型 | 用途 |
|----------|------|
| 正面全身 | 角色卡、介绍页 |
| 表情特写 | 对话场景、情绪表达 |
| 日常服装 | 日常生活场景 |
| 战斗姿态 | 动作场景 |

---

## 输出格式

### 完整提示词示例

```markdown
## 慕容天 角色肖像

### 基础信息
- 年龄：十七八岁
- 性别：男
- 体型：偏瘦但结实

### 外观描述
少年身形，面容清秀，剑眉星目，鼻若悬胆。
黑色长发，用一根青色丝带束起。
身穿青色布衣，腰间系一条黑色腰带。
背负一柄长剑，剑鞘古朴。

### 正面全身照提示词
A young Chinese man, about 17-18 years old, slender but athletic build,
black long hair tied with a青色 ribbon, swordsman appearance,
black eyes, determined expression, wearing青色布衣,
black belt, carrying an ancient sword, full body shot,
traditional Chinese style, ink painting style, soft lighting

### 表情特写提示词
Close-up of a young Chinese man's face, 17-18 years old,
black long hair, sword eyebrows, star-like eyes,
determined expression, wearing古代布衣,
cinematic lighting, Chinese ink painting style
```

---

## Qwen-Image 优化技巧

### 1. 服装材质描述

| 材质 | 英文描述 |
|------|----------|
| 丝绸 | silk fabric, lustrous sheen |
| 粗布 | coarse cloth fabric, textured |
| 锦缎 | brocade, intricate patterns |
| 皮草 | fur, luxurious texture |

### 2. 表情描述

| 表情 | 英文描述 |
|------|----------|
| 坚毅 | determined expression, firm gaze |
| 温柔 | gentle expression, warm smile |
| 冷峻 | cold expression, piercing eyes |
| 悲伤 | melancholic expression, sorrowful eyes |

### 3. 避免的特征

```
❌ ugly, deformed, bad anatomy
❌ modern clothing, casual wear
❌ bright colors (for ancient style)
❌ western features
```

---

## 组合使用方案

### 方案一：全新角色创建

```
1. /aim:portrait <角色名>     → 生成角色肖像
2. 手动添加到 character.md     → 记录角色设定
3. /aim:visualize             → 生成更多场景变体
```

### 方案二：批量生成主角团队

```
1. /aim:portrait 主角1
2. /aim:portrait 主角2
3. /aim:portrait 主角3
4. ...（每个角色都生成多个变体）
```

---

## 注意事项

1. **一致性**：所有提示词保持角色外观描述一致
2. **参考作品**：可以在提示词中添加参考作品风格
3. **背景**：根据场景需求调整背景描述
4. **光线**：统一整体光线风格

---

## 相关命令

| 命令 | 用途 |
|------|------|
| `/aim:story` | 开始创作 |
| `/aim:visualize` | 生成场景图片 |
| `/aim:check-story` | 检查角色一致性 |
