# 🚀 直接给 Claude Code 的执行 Prompt

> 以下内容直接复制粘贴到 Claude Code 的对话框中即可。建议分阶段执行，每段执行完确认无误后再执行下一段。

---

## ✅ 第一段 Prompt — Phase 1：精简（删除非 Claude 平台代码）

```
请帮我对当前项目进行大幅精简。这个项目原本是一个多平台 AI 开发工作流框架（支持 Claude Code、Cursor、iFlow、OpenCode、Codex），我现在要把它改造为仅支持 Claude Code 的 AI 漫剧/连续剧生成工作流 CLI 工具。

第一步，请完成以下精简操作：

1. **删除以下配置器文件**：
   - src/configurators/cursor.ts
   - src/configurators/iflow.ts
   - src/configurators/opencode.ts
   - src/configurators/codex.ts

2. **删除以下模板目录**（整个目录）：
   - src/templates/cursor/
   - src/templates/iflow/
   - src/templates/opencode/
   - src/templates/codex/

3. **删除以下项目根目录的工具配置**（整个目录）：
   - .cursor/
   - .opencode/
   - .agents/

4. **修改类型定义** `src/types/ai-tools.ts`：
   - AITool 类型仅保留 "claude-code"
   - TemplateDir 类型仅保留 "common" | "claude"
   - CliFlag 类型仅保留 "claude"
   - AI_TOOLS 对象仅保留 "claude-code" 条目，删除 cursor/opencode/iflow/codex

5. **修改配置器注册** `src/configurators/index.ts`：
   - 删除所有非 Claude 的 import
   - PLATFORM_FUNCTIONS 仅保留 "claude-code" 条目
   - 删除对 cursor/iflow/opencode/codex 模板的 import

6. **修改 CLI 入口** `src/cli/index.ts`：
   - 删除 --cursor、--iflow、--opencode、--codex 等 CLI 选项

7. **修改 init 命令** `src/commands/init.ts`：
   - 删除多工具选择逻辑，InitOptions 中删除非 Claude 的 flag
   - 初始化时默认且仅配置 Claude Code

8. **修改 update 命令** `src/commands/update.ts`：
   - 删除多平台遍历逻辑，仅更新 Claude Code 模板

9. **修改模板提取** `src/templates/extract.ts`：
   - 删除非 Claude 模板路径的导出函数

10. **检查并修改** `src/migrations/` 目录，删除涉及 cursor/iflow/opencode/codex 的迁移脚本

11. **清理测试** `test/`：删除涉及被删平台的测试用例

12. 完成后运行 `pnpm build` 和 `pnpm test` 确保编译通过且测试通过

每修改一个文件后都要检查是否有死引用（import 指向已删除的文件），全部清理干净。最后给我一个修改总结。
```

---

## ✅ 第二段 Prompt — Phase 2：改名换牌

```
接下来进行品牌重命名。将项目从 Trellis 改名为 AIM Studio（AI 漫剧工作室）。

1. **修改 package.json**：
   - name: "@mindfoldhq/trellis" → 改为你建议的新 scope/名称（如 "aim-studio-cli" 或我的 npm 用户名 scope）
   - description: 改为 "AI 漫剧 & 连续剧生成工作流 CLI — 从剧本到分镜到成片的全链路 AI 创作框架"
   - bin: "trellis"/"tl" → "aim"
   - keywords: 改为 ["ai", "comic", "drama", "manga", "video-generation", "image-generation", "storyboard", "prompt-engineering", "claude-code", "workflow", "cli"]
   - author: 改为 "你的名字"（先用占位符 "YOUR_NAME"）
   - license: 改为 "MIT"

2. **重命名 bin 文件**：bin/trellis.js → bin/aim.js，并更新内部引用

3. **全局搜索替换**（谨慎执行，逐一确认）：
   - `.trellis` 目录名/引用 → `.aim-studio`
   - `trellis` CLI 命令名 → `aim`
   - `Trellis` 显示名 → `AIM Studio`
   - `@mindfoldhq/trellis` → 新包名

4. **更新 src/constants/** 中的品牌引用

5. 完成后运行 `pnpm build` 确保编译通过。给我一个改动总结。
```

---

## ✅ 第三段 Prompt — Phase 3：注入漫剧创作 Skill

```
现在进行核心转型。请读取 aim-prompt/ 目录下的以下文件作为参考：
- aim-prompt/02-漫剧工作流设计prompt.md（工作流设计）
- aim-prompt/03-ClaudeCode-Skill适配prompt.md（Skill 编写规范）
- aim-prompt/图片生成优化skill.md（已有的图片 Skill）
- aim-prompt/视频生成优化skill.md（已有的视频 Skill）

基于这些参考文档，完成以下操作：

1. **创建 Skill 文件**，放在 `src/templates/claude/skills/` 目录下：
   - `script-parser.md` — 剧本解析技能（将自由格式剧本解析为结构化场景）
   - `storyboard-designer.md` — 分镜设计技能（从场景列表生成分镜表）
   - `character-manager.md` — 角色一致性管理技能（角色卡创建与维护）
   - `image-prompt-optimizer.md` — 复制并适配自 aim-prompt/图片生成优化skill.md，增加角色卡注入机制
   - `video-prompt-optimizer.md` — 复制并适配自 aim-prompt/视频生成优化skill.md，增加角色卡注入机制
   - `style-keeper.md` — 风格统一技能（画风/色彩/渲染风格锁定）
   - `episode-manager.md` — 集数管理技能（多集项目管理）

2. **创建 Slash 命令文件**，放在 `src/templates/claude/commands/aim/` 目录下：
   - `new-project.md` — 初始化新漫剧项目
   - `new-episode.md` — 新建一集
   - `new-character.md` — 新建角色卡
   - `parse-script.md` — 解析剧本
   - `storyboard.md` — 生成分镜
   - `prompts.md` — 批量生成提示词
   - `status.md` — 查看项目进度

3. **改造 Agent 定义**，替换 `src/templates/claude/agents/` 下的原有 agent：
   - `director.md` — 创作总监（路由+协调）
   - `writer.md` — 编剧助手
   - `storyboard-artist.md` — 分镜师
   - `prompt-engineer.md` — 提示词工程师
   - 删除原有的 dispatch.md / implement.md / check.md / research.md

4. **更新 settings.json** — 更新 hook 配置以适配新的命令和 agent

5. **更新模板注册**：确保 `src/templates/claude/index.ts`（或相关文件）正确导出新增的 skills/commands/agents

6. 每个 Skill 文件必须遵循以下格式：
   - 包含技能标识（名称/版本/用途）
   - 清晰的输入/输出规范
   - 至少一个完整示例
   - 自检清单
   - 常见错误规避表

完成后运行 `pnpm build` 确保编译通过。
```

---

## ✅ 第四段 Prompt — Phase 4：文档重写

```
请重写项目文档：

1. **重写 README.md**：
   - 项目名：AIM Studio
   - 一句话介绍：AI 漫剧 & 连续剧生成工作流 CLI
   - 安装方式：npm install -g 包名
   - 快速开始：aim init → Claude Code 中使用 /aim:命令
   - 功能列表：剧本解析 / 角色一致性 / 图片提示词 / 视频提示词 / 风格锁定 / 集数管理
   - 用中文写

2. **删除不需要的文档**：
   - README_CN.md（合并到 README.md）
   - CONTRIBUTING.md 和 CONTRIBUTING_CN.md（个人项目不需要）
   - docs/ 下不再适用的指南

3. **重写 CLAUDE.md**：面向 Claude Code 的项目技术说明，描述新项目的结构和用途

4. **创建新的 LICENSE 文件**：MIT 许可证

5. 完成后给我总结。
```

---

## ✅ 第五段 Prompt — Phase 5：验证与发布准备

```
最后验证阶段：

1. 运行 `pnpm build`，确保零错误
2. 运行 `pnpm test`，修复任何失败的测试
3. 运行 `npm pack`，检查包内容和大小
4. 检查 dist/templates/claude/skills/ 目录是否包含所有 Skill 文件
5. 检查 dist/templates/claude/commands/ 目录是否包含所有命令文件
6. 确认 bin/aim.js 正确指向入口
7. 给我一个最终的项目状态报告，包括：
   - 文件结构树
   - 功能清单
   - npm 包信息
   - 还有什么遗留问题需要处理
```

---

## 💡 使用说明

1. **打开 Claude Code**，确保工作目录是 `d:\Desktop\Trellis`
2. **依次复制粘贴**上面 5 段 Prompt（每段用 ` ``` ` 包裹的内容就是要粘贴的）
3. **每段执行完后确认无误**，再执行下一段
4. 如果某一步出错，让 Claude Code 修复后再继续
5. 全部完成后执行 `npm publish` 发布到 npm
