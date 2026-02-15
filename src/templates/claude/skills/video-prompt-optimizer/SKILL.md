---
name: video-prompt-optimizer
description: 视频提示词优化器 — 生成 Seedance / Kling / Sora 优化的视频提示词
---

# Video Prompt Optimizer（视频提示词优化器）

生成高度优化的 AI 视频提示词，涵盖动态物理、运镜权重及运动幅度控制。

## 平台特定优化策略

### 1. Seedance (动作捕捉与物理)

*   **优势**：精准动作控制、物理模拟（布料/流体）。
*   **策略**：强调动作的起止点，描述物理各属性。
*   **格式**：YAML 或 JSON 风格的结构化描述。
*   **时长**：5s (最佳质量) / 10s.

### 2. Kling (AI 视频生成)

*   **优势**：长达 2 分钟，电影级画质，自然的人物动态。
*   **策略**：详细的电影剧本式描述，包含环境变化。
*   **参数**：`--camera_zoom 1.5 --motion_bucket 6`

### 3. Sora / Runway Gen-3 (场景模拟)

*   **优势**：极其复杂的场景交互，多主体一致性。
*   **策略**：全景式描述，包含时间流逝和因果关系。

## 核心参数库

### 1. 物理模拟标签 (Physics Tags)

*   **流体**：`Fluid simulation, splashing water, flowing river, smoke turbulence`
*   **布料**：`Cloth physics, dress blowing in wind, heavy fabric movement`
*   **毛发**：`Hair physics, windblown hair, fur simulation`
*   **粒子**：`Particle effects, sparks, dust motes, rain, snow`
*   **破坏**：`Destruction physics, shattering glass, collapsing wall`

### 2. 运动控制 (Motion Control)

#### 运动幅度 (Motion Bucket)
*   **Low Motion (1-3)**：只有微表情，背景几乎静止。适合对话、特写。
*   **Medium Motion (4-6)**：正常行走、手势、环境自然摆动。适合叙事。
*   **High Motion (7-10)**：奔跑、打斗、爆炸、快速运镜。适合动作戏。

#### 运镜权重 (Camera Weights)
使用括号加权重来控制运镜强度：
*   `(Camera Zoom In: 1.5)`
*   `(Camera Pan Right: 0.8)`
*   `(Camera Shake: 2.0)` - 模拟地震或爆炸冲击

### 3. 时间流逝 (Temporal Descriptions)

*   `Time-lapse of [Scene]`：延时摄影（花开、日落）。
*   `Slow motion (60fps/120fps)`：慢动作。
*   `Hyper-lapse`：大范围移动延时。
*   `Reverse motion`：倒放。

## 输出模板

### Seedance / Standard Video Prompt

```markdown
## 视频生成参数表 (Video Generation Sheet)

**主提示词 (Main Prompt)**:
A cinematic shot of [Subject]. [Action description: Start -> End]. 
[Environment details]. [Lighting & Style].
high quality, 8k, photorealistic.

**运镜指令 (Camera Control)**:
- Movement: [Pan/Tilt/Zoom/Truck]
- Speed: [Slow/Normal/Fast]
- Shake: [None/Handheld/Earthquake]

**物理与特效 (Physics & FX)**:
- [Physics Tag 1]
- [Physics Tag 2]

**参数设置 (Settings)**:
- Duration: [5s/10s]
- Motion Bucket: [1-10]
- FPS: 24
- Seed: [Optional]
```

## 动态动作描述技巧 (Dynamic Action Guide)

描述动作时，必须包含**时间维度的变化**：

*   ❌ *Bad*: "A man calculates."
*   ✅ *Good*: "A man stands at a blackboard, *furiously writing* equations, then *pauses to scratch his head*, chalk dust floating in the air."

*   ❌ *Bad*: "A car drives."
*   ✅ *Good*: "A red sports car *drifts around a corner*, tires smoking, headlights *sweeping across* the wet pavement."

## 使用方式

```
请为以下分镜生成视频提示词，主要动作是[动作]：
[分镜描述]
```

## 注意事项

- **避免变形**：过大的 Motion Bucket (8+) 容易导致人物肢体变形。
- **一致性**：同一场戏的多个镜头，Seed 值和 Prompt 前缀保持一致。
- **负面提示**：`morphing, distortion, disjointed limbs, flickering`。
