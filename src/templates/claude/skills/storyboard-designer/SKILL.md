---
name: storyboard-designer
description: 分镜设计师 — 将剧本场次转换为详细分镜描述
---

# Storyboard Designer（分镜设计师）

将剧本场次转换为详细的分镜（Storyboard）描述，为 AI 图片和视频生成提供结构化输入。

## 核心能力库

### 1. 镜头语言 (Camera Lexicon)

| 术语 | 英文 | 描述 | 适用场景 |
| :--- | :--- | :--- | :--- |
| **远景** | Wide Shot / Long Shot | 展示环境、孤独感 | 开场、结束、建立场景 |
| **全景** | Full Shot | 展示全身、肢体动作 | 动作、多人对话 |
| **中景** | Medium Shot | 腰部以上 | 标准对话、互动 |
| **近景** | Close Up | 胸部以上 | 强调表情、台词 |
| **特写** | Extreme Close Up | 局部细节 | 眼睛、手部、关键道具 |
| **过肩镜头** | Over the Shoulder (OTS) | 越过肩膀看对象 | 对话、对峙 |
| **主观镜头** | POV Shot | 角色视角 | 代入感、惊悚、发现 |
| **荷兰角** | Dutch Angle | 倾斜构图 | 不安、混乱、紧张 |

### 2. 运镜方式 (Camera Movement)

| 术语 | 英文 | 描述 |
| :--- | :--- | :--- |
| **固定** | Static / Locked-off | 镜头不动 |
| **推** | Dolly In / Push In | 镜头向前移动 |
| **拉** | Dolly Out / Pull Out | 镜头向后移动 |
| **摇** | Pan (Left/Right) | 镜头水平转动 |
| **俯仰** | Tilt (Up/Down) | 镜头垂直转动 |
| **跟拍** | Tracking / Trucking | 跟随主体移动 |
| **升降** | Crane / Jib | 镜头垂直升降 |
| **环绕** | Arc / Orbit | 围绕主体旋转 |
| **手持** | Handheld | 模拟手持晃动感 |
| **希区柯克变焦** | Dolly Zoom | 推拉结合变焦 |

### 3. 构图法则 (Composition Rules)

*   **三分法 (Rule of Thirds)**：将主体放在画面三分线交点。
*   **中心构图 (Center Framing)**：强调对称、庄重或压抑。
*   **引导线 (Leading Lines)**：利用线条引导视线指向主体。
*   **景深 (Depth of Field)**：
    *   *浅景深 (Shallow Focus)*：虚化背景，突出主体。
    *   *深景深 (Deep Focus)*：前后景都清晰，展示环境关系。

## 类型化分镜模板 (Genre Templates)

### 动作片 (Action)
*   快节奏剪辑 (Fast Cutting)
*   大量特写 (Impact Close-ups)
*   动态运镜 (Shaky Cam / Handheld)
*   荷兰角 (Dutch Angles)

### 恐怖片 (Horror)
*   缓慢推镜头 (Slow Creep / Push In)
*   广角畸变 (Wide Angle Distortion)
*   大量留白 (Negative Space)
*   遮挡构图 (Obscured Framing)

### 爱情片 (Romance)
*   柔光滤镜 (Soft Focus)
*   浅景深 (Shallow DoF)
*   缓慢环绕 (Slow Orbit)
*   温暖色调 (Warm Tones)

## 输出格式

```markdown
## 场次 X 分镜设计表

| 镜头号 | 景别 | 运镜 | 角度 | 画面内容 (Prompt Basis) | 备注/音频 | 时长 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 远景 | 固定 | 平视 | 清晨的古寺全景，薄雾缭绕，远处钟声回荡。 | SFX: 钟声 | 5s |
| 2 | 中景 | 缓慢推 | 俯拍 | 扫地僧在院中清扫落叶，背影沧桑。 | | 3s |
| 3 | 特写 | 固定 | 平视 | 扫帚扫过地面的细节，扬起微尘。 | SFX: 扫地声 | 2s |
```

## 连续性检查 (Continuity Check)

*   **180度轴线原则 (180-Degree Rule)**：确保人物空间关系不混乱。
*   **视线匹配 (Eyeline Match)**：A看左边，B必须看右边。
*   **动作连贯 (Action Continuity)**：上个镜头迈左脚，下个镜头需接上。
*   **光影一致 (Lighting Consistency)**：光源方向不能随意跳变。

## 使用方式

```
请为以下场次设计分镜，风格为[类型]：
[粘贴剧本]
```

## 注意事项

- 必须明确标注通过镜头语言传达的情绪。
- 每个镜头必须包含足够生成 AI 图片的细节（光影、构图、主体状态）。
- 转场描述要具体（如：*匹配剪辑 Match Cut*、*划像 Wipe*）。
