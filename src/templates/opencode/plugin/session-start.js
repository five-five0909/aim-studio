/* global process */
/**
 * AIM Studio Session Start Plugin
 *
 * Injects context when user sends the first message in a session.
 */

import { existsSync } from "fs"
import { join } from "path"
import { AimContext, contextCollector, debugLog } from "../lib/aim-context.js"

/**
 * Build session context for injection
 */
function buildSessionContext(ctx) {
  const directory = ctx.directory
  const aimDir = join(directory, ".aim-studio")
  const opencodeDir = join(directory, ".opencode")

  const parts = []

  // 1. Header
  parts.push(`<aim-context>
你正在一个 AIM Studio 管理的项目中开始新的会话。
请仔细阅读并遵循以下所有指令。
</aim-context>`)

  // 2. Current Context (dynamic)
  const contextScript = join(aimDir, "scripts", "get_context.py")
  if (existsSync(contextScript)) {
    const output = ctx.runScript(contextScript)
    if (output) {
      parts.push("<current-state>")
      parts.push(output)
      parts.push("</current-state>")
    }
  }

  // 3. Workflow Guide
  const workflow = ctx.readProjectFile(".aim-studio/workflow.md")
  if (workflow) {
    parts.push("<workflow>")
    parts.push(workflow)
    parts.push("</workflow>")
  }

  // 4. Guidelines Index
  parts.push("<guidelines>")

  parts.push("## 创作规范")
  const storySpecDir = join(aimDir, "spec", "story")
  if (existsSync(storySpecDir)) {
    const storySpecs = ctx.readDirectoryMdFiles(".aim-studio/spec/story")
    for (const spec of storySpecs) {
      parts.push(`- ${spec.path}`)
    }
  } else {
    parts.push("未配置")
  }

  parts.push("</guidelines>")

  // 5. Session Instructions
  const startMd = ctx.readFile(join(opencodeDir, "commands", "aim", "start.md"))
  if (startMd) {
    parts.push("<instructions>")
    parts.push(startMd)
    parts.push("</instructions>")
  }

  // 6. Final directive
  parts.push(`<ready>
上下文已加载。等待用户的第一条消息，然后遵循 <instructions> 处理他们的请求。
</ready>`)

  return parts.join("\n\n")
}

export default async ({ directory }) => {
  const ctx = new AimContext(directory)
  debugLog("session", "Plugin loaded, directory:", directory)

  return {
    // chat.message - triggered when user sends a message
    "chat.message": async (input, output) => {
      try {
        const sessionID = input.sessionID
        debugLog("session", "chat.message called, sessionID:", sessionID)

        // Skip in non-interactive mode
        if (process.env.OPENCODE_NON_INTERACTIVE === "1") {
          return
        }

        // Skip if not an AIM project
        if (!ctx.isAimProject()) {
          return
        }

        // Only inject on first message
        if (contextCollector.isProcessed(sessionID)) {
          return
        }

        // Mark session as processed
        contextCollector.markProcessed(sessionID)

        // Build and store context
        const context = buildSessionContext(ctx)
        contextCollector.store(sessionID, context)
        debugLog("session", "Context stored for session:", sessionID)

      } catch (error) {
        debugLog("session", "Error in chat.message:", error.message)
      }
    },

    // experimental.chat.messages.transform - modify messages before sending to AI
    "experimental.chat.messages.transform": async (input, output) => {
      try {
        const { messages } = output

        if (!messages || messages.length === 0) {
          return
        }

        // Find last user message
        let lastUserMessageIndex = -1
        for (let i = messages.length - 1; i >= 0; i--) {
          if (messages[i].info?.role === "user") {
            lastUserMessageIndex = i
            break
          }
        }

        if (lastUserMessageIndex === -1) {
          return
        }

        const lastUserMessage = messages[lastUserMessageIndex]
        const sessionID = lastUserMessage.info?.sessionID

        if (!sessionID || !contextCollector.hasPending(sessionID)) {
          return
        }

        // Get and consume pending context
        const pending = contextCollector.consume(sessionID)

        // Find first text part
        const textPartIndex = lastUserMessage.parts?.findIndex(
          p => p.type === "text" && p.text !== undefined
        )

        if (textPartIndex === -1) {
          return
        }

        // Prepend context to the text part
        const originalText = lastUserMessage.parts[textPartIndex].text || ""
        lastUserMessage.parts[textPartIndex].text = `${pending.content}\n\n---\n\n${originalText}`

        debugLog("session", "Injected context, length:", pending.content.length)

      } catch (error) {
        debugLog("session", "Error in messages.transform:", error.message)
      }
    }
  }
}
