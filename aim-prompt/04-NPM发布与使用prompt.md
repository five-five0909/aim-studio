# 📦 NPM 发布与个人使用 Prompt

> **角色**：你是一个 npm 包发布专家，负责将转型后的 AI 漫剧工作流 CLI 工具配置为可通过 npm 安装使用的个人工具包。

---

## 一、发布前必须完成的配置

### 1.1 npm scope 选择

**推荐方案**：使用个人 npm scope

```json
{
  "name": "@你的npm用户名/aim-studio",
  "publishConfig": {
    "access": "public"
  }
}
```

> 如果不想用 scope，也可以直接用无 scope 包名（需确保全局唯一）：
> `"name": "aim-studio-cli"`

### 1.2 版本策略

```
0.1.0 — 初始版本（最小可用）
0.2.0 — 完善 Skill 内容
0.3.0 — 补充更多 slash 命令
1.0.0 — 稳定版
```

### 1.3 package.json 完整配置

```json
{
  "name": "@你的scope/aim-studio",
  "version": "0.1.0",
  "description": "AI 漫剧 & 连续剧生成工作流 CLI — 从剧本到分镜到成片的全链路 AI 创作框架",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "bin": {
    "aim": "./bin/aim.js"
  },
  "publishConfig": {
    "access": "public"
  },
  "scripts": {
    "build": "tsc && pnpm run copy-templates",
    "copy-templates": "node scripts/copy-templates.js",
    "dev": "tsc --watch",
    "start": "node ./dist/cli/index.js",
    "test": "vitest run",
    "lint": "eslint src/",
    "format": "prettier --write src/",
    "prepublishOnly": "pnpm run build",
    "release": "pnpm version patch && npm publish"
  },
  "keywords": [
    "ai",
    "comic",
    "drama",
    "manga",
    "video-generation",
    "image-generation",
    "storyboard",
    "prompt-engineering",
    "claude-code",
    "workflow",
    "cli"
  ],
  "author": "你的作者名",
  "license": "MIT",
  "files": [
    "dist",
    "bin",
    "README.md",
    "LICENSE"
  ],
  "engines": {
    "node": ">=18.0.0"
  },
  "repository": {
    "type": "git",
    "url": "你的仓库地址"
  }
}
```

---

## 二、bin 文件配置

### `bin/aim.js`

```javascript
#!/usr/bin/env node

import '../dist/cli/index.js';
```

> 确保该文件有可执行权限（Linux/Mac），Windows 下 npm 会自动处理。

---

## 三、files 字段审查

`"files"` 字段决定 npm 包中包含哪些文件。必须确保：

### 3.1 必须包含
- `dist/` — 编译后的 JS + 类型声明
- `bin/` — CLI 入口
- `README.md` — 使用说明

### 3.2 必须排除（通过 `.npmignore` 或 `files` 白名单）
- `src/` — TypeScript 源码（不需要发布）
- `test/` — 测试文件
- `aim-prompt/` — Prompt 文档（开发用，不发布）
- `.trellis/` — 项目自身的配置
- `.claude/` — 项目自身的 Claude 配置
- `.github/` — GitHub 配置
- `assets/` — 项目文档图片
- `pnpm-lock.yaml`
- `*.config.*` — 构建工具配置

### 3.3 关键检查：模板文件是否包含在 dist 中

Trellis 原项目通过 `scripts/copy-templates.js` 将模板文件复制到 `dist/` 目录中。**必须确保**：

1. `copy-templates.js` 脚本正确复制了新的模板目录（包括 skills/）
2. `dist/templates/` 中包含所有 `.md` / `.py` / `.json` 模板文件
3. `src/templates/extract.ts` 中的路径解析正确指向 `dist/templates/`

```bash
# 验证方法
pnpm build
ls dist/templates/claude/skills/     # 应该看到所有 Skill 文件
ls dist/templates/claude/commands/   # 应该看到所有命令文件
```

---

## 四、发布前验证流程

### 4.1 本地打包测试

```bash
# 1. 构建
pnpm build

# 2. 本地打包
npm pack

# 3. 检查包内容
tar -tzf 你的scope-aim-studio-0.1.0.tgz | head -50

# 4. 检查包大小（建议 < 500KB）
ls -la 你的scope-aim-studio-0.1.0.tgz
```

### 4.2 本地安装测试

```bash
# 1. 全局安装本地包
npm install -g ./你的scope-aim-studio-0.1.0.tgz

# 2. 测试 CLI 命令
aim --help
aim --version

# 3. 在测试目录中初始化
mkdir test-project && cd test-project
aim init

# 4. 检查生成的目录结构
ls -la .aim-studio/
ls -la .claude/skills/
ls -la .claude/commands/

# 5. 卸载
npm uninstall -g @你的scope/aim-studio
```

### 4.3 发布到 npm

```bash
# 1. 登录 npm
npm login

# 2. 发布
npm publish

# 3. dry-run（仅验证，不实际发布）
npm publish --dry-run
```

---

## 五、发布后使用方式

### 5.1 安装

```bash
npm install -g @你的scope/aim-studio@latest
```

### 5.2 日常使用

```bash
# 1. 在项目目录初始化
cd my-comic-project
aim init

# 2. 启动 Claude Code 开始创作
# Claude 会自动加载所有 Skill + 命令

# 3. 在 Claude Code 中使用
# /aim:new-project → 创建新漫剧项目
# /aim:new-character → 创建角色卡
# /aim:parse-script → 解析剧本
# /aim:storyboard → 生成分镜
# /aim:prompts → 生成提示词
```

### 5.3 更新

```bash
# 更新工具本身
npm install -g @你的scope/aim-studio@latest

# 更新项目中的 Skill/命令
cd my-comic-project
aim update
```

---

## 六、许可证选择

### 个人使用推荐

| 许可证 | 适用场景 |
| --- | --- |
| **MIT** | 最宽松，个人项目推荐 |
| **ISC** | 类似 MIT，更简短 |
| **Unlicense** | 完全放弃版权，极简 |

> ⚠️ **注意**：原项目使用 AGPL-3.0-only，转型后如果你是个人使用且重写了大部分代码，建议更换为 MIT。如果大量保留原始代码，需遵循 AGPL-3.0 的要求。

### 许可证修改

```diff
# package.json
- "license": "AGPL-3.0-only"
+ "license": "MIT"
```

替换 `LICENSE` 文件内容为 MIT 许可证文本。

---

## 七、README.md 模板

```markdown
# 🎬 AIM Studio

> AI 漫剧 & 连续剧生成工作流 CLI — 从剧本到分镜到成片

## 安装

\`\`\`bash
npm install -g @你的scope/aim-studio@latest
\`\`\`

## 快速开始

\`\`\`bash
# 在项目目录初始化
aim init

# 在 Claude Code 中使用 slash 命令创作
/aim:new-project       # 创建新漫剧项目
/aim:new-character     # 创建角色卡
/aim:parse-script      # 解析剧本
/aim:storyboard        # 生成分镜
/aim:prompts           # 生成图片/视频提示词
\`\`\`

## 功能

- 🎭 **剧本解析** — 自由文本 → 结构化场景
- 🎨 **角色一致性** — 角色卡系统确保跨镜头一致
- 🖼️ **图片提示词** — 适配 Qwen-Image/FLUX 等多模型
- 🎬 **视频提示词** — 适配 Seedance/可灵等视频模型
- 🎯 **风格锁定** — 全剧画风/色调统一
- 📖 **集数管理** — 多集连续剧项目管理

## 许可证

MIT
```

---

## 八、CI/CD 建议（可选）

如果后续需要自动化发布：

```yaml
# .github/workflows/publish.yml
name: Publish to npm
on:
  push:
    tags:
      - 'v*'
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          registry-url: https://registry.npmjs.org
      - run: npm install -g pnpm
      - run: pnpm install
      - run: pnpm build
      - run: pnpm test
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

---

## 九、发布检查清单

- [ ] `package.json` 中的 `name` / `version` / `description` 已更新？
- [ ] `bin` 字段指向正确的 CLI 入口文件？
- [ ] `files` 字段包含 `dist` / `bin` / `README.md`？
- [ ] `dist/templates/` 中包含所有模板文件（特别是 skills/）？
- [ ] `npm pack` 打出的包大小合理（< 500KB）？
- [ ] 本地全局安装测试 `aim init` 正常工作？
- [ ] `.claude/skills/` 目录正确生成？
- [ ] 许可证已更换（如需要）？
- [ ] README.md 已更新为新项目说明？
- [ ] `npm publish --dry-run` 无错误？

---

**本 Prompt 为 npm 发布的完整指南，确保打包正确、模板文件完整、CLI 可用。**
