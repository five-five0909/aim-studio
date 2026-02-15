/**
 * OpenCode templates
 *
 * These are GENERIC templates for user projects.
 *
 * Directory structure:
 *   opencode/
 *   ├── commands/       # Slash commands
 *   ├── agents/         # Multi-agent pipeline agents
 *   ├── lib/            # Shared library code
 *   └── plugin/         # Plugin hooks
 */

import { readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

function readTemplate(relativePath: string): string {
  return readFileSync(join(__dirname, relativePath), "utf-8");
}

function listFiles(dir: string): string[] {
  try {
    return readdirSync(join(__dirname, dir));
  } catch {
    return [];
  }
}

/**
 * Command template with name and content
 */
export interface CommandTemplate {
  name: string;
  content: string;
}

/**
 * Agent template with name and content
 */
export interface AgentTemplate {
  name: string;
  content: string;
}

/**
 * Plugin file template with target path and content
 */
export interface PluginTemplate {
  targetPath: string;
  content: string;
}

/**
 * Get all command templates
 * Commands are stored in commands/aim/ subdirectory
 * This creates commands like /aim:start, /aim:finish-work, etc.
 */
export function getAllCommands(): CommandTemplate[] {
  const commands: CommandTemplate[] = [];
  const files = listFiles("commands/aim");

  for (const file of files) {
    if (file.endsWith(".md")) {
      const name = file.replace(".md", "");
      const content = readTemplate(`commands/aim/${file}`);
      commands.push({ name, content });
    }
  }

  return commands;
}

/**
 * Get all agent templates
 */
export function getAllAgents(): AgentTemplate[] {
  const agents: AgentTemplate[] = [];
  const files = listFiles("agents");

  for (const file of files) {
    if (file.endsWith(".md")) {
      const name = file.replace(".md", "");
      const content = readTemplate(`agents/${file}`);
      agents.push({ name, content });
    }
  }

  return agents;
}

/**
 * Get all plugin files (lib + plugin directories)
 */
export function getAllPlugins(): PluginTemplate[] {
  const plugins: PluginTemplate[] = [];

  // Read lib files
  const libFiles = listFiles("lib");
  for (const file of libFiles) {
    if (file.endsWith(".js")) {
      const content = readTemplate(`lib/${file}`);
      plugins.push({ targetPath: `lib/${file}`, content });
    }
  }

  // Read plugin files
  const pluginFiles = listFiles("plugin");
  for (const file of pluginFiles) {
    if (file.endsWith(".js")) {
      const content = readTemplate(`plugin/${file}`);
      plugins.push({ targetPath: `plugin/${file}`, content });
    }
  }

  return plugins;
}
