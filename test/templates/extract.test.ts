import { describe, expect, it } from "vitest";
import fs from "node:fs";
import {
  getAimTemplatePath,
  getClaudeTemplatePath,
  getAimSourcePath,
  getClaudeSourcePath,
  readAimFile,
  readTemplate,
  readScript,
  readMarkdown,
  readClaudeFile,
} from "../../src/templates/extract.js";

// =============================================================================
// getXxxTemplatePath — returns existing directory paths
// =============================================================================

describe("template path functions", () => {
  it("getAimTemplatePath returns existing directory", () => {
    const p = getAimTemplatePath();
    expect(fs.existsSync(p)).toBe(true);
    expect(fs.statSync(p).isDirectory()).toBe(true);
  });

  it("getClaudeTemplatePath returns existing directory", () => {
    const p = getClaudeTemplatePath();
    expect(fs.existsSync(p)).toBe(true);
    expect(fs.statSync(p).isDirectory()).toBe(true);
  });
});

// =============================================================================
// Deprecated aliases return same result
// =============================================================================

describe("deprecated source path aliases", () => {
  it("getAimSourcePath equals getAimTemplatePath", () => {
    expect(getAimSourcePath()).toBe(getAimTemplatePath());
  });

  it("getClaudeSourcePath equals getClaudeTemplatePath", () => {
    expect(getClaudeSourcePath()).toBe(getClaudeTemplatePath());
  });
});

// =============================================================================
// readTrellisFile — reads files from trellis template directory
// =============================================================================

describe("readAimFile", () => {
  it("reads workflow.md from aim templates", () => {
    const content = readAimFile("workflow.md");
    expect(typeof content).toBe("string");
    expect(content.length).toBeGreaterThan(0);
    expect(content).toContain("#"); // markdown heading
  });

  it("reads a script file", () => {
    const content = readAimFile("scripts/task.py");
    expect(typeof content).toBe("string");
    expect(content.length).toBeGreaterThan(0);
  });

  it("throws for nonexistent file", () => {
    expect(() => readAimFile("nonexistent.txt")).toThrow();
  });
});

// =============================================================================
// readTemplate — reads from category subdirectories
// =============================================================================

describe("readTemplate", () => {
  it("throws for nonexistent category/file", () => {
    expect(() => readTemplate("scripts", "nonexistent.txt")).toThrow();
  });
});

// =============================================================================
// readScript — helper wrapping readTrellisFile
// =============================================================================

describe("readScript", () => {
  it("reads a Python script from scripts/", () => {
    const content = readScript("task.py");
    expect(typeof content).toBe("string");
    expect(content.length).toBeGreaterThan(0);
  });
});

// =============================================================================
// readMarkdown — helper wrapping readTrellisFile
// =============================================================================

describe("readMarkdown", () => {
  it("reads workflow.md", () => {
    const content = readMarkdown("workflow.md");
    expect(typeof content).toBe("string");
    expect(content).toContain("#");
  });
});

// =============================================================================
// Platform file readers
// =============================================================================

describe("readClaudeFile", () => {
  it("reads settings.json from claude templates", () => {
    const content = readClaudeFile("settings.json");
    expect(typeof content).toBe("string");
    expect(content.length).toBeGreaterThan(0);
    // Should be valid JSON
    expect(() => JSON.parse(content)).not.toThrow();
  });
});

