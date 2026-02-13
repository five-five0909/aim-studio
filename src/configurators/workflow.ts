import path from "node:path";

import { DIR_NAMES, PATHS } from "../constants/paths.js";
import { copyAimDir } from "../templates/extract.js";

// Import aim templates (generic, not project-specific)
import {
  workflowMdTemplate,
  worktreeYamlTemplate,
  gitignoreTemplate,
} from "../templates/aim/index.js";

// Import markdown templates
import {
  agentProgressIndexContent,
  // Story structure (for comic/novel creation)
  storyIndexContent,
  storyCharacterContent,
  storyWorldContent,
  storyScriptContent,
} from "../templates/markdown/index.js";

import { writeFile, ensureDir } from "../utils/file-writer.js";
import type { ProjectType } from "../utils/project-detector.js";

interface DocDefinition {
  name: string;
  content: string;
}

/**
 * Options for creating workflow structure
 */
export interface WorkflowOptions {
  /** Detected or specified project type */
  projectType: ProjectType;
  /** Enable multi-agent pipeline with worktree support */
  multiAgent?: boolean;
  /** Skip creating local spec templates (when using remote template) */
  skipSpecTemplates?: boolean;
}

/**
 * Create workflow structure based on project type
 *
 * This function creates the .aim-studio/ directory structure by:
 * 1. Copying scripts/ directory directly (dogfooding)
 * 2. Copying workflow.md and .gitignore (dogfooding)
 * 3. Creating workspace/ with index.md
 * 4. Creating tasks/ directory
 * 5. Creating spec/ with templates (not dogfooded - generic templates)
 * 6. Copying worktree.yaml if multi-agent is enabled
 *
 * @param cwd - Current working directory
 * @param options - Workflow options including project type
 */
export async function createWorkflowStructure(
  cwd: string,
  options?: WorkflowOptions,
): Promise<void> {
  const projectType = options?.projectType ?? "fullstack";
  const multiAgent = options?.multiAgent ?? false;
  const skipSpecTemplates = options?.skipSpecTemplates ?? false;

  // Create base .aim-studio directory
  ensureDir(path.join(cwd, DIR_NAMES.WORKFLOW));

  // Copy scripts/ directory from templates
  await copyAimDir("scripts", path.join(cwd, PATHS.SCRIPTS), {
    executable: true,
  });

  // Copy workflow.md from templates
  await writeFile(
    path.join(cwd, PATHS.WORKFLOW_GUIDE_FILE),
    workflowMdTemplate,
  );

  // Copy .gitignore from templates
  await writeFile(
    path.join(cwd, DIR_NAMES.WORKFLOW, ".gitignore"),
    gitignoreTemplate,
  );

  // Create workspace/ with index.md
  ensureDir(path.join(cwd, PATHS.WORKSPACE));
  await writeFile(
    path.join(cwd, PATHS.WORKSPACE, "index.md"),
    agentProgressIndexContent,
  );

  // Create tasks/ directory
  ensureDir(path.join(cwd, PATHS.TASKS));

  // Copy worktree.yaml if multi-agent enabled
  if (multiAgent) {
    await writeFile(
      path.join(cwd, DIR_NAMES.WORKFLOW, "worktree.yaml"),
      worktreeYamlTemplate,
    );
  }

  // Create spec templates based on project type
  // These are NOT dogfooded - they are generic templates for new projects
  // Skip if using remote template (already downloaded)
  if (!skipSpecTemplates) {
    await createSpecTemplates(cwd, projectType);
  }
}

async function createSpecTemplates(
  cwd: string,
  projectType: ProjectType,
): Promise<void> {
  // Ensure spec directory exists
  ensureDir(path.join(cwd, PATHS.SPEC));

  // Only create story spec (for comic/novel creation)
  if (projectType === "story") {
    ensureDir(path.join(cwd, `${PATHS.SPEC}/story`));
    const storyDocs: DocDefinition[] = [
      { name: "index.md", content: storyIndexContent },
      { name: "character.md", content: storyCharacterContent },
      { name: "world.md", content: storyWorldContent },
      { name: "script.md", content: storyScriptContent },
    ];

    for (const doc of storyDocs) {
      await writeFile(
        path.join(cwd, `${PATHS.SPEC}/story`, doc.name),
        doc.content,
      );
    }
  }
}
