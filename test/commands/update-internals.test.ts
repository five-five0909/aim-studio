/**
 * Tests for internal helper functions exported from update.ts
 *
 * These test cleanupEmptyDirs and sortMigrationsForExecution
 * to cover command-level behavior that was previously untested.
 */

import { describe, it, expect, beforeEach, afterEach } from "vitest";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

import {
  cleanupEmptyDirs,
  sortMigrationsForExecution,
} from "../../src/commands/update.js";

// =============================================================================
// cleanupEmptyDirs
// =============================================================================

describe("cleanupEmptyDirs", () => {
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "trellis-cleanup-"));
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it("removes empty subdirectory under managed path", () => {
    // Create .claude/commands/ (empty)
    fs.mkdirSync(path.join(tmpDir, ".claude", "commands"), { recursive: true });
    cleanupEmptyDirs(tmpDir, ".claude/commands");
    expect(fs.existsSync(path.join(tmpDir, ".claude", "commands"))).toBe(false);
  });

  it("does not remove non-empty directory", () => {
    fs.mkdirSync(path.join(tmpDir, ".claude", "commands"), { recursive: true });
    fs.writeFileSync(
      path.join(tmpDir, ".claude", "commands", "file.md"),
      "content",
    );
    cleanupEmptyDirs(tmpDir, ".claude/commands");
    expect(fs.existsSync(path.join(tmpDir, ".claude", "commands"))).toBe(true);
  });

  it("does not remove directories outside managed paths", () => {
    fs.mkdirSync(path.join(tmpDir, "src", "utils"), { recursive: true });
    cleanupEmptyDirs(tmpDir, "src/utils");
    // Should still exist because src/utils is not a managed path
    expect(fs.existsSync(path.join(tmpDir, "src", "utils"))).toBe(true);
  });

  it("[CR#1] does not delete managed root directories even if empty", () => {
    // This is the bug that CR#1 identified: .claude itself should never be deleted
    fs.mkdirSync(path.join(tmpDir, ".claude"), { recursive: true });
    cleanupEmptyDirs(tmpDir, ".claude");
    expect(fs.existsSync(path.join(tmpDir, ".claude"))).toBe(true);
  });

  it("[CR#1] does not delete .aim-studio root even if empty", () => {
    fs.mkdirSync(path.join(tmpDir, ".aim-studio"), { recursive: true });
    cleanupEmptyDirs(tmpDir, ".aim-studio");
    expect(fs.existsSync(path.join(tmpDir, ".aim-studio"))).toBe(true);
  });

  it("[CR#1] does not delete .iflow root even if empty", () => {
    fs.mkdirSync(path.join(tmpDir, ".iflow"), { recursive: true });
    cleanupEmptyDirs(tmpDir, ".iflow");
    expect(fs.existsSync(path.join(tmpDir, ".iflow"))).toBe(true);
  });

  it("recursively cleans parent directories but stops at root", () => {
    // Create .aim-studio/scripts/multi_agent/ (all empty)
    fs.mkdirSync(path.join(tmpDir, ".aim-studio", "scripts", "multi_agent"), {
      recursive: true,
    });
    cleanupEmptyDirs(tmpDir, ".aim-studio/scripts/multi_agent");

    // multi_agent and scripts should be removed (both empty)
    expect(
      fs.existsSync(
        path.join(tmpDir, ".aim-studio", "scripts", "multi_agent"),
      ),
    ).toBe(false);
    expect(
      fs.existsSync(path.join(tmpDir, ".aim-studio", "scripts")),
    ).toBe(false);
    // .aim-studio root must survive
    expect(fs.existsSync(path.join(tmpDir, ".aim-studio"))).toBe(true);
  });

  it("handles non-existent directory gracefully", () => {
    // Should not throw
    expect(() => cleanupEmptyDirs(tmpDir, ".claude/nonexistent")).not.toThrow();
  });
});

// =============================================================================
// sortMigrationsForExecution
// =============================================================================

describe("sortMigrationsForExecution", () => {
  it("returns empty array for empty input", () => {
    expect(sortMigrationsForExecution([])).toEqual([]);
  });

  it("puts rename-dir before rename and delete", () => {
    const items = [
      { type: "rename" as const, from: ".claude/a.md", to: ".claude/b.md" },
      { type: "rename-dir" as const, from: ".aim-studio/old", to: ".aim-studio/new" },
      { type: "delete" as const, from: ".claude/c.md" },
    ];
    const sorted = sortMigrationsForExecution(items);
    expect(sorted[0].type).toBe("rename-dir");
  });

  it("sorts rename-dir by path depth (deeper first)", () => {
    const items = [
      { type: "rename-dir" as const, from: ".aim-studio/a", to: ".aim-studio/x" },
      {
        type: "rename-dir" as const,
        from: ".aim-studio/a/b/c",
        to: ".aim-studio/x/y/z",
      },
      { type: "rename-dir" as const, from: ".aim-studio/a/b", to: ".aim-studio/x/y" },
    ];
    const sorted = sortMigrationsForExecution(items);
    expect(sorted[0].from).toBe(".aim-studio/a/b/c"); // depth 4
    expect(sorted[1].from).toBe(".aim-studio/a/b"); // depth 3
    expect(sorted[2].from).toBe(".aim-studio/a"); // depth 2
  });

  it("preserves relative order of rename and delete items", () => {
    const items = [
      { type: "rename" as const, from: ".claude/a.md", to: ".claude/b.md" },
      { type: "delete" as const, from: ".claude/c.md" },
      { type: "rename" as const, from: ".claude/d.md", to: ".claude/e.md" },
    ];
    const sorted = sortMigrationsForExecution(items);
    // No rename-dir items, so original order is preserved
    expect(sorted[0].from).toBe(".claude/a.md");
    expect(sorted[1].from).toBe(".claude/c.md");
    expect(sorted[2].from).toBe(".claude/d.md");
  });

  it("does not mutate original array", () => {
    const items = [
      { type: "rename" as const, from: "a", to: "b" },
      { type: "rename-dir" as const, from: "c", to: "d" },
    ];
    const original = [...items];
    sortMigrationsForExecution(items);
    expect(items).toEqual(original);
  });
});
