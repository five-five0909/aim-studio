/**
 * Markdown templates for AIM Studio workflow
 *
 * These are GENERIC templates for new projects.
 * Structure templates use .md.txt extension as they are generic templates.
 */

import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/**
 * Read a template file from src/templates/markdown/
 */
function readLocalTemplate(filename: string): string {
  const filePath = join(__dirname, filename);
  return readFileSync(filePath, "utf-8");
}

// =============================================================================
// Root files for new projects
// =============================================================================

export const agentsMdContent: string = readLocalTemplate("agents.md");

// Workspace index template (developer work records)
export const workspaceIndexContent: string =
  readLocalTemplate("workspace-index.md");

// Backwards compatibility alias
export const agentProgressIndexContent = workspaceIndexContent;

// Gitignore (template file - .gitignore is ignored by npm)
export const workflowGitignoreContent: string =
  readLocalTemplate("gitignore.txt");

// =============================================================================
// Story structure templates (for AI comic/novel creation)
// =============================================================================

export const storyIndexContent: string = readLocalTemplate(
  "spec/story/index.md.txt",
);
export const storyCharacterContent: string = readLocalTemplate(
  "spec/story/character.md.txt",
);
export const storyWorldContent: string = readLocalTemplate(
  "spec/story/world.md.txt",
);
export const storyScriptContent: string = readLocalTemplate(
  "spec/story/script.md.txt",
);
export const styleGuideContent: string = readLocalTemplate(
  "spec/story/style-guide.md.txt",
);
