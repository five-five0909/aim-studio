/**
 * AIM Studio Context Manager
 *
 * Unified context management for OpenCode plugins.
 */

import { existsSync, readFileSync, appendFileSync, readdirSync } from "fs"
import { join } from "path"
import { homedir, platform } from "os"
import { execSync } from "child_process"

// Python command: Windows uses 'python', macOS/Linux use 'python3'
const PYTHON_CMD = platform() === "win32" ? "python" : "python3"

// Debug log path
const DEBUG_LOG = platform() === "win32" 
  ? join(homedir(), "AppData", "Local", "Temp", "aim-plugin-debug.log")
  : "/tmp/aim-plugin-debug.log"

function debugLog(prefix, ...args) {
  const timestamp = new Date().toISOString()
  const msg = `[${timestamp}] [${prefix}] ${args.map(a => typeof a === "object" ? JSON.stringify(a) : a).join(" ")}\n`
  try {
    appendFileSync(DEBUG_LOG, msg)
  } catch {
    // ignore
  }
}

/**
 * AIM Studio Context Manager
 */
export class AimContext {
  constructor(directory) {
    this.directory = directory
    debugLog("context", "AimContext initialized", { directory })
  }

  /**
   * Check if this is an AIM Studio managed project
   */
  isAimProject() {
    return existsSync(join(this.directory, ".aim-studio"))
  }

  /**
   * Read a file, return null on error
   */
  readFile(filePath) {
    try {
      if (existsSync(filePath)) {
        return readFileSync(filePath, "utf-8")
      }
    } catch {
      // Ignore read errors
    }
    return null
  }

  /**
   * Read a file relative to project directory
   */
  readProjectFile(relativePath) {
    return this.readFile(join(this.directory, relativePath))
  }

  /**
   * Run a Python script and return output
   */
  runScript(scriptPath, cwd = null) {
    try {
      const result = execSync(`${PYTHON_CMD} "${scriptPath}"`, {
        cwd: cwd || this.directory,
        timeout: 10000,
        encoding: "utf-8",
        stdio: ["pipe", "pipe", "pipe"]
      })
      return result || ""
    } catch {
      return ""
    }
  }

  /**
   * Read all .md files in a directory
   */
  readDirectoryMdFiles(dirPath, maxFiles = 20) {
    const results = []
    const fullPath = join(this.directory, dirPath)

    if (!existsSync(fullPath)) {
      return results
    }

    try {
      const files = readdirSync(fullPath)
        .filter(f => f.endsWith(".md"))
        .sort()
        .slice(0, maxFiles)

      for (const filename of files) {
        const filePath = join(dirPath, filename)
        const content = this.readProjectFile(filePath)
        if (content) {
          results.push({ path: filePath, content })
        }
      }
    } catch {
      // Ignore directory read errors
    }

    return results
  }
}

// Context Collector for cross-hook communication
class ContextCollector {
  constructor() {
    this.pending = new Map()
    this.processed = new Set()
  }

  store(sessionID, content) {
    this.pending.set(sessionID, { content, timestamp: Date.now() })
    debugLog("collector", "stored context for session:", sessionID)
  }

  hasPending(sessionID) {
    return this.pending.has(sessionID)
  }

  consume(sessionID) {
    const pending = this.pending.get(sessionID)
    this.pending.delete(sessionID)
    return pending
  }

  markProcessed(sessionID) {
    this.processed.add(sessionID)
  }

  isProcessed(sessionID) {
    return this.processed.has(sessionID)
  }
}

export const contextCollector = new ContextCollector()
export { debugLog }
