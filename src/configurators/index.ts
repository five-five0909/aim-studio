/**
 * Platform Registry — Single source of truth for platform functions and derived helpers
 *
 * Simplified to only support Claude Code.
 */

import fs from "node:fs";
import path from "node:path";
import { AI_TOOLS, type AITool, type CliFlag } from "../types/ai-tools.js";

// Platform configurators
import { configureClaude } from "./claude.js";

// Shared utilities
import { resolvePlaceholders } from "./shared.js";

// Template content for update tracking
import {
  getAllAgents as getClaudeAgents,
  getAllCommands as getClaudeCommands,
  getAllHooks as getClaudeHooks,
  getSettingsTemplate as getClaudeSettings,
} from "../templates/claude/index.js";

// =============================================================================
// Platform Functions Registry
// =============================================================================

interface PlatformFunctions {
  /** Configure platform during init (copy templates to project) */
  configure: (cwd: string) => Promise<void>;
  /** Collect template files for update tracking. Undefined = platform skipped during update. */
  collectTemplates?: () => Map<string, string>;
}

/**
 * Platform functions registry — maps each AITool to its behavior.
 */
const PLATFORM_FUNCTIONS: Record<AITool, PlatformFunctions> = {
  "claude-code": {
    configure: configureClaude,
    collectTemplates: () => {
      const files = new Map<string, string>();
      // Commands (in trellis/ subdirectory for namespace)
      for (const cmd of getClaudeCommands()) {
        files.set(`.claude/commands/aim/${cmd.name}.md`, cmd.content);
      }
      // Agents
      for (const agent of getClaudeAgents()) {
        files.set(`.claude/agents/${agent.name}.md`, agent.content);
      }
      // Hooks
      for (const hook of getClaudeHooks()) {
        files.set(`.claude/${hook.targetPath}`, hook.content);
      }
      // Settings (resolve {{PYTHON_CMD}} to match what configure() writes)
      const settings = getClaudeSettings();
      files.set(
        `.claude/${settings.targetPath}`,
        resolvePlaceholders(settings.content),
      );
      return files;
    },
  },
};

// =============================================================================
// Derived Helpers — all derived from AI_TOOLS registry
// =============================================================================

/** All platform IDs */
export const PLATFORM_IDS = Object.keys(AI_TOOLS) as AITool[];

/** All platform config directory names */
export const CONFIG_DIRS = PLATFORM_IDS.map((id) => AI_TOOLS[id].configDir);

/** All directories managed by AIM Studio (including .aim-studio itself) */
export const ALL_MANAGED_DIRS = [".aim-studio", ...CONFIG_DIRS];

/**
 * Detect which platforms are configured by checking for directory existence
 */
export function getConfiguredPlatforms(cwd: string): Set<AITool> {
  const platforms = new Set<AITool>();
  for (const id of PLATFORM_IDS) {
    if (fs.existsSync(path.join(cwd, AI_TOOLS[id].configDir))) {
      platforms.add(id);
    }
  }
  return platforms;
}

/**
 * Get platform IDs that have Python hooks (for Windows encoding detection)
 */
export function getPlatformsWithPythonHooks(): AITool[] {
  return PLATFORM_IDS.filter((id) => AI_TOOLS[id].hasPythonHooks);
}

/**
 * Check if a path starts with any managed directory
 */
export function isManagedPath(dirPath: string): boolean {
  // Normalize Windows backslashes to forward slashes for consistent matching
  const normalized = dirPath.replace(/\\/g, "/");
  return ALL_MANAGED_DIRS.some(
    (d) => normalized.startsWith(d + "/") || normalized === d,
  );
}

/**
 * Check if a directory name is a managed root directory (should not be deleted)
 */
export function isManagedRootDir(dirName: string): boolean {
  return ALL_MANAGED_DIRS.includes(dirName);
}

/**
 * Get the configure function for a platform
 */
export function configurePlatform(
  platformId: AITool,
  cwd: string,
): Promise<void> {
  return PLATFORM_FUNCTIONS[platformId].configure(cwd);
}

/**
 * Collect template files for a specific platform (for update tracking).
 * Returns undefined if the platform doesn't support template tracking.
 */
export function collectPlatformTemplates(
  platformId: AITool,
): Map<string, string> | undefined {
  return PLATFORM_FUNCTIONS[platformId].collectTemplates?.();
}

/**
 * Build TOOLS array for interactive init prompt, derived from AI_TOOLS registry
 */
export function getInitToolChoices(): {
  key: CliFlag;
  name: string;
  defaultChecked: boolean;
  platformId: AITool;
}[] {
  return PLATFORM_IDS.map((id) => ({
    key: AI_TOOLS[id].cliFlag,
    name: AI_TOOLS[id].name,
    defaultChecked: AI_TOOLS[id].defaultChecked,
    platformId: id,
  }));
}

/**
 * Resolve CLI flag name to AITool id (e.g., "claude" → "claude-code")
 */
export function resolveCliFlag(flag: string): AITool | undefined {
  return PLATFORM_IDS.find((id) => AI_TOOLS[id].cliFlag === flag);
}
