import { readFileSync, readdirSync, statSync } from "node:fs";
import path from "node:path";
import { getOpencodeTemplatePath } from "../templates/extract.js";
import { ensureDir, writeFile } from "../utils/file-writer.js";

/**
 * Files to exclude when copying templates
 * These are TypeScript compilation artifacts
 */
const EXCLUDE_PATTERNS = [
  ".d.ts",
  ".d.ts.map",
  ".js",
  ".js.map",
  "__pycache__",
];

/**
 * Check if a file should be excluded
 */
function shouldExclude(filename: string): boolean {
  for (const pattern of EXCLUDE_PATTERNS) {
    if (filename.endsWith(pattern) || filename === pattern) {
      return true;
    }
  }
  return false;
}

/**
 * Recursively copy directory, excluding build artifacts
 * Uses writeFile to handle file conflicts with the global writeMode setting
 */
async function copyDirFiltered(src: string, dest: string): Promise<void> {
  ensureDir(dest);

  for (const entry of readdirSync(src)) {
    if (shouldExclude(entry)) {
      continue;
    }

    const srcPath = path.join(src, entry);
    const destPath = path.join(dest, entry);
    const stat = statSync(srcPath);

    if (stat.isDirectory()) {
      await copyDirFiltered(srcPath, destPath);
    } else {
      const content = readFileSync(srcPath, "utf-8");
      await writeFile(destPath, content);
    }
  }
}

/**
 * Configure OpenCode by copying from templates
 *
 * The opencode templates include:
 * - commands/aim/ - Slash commands
 * - agents/ - Agent definitions
 * - lib/ - Shared library code
 * - plugin/ - Plugin hooks
 */
export async function configureOpencode(cwd: string): Promise<void> {
  const sourcePath = getOpencodeTemplatePath();
  const destPath = path.join(cwd, ".opencode");

  // Copy templates, excluding build artifacts
  await copyDirFiltered(sourcePath, destPath);
}
