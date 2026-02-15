> [← 返回根目录](../CLAUDE.md) | **src/utils/**
>
> 本模块提供 AIM Studio 项目使用的工具函数。

## 概览

`src/utils/` 包含项目中的工具函数模块。

## 模块索引

| 文件 | 导出 | 职责 |
| --- | --- | --- |
| `compare-versions.ts` | `compareVersions()` | 比较语义化版本 |
| `file-writer.ts` | `FileWriter` | 文件写入和模板渲染 |
| `project-detector.ts` | `detectProject()` | 检测项目类型和框架 |
| `template-fetcher.ts` | `fetchTemplate()` | 从远程获取模板 |
| `template-hash.ts` | `computeHash()` | 计算模板哈希 |

## 关键 API

### compareVersions

```typescript
/**
 * 比较两个语义化版本
 * @returns
 *   - 正数: v1 > v2
 *   - 0: v1 == v2
 *   - 负数: v1 < v2
 */
function compareVersions(v1: string, v2: number): number
```

### FileWriter

```typescript
class FileWriter {
  write(filePath: string, content: string): Promise<void>;
  render(template: string, data: Record<string, unknown>): string;
}
```

### template-fetcher

```typescript
async function fetchTemplate(templateName: string): Promise<TemplateInfo> {
  // 从远程仓库获取模板
}
```

## 使用示例

```typescript
import { compareVersions } from "./utils/compare-versions.js";
import { FileWriter } from "./utils/file-writer.js";

// 版本比较
const cmp = compareVersions("1.2.0", "1.1.0");
// cmp > 0 表示 v1 更新

// 文件写入
const writer = new FileWriter();
await writer.write("./output.md", "# Hello");
```

## 依赖关系

```
src/utils/
├── compare-versions.ts    → src/commands/update.ts
├── file-writer.ts         → src/commands/init.ts
├── project-detector.ts    → src/configurators/
├── template-fetcher.ts    → src/commands/init.ts
└── template-hash.ts       → src/templates/
```

## 相关模块

- [src/commands/](../commands/) - 命令实现
- [src/configurators/](../configurators/) - 配置器
- [src/templates/](../templates/) - 模板系统
