import * as fs from "node:fs";
import * as path from "node:path";
import { fileURLToPath } from "node:url";
import { ensureDir, writeFile } from "../utils/file-writer.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

type TemplateCategory = "scripts" | "markdown" | "commands";

/**
 * Get the path to the aim templates directory.
 *
 * This reads from src/templates/aim/ (development) or dist/templates/aim/ (production).
 * These are GENERIC templates, not the project's own .aim-studio/ configuration.
 */
export function getAimTemplatePath(): string {
  // Templates are in the same directory as this file
  const templatePath = path.join(__dirname, "aim");
  if (fs.existsSync(templatePath)) {
    return templatePath;
  }

  throw new Error(
    "Could not find aim templates directory. Expected at templates/aim/",
  );
}

/**
 * @deprecated Use getAimTemplatePath() instead.
 * This function is kept for backwards compatibility but now returns the template path.
 */
export function getAimSourcePath(): string {
  return getAimTemplatePath();
}

/**
 * Get the path to the claude templates directory.
 *
 * This reads from src/templates/claude/ (development) or dist/templates/claude/ (production).
 */
export function getClaudeTemplatePath(): string {
  const templatePath = path.join(__dirname, "claude");
  if (fs.existsSync(templatePath)) {
    return templatePath;
  }

  throw new Error(
    "Could not find claude templates directory. Expected at templates/claude/",
  );
}

/**
 * @deprecated Use getClaudeTemplatePath() instead.
 */
export function getClaudeSourcePath(): string {
  return getClaudeTemplatePath();
}

/**
 * Read a file from the .aim-studio directory
 * @param relativePath - Path relative to .aim-studio/ (e.g., 'scripts/task.py')
 * @returns File content as string
 */
export function readAimFile(relativePath: string): string {
  const aimPath = getAimSourcePath();
  const filePath = path.join(aimPath, relativePath);
  return fs.readFileSync(filePath, "utf-8");
}

/**
 * Read template content from a .txt file in commands directory
 * @param category - Template category (only 'commands' uses .txt files now)
 * @param filename - Template filename (e.g., 'common/finish-work.txt')
 * @returns File content as string
 */
export function readTemplate(
  category: TemplateCategory,
  filename: string,
): string {
  const templatePath = path.join(__dirname, category, filename);
  return fs.readFileSync(templatePath, "utf-8");
}

/**
 * Helper to read script template from .aim-studio/scripts/
 * @param relativePath - Path relative to .aim-studio/scripts/ (e.g., 'task.py')
 */
export function readScript(relativePath: string): string {
  return readAimFile(`scripts/${relativePath}`);
}

/**
 * Helper to read markdown template from .aim-studio/
 * @param relativePath - Path relative to .aim-studio/ (e.g., 'workflow.md')
 */
export function readMarkdown(relativePath: string): string {
  return readAimFile(relativePath);
}

/**
 * Helper to read command template (these still use .txt files in src/templates/commands/)
 */
export function readCommand(filename: string): string {
  return readTemplate("commands", filename);
}

/**
 * Read a file from the .claude directory (dogfooding)
 * @param relativePath - Path relative to .claude/ (e.g., 'commands/start.md')
 * @returns File content as string
 */
export function readClaudeFile(relativePath: string): string {
  const claudePath = getClaudeSourcePath();
  const filePath = path.join(claudePath, relativePath);
  return fs.readFileSync(filePath, "utf-8");
}

/**
 * Copy a directory from .aim-studio/ to target, making scripts executable
 * Uses writeFile to handle file conflicts with the global writeMode setting
 * @param srcRelativePath - Source path relative to .aim-studio/ (e.g., 'scripts')
 * @param destPath - Absolute destination path
 * @param options - Copy options
 */
export async function copyAimDir(
  srcRelativePath: string,
  destPath: string,
  options?: { executable?: boolean },
): Promise<void> {
  const aimPath = getAimSourcePath();
  const srcPath = path.join(aimPath, srcRelativePath);
  await copyDirRecursive(srcPath, destPath, options);
}

/**
 * Recursively copy directory with options
 * Uses writeFile to handle file conflicts
 */
async function copyDirRecursive(
  src: string,
  dest: string,
  options?: { executable?: boolean },
): Promise<void> {
  ensureDir(dest);

  for (const entry of fs.readdirSync(src)) {
    const srcPath = path.join(src, entry);
    const destPath = path.join(dest, entry);
    const stat = fs.statSync(srcPath);

    if (stat.isDirectory()) {
      await copyDirRecursive(srcPath, destPath, options);
    } else {
      const content = fs.readFileSync(srcPath, "utf-8");
      const isExecutable =
        options?.executable && (entry.endsWith(".sh") || entry.endsWith(".py"));
      await writeFile(destPath, content, { executable: isExecutable });
    }
  }
}
