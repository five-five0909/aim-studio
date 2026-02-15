# 场景图片生成

将当前剧本段落转换为 AI 绘画提示词，针对 Qwen-Image 优化。

## Qwen-Image 核心优势

| 能力维度 | 技术特点 | 优势 |
|---------|---------|------|
| **复杂文本渲染** | 中英文多行文本、段落级语义 | 中文渲染 58.30%，远超竞品 |
| **精准图像编辑** | 语义一致性与视觉保真度 | 支持链式编辑 |
| **空间关系** | MSRoPE 位置编码 | 精确布局控制 |

---

## Prompt 结构原则

Qwen-Image 使用 **Qwen2.5-VL 作为文本编码器**，最优 Prompt 应包含：

```
【主体对象】+ 【属性细节（颜色/数量/形状/材质）】+ 【空间关系】+ 【文本内容（如需要）】+ 【环境背景】+ 【风格/光影】
```

---

## 执行步骤

### 1. 生成提示词

直接读取当前选中的剧本段落，将其转换为 Qwen-Image 优化的提示词。

### 2. 输出格式

每个场次生成以下格式的提示词：

```markdown
## 场次 X 图片提示词

### 主体描述
[主体对象]，[颜色]，[数量]，[形状]，[材质]

### 属性细节
- 面部特征：[脸型、眼睛、眉毛、发型等]
- 服装：[颜色、材质、款式]
- 配饰：[如有]

### 空间关系
[主体在画面中的位置]，[与其他物体的距离]，[前景/背景关系]

### 文本内容（如需要）
- 文字内容："需要渲染的文字"
- 文字位置：[左上角/中央/底部等]
- 字体样式：[手写体/宋体/霓虹灯管字体等]

### 环境背景
[场景描述]，[时间]，[天气]，[氛围]

### 风格光影
[整体风格]，[色调]，[光源方向]，[参考作品]

### 完整英文提示词
```
{Subject}, {Appearance details}, {Clothing}, {Position}, 
{Environment}, {Lighting}, {Style}, {Quality tags}
```

### 负面提示词
```
ugly, deformed, bad anatomy, extra limbs, blurry, low quality, 
western style (if Chinese style needed), modern clothing (if period piece)
```
```

---

## 中文场景特化技巧

### 1. 直接使用中文字符

```
✅ "招牌上写着'云计算'"
❌ "sign with Chinese characters meaning cloud computing"
```

### 2. 利用成语、诗句、对联

```
一首古诗书法作品，内容为：
"毕竟西湖六月中，风光不与四时同。
接天莲叶无穷碧，映日荷花别样红。"
字体为楷书，背景是水墨画风格的西湖景色。
```

### 3. 复杂排版布局

```
一张信息图表，标题为"情绪健康习惯"，周围环绕六个模块：
左上："练习正念" - 莲花图标
右上："持续学习" - 书本图标
左中："培养感恩" - 双手图标
右中："定期运动" - 跑步图标
左下："保持联结" - 对话图标
右下："优先睡眠" - 月亮图标
整体为优雅的信息图风格，对称布局。
```

---

## 避坑指南

| ❌ 避免 | ✅ 替代 |
|--------|--------|
| "高质量"、"精美" 等空泛词 | 具体描述材质、光影、分辨率要求 |
| 模糊的文本描述 | 用引号明确标注每个文字 |
| 忽略空间位置词 | 使用"左上角"、"中央"、"底部"等明确位置 |
| 过长的无结构句子 | 分段描述不同元素，使用分号或换行 |
| 假设模型懂特定IP或风格 | 详细描述视觉特征 |

---

## 示例

### 输入剧本

```
场次 1：青云峰主殿内 - 清晨 - 萧条落寞

白衣中年沈安在瘫坐在太师椅上，神情苦涩。殿外，少年慕容天背着大包小包，站在门口。
```

### 输出提示词

```markdown
## 场次 1 图片提示词

### 主体描述
- 人物1：沈安在，白衣中年男子，两鬓霜白，面容俊俏，神情苦涩
- 人物2：慕容天，少年身形，背着大包小包

### 属性细节
- 沈安在服装：白色道袍，材质为丝绸，款式宽松
- 慕容天服装：青色布衣，背着布包裹
- 场景道具：太师椅（深棕色木质）、残破窗棂

### 空间关系
沈安在位于画面中央偏左，瘫坐在太师椅上；慕容天位于画面右侧门口处，两人之间有一定距离

### 环境背景
青云峰主殿内部，破旧的大殿，阳光透过残破窗棂洒落，萧条冷清的氛围，清晨光线

### 风格光影
中国仙侠风格，水墨画质感，柔和晨光从左侧打入，产生柔和阴影，色调偏冷

### 完整英文提示词
```
A middle-aged Chinese man in white Taoist robe, sitting slumped on a wooden chair, 
bitter expression, white hair at temples, handsome face. 
In the background, a young man in blue clothes standing at the doorway, carrying large cloth bundles.
Dilapidated temple interior, morning sunlight through broken windows, 
melancholic atmosphere, Chinese xianxia style, ink painting texture, 
soft lighting from left, cool color tone, cinematic composition
```

### 负面提示词
```
ugly, deformed, bad anatomy, extra limbs, blurry, low quality, 
modern clothing, western style, bright colors, happy expression
```
```

---

## 注意事项

1. **文本渲染**：如需要在图片中渲染文字，必须用引号明确标注
2. **中文优化**：Qwen-Image 对中文渲染有独特优势，直接使用汉字
3. **空间布局**：使用明确的位置词（左上角、中央、底部等）
4. **结构化描述**：分段描述不同元素，避免过长的无结构句子