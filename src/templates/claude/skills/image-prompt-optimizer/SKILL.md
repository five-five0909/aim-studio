---
name: image-prompt-optimizer
description: 图片提示词优化器 — 生成 Qwen-Image / Flux / MJ 优化的绘画提示词
---

# Image Prompt Optimizer（图片提示词优化器）

生成高度优化、平台特定的 AI 绘画提示词，涵盖光影、构图、风格及细节描述。

## 平台特定优化策略

### 1. Qwen-Image (中文语义增强)

*   **优势**：极强的中文理解、多行文本渲染、复杂逻辑关系。
*   **策略**：直接使用中文长句描述，强调逻辑连接词。
*   **格式**：`[主体描述]，[环境描述]，[光影气氛]，[风格定义]`
*   **文本渲染**：`文字内容："需要渲染的文字"`

### 2. Flux (极致写实与构图)

*   **优势**：解剖学正确、手部细节好、遵循复杂构图。
*   **策略**：自然语言英文描述 (Natural Language Prompts)，类似详细的图片说明。
*   **格式**：`A high resolution photo/illustration of [Subject doing Action] in [Setting]. The lighting is [Light Type]. The style is [Style].`

### 3. Midjourney v6 (艺术与美学)

*   **优势**：艺术风格化、色彩表现力、纹理质感。
*   **策略**：关键词堆叠 (Tagging)，注重艺术风格词和材质词。
*   **参数**：`--ar 16:9 --stylize 250 --v 6.0`

## 核心参数库

### 1. 光影库 (Lighting Library)

| 类型 | 英文 | 效果 |
| :--- | :--- | :--- |
| **伦勃朗光** | Rembrandt Lighting | 经典人像，三角光斑，戏剧性 |
| **蝴蝶光** | Butterfly Lighting | 美颜，鼻下阴影，柔美 |
| **侧光** | Split Lighting / Side Light | 强对比，阴阳脸，神秘 |
| **轮廓光** | Rim Light / Backlight | 勾勒轮廓，与背景分离 |
| **体积光** | Volumetric Lighting / God Rays | 丁达尔效应，神圣感，空间感 |
| **赛博朋克光** | Cyberpunk Lighting / Neon | 霓虹色彩，蓝紫对比，未来感 |
| **柔光** | Softbox / Diffused Light | 无硬阴影，温和，日常 |

### 2. 镜头与视角 (Lens & Angle)

| 类型 | 英文 | 效果 |
| :--- | :--- | :--- |
| **广角** | Wide Angle / 24mm | 宏大场景，夸张透视 |
| **人像头** | Portrait Lens / 85mm | 背景虚化，面部自然 |
| **微距** | Macro Lens / 100mm | 极致细节，昆虫/瞳孔 |
| **鱼眼** | Fisheye Lens | 极度扭曲，趣味性 |
| **俯视** | High Angle / Bird's Eye | 渺小，全局 |
| **仰视** | Low Angle / Worm's Eye | 压迫感，高大 |
| **移轴** | Tilt-shift | 微缩模型感 |

### 3. 材质与质感 (Texture & Material)

*   **皮肤**：`Detailed skin texture, pores, subsurface scattering (SSS)`
*   **衣物**：`Silk（丝绸）, Denim（丹宁）, Leather（皮革）, Latex（乳胶）`
*   **环境**：`Rust（锈迹）, Moss（苔藓）, Concrete（混凝土）, Marble（大理石）`

## 输出模板

### Qwen-Image 提示词模板

```markdown
主体：[详细描述角色外貌、衣着、动作]
环境：[详细描述场景、天气、时间]
光影：[光源方向、色温、阴影类型]
构图：[景别、视角、主体位置]
风格：[艺术风格、画质要求]
文本（如有）：海报上写着"内容"
```

### Flux / MJ 提示词模板

```markdown
[Subject Description], [Action], [Environment], [Lighting keywords], [Camera Angle], [Style/Medium keywords]. 
High quality, 8k, masterpiece, ultra-detailed. 
--ar 16:9 --stylize 300
```

### 负面提示词 (Negative Prompt)

```
ugly, deformed, noisy, blurry, distorted, low quality, bad anatomy, 
extra limbs, poorly drawn face, poorly drawn hands, missing fingers, 
text, watermark, signature, username, artist name
```

## 使用方式

```
请为以下画面生成 [Platform] 提示词：
[画面描述]
```

## 注意事项

- **权重控制**：使用 `(keyword:1.2)` 强调关键元素。
- **风格混合**：`Mixing [Style A] and [Style B]` 可创造新颖视觉。
- **色彩指定**：明确指定主色调，如 `Teal and Orange color grading`。
