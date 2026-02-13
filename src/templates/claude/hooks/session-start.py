#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session Start Hook - Inject structured context
"""

# IMPORTANT: Suppress all warnings FIRST
import warnings
warnings.filterwarnings("ignore")

import json
import os
import subprocess
import sys
from io import StringIO
from pathlib import Path

# IMPORTANT: Force stdout to use UTF-8 on Windows
# This fixes UnicodeEncodeError when outputting non-ASCII characters
if sys.platform == "win32":
    import io as _io
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    elif hasattr(sys.stdout, "detach"):
        sys.stdout = _io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8", errors="replace")  # type: ignore[union-attr]


def should_skip_injection() -> bool:
    return (
        os.environ.get("CLAUDE_NON_INTERACTIVE") == "1"
        or os.environ.get("OPENCODE_NON_INTERACTIVE") == "1"
    )


def read_file(path: Path, fallback: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        return fallback


def run_script(script_path: Path) -> str:
    try:
        if script_path.suffix == ".py":
            # Add PYTHONIOENCODING to force UTF-8 in subprocess
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            cmd = [sys.executable, "-W", "ignore", str(script_path)]
        else:
            env = os.environ
            cmd = [str(script_path)]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            cwd=script_path.parent.parent.parent,
            env=env,
        )
        return result.stdout if result.returncode == 0 else "No context available"
    except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
        return "No context available"


def detect_project_type(project_dir: Path) -> str:
    """Detect project type based on directory structure."""

    # Check for bin/ directory (CLI tool)
    if (project_dir / "bin").is_dir():
        return "cli"

    # Check for story project (has spec/story/)
    if (project_dir / ".aim-studio" / "spec" / "story").is_dir():
        return "story"

    # Check for frontend indicators
    frontend_indicators = [
        "package.json",
        "vite.config.ts",
        "vite.config.js",
        "next.config.js",
        "next.config.ts",
        "nuxt.config.ts",
    ]
    has_frontend = any((project_dir / f).exists() for f in frontend_indicators)

    # Check for backend indicators
    backend_indicators = [
        "requirements.txt",
        "pyproject.toml",
        "go.mod",
        "Cargo.toml",
        "pom.xml",
        "composer.json",
    ]
    has_backend = any((project_dir / f).exists() for f in backend_indicators)

    if has_frontend and has_backend:
        return "fullstack"
    elif has_frontend:
        return "frontend"
    elif has_backend:
        return "backend"

    return "unknown"


def main():
    if should_skip_injection():
        sys.exit(0)

    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
    trellis_dir = project_dir / ".aim-studio"
    claude_dir = project_dir / ".claude"

    # Detect project type
    project_type = detect_project_type(project_dir)

    output = StringIO()

    # 根据项目类型显示不同的欢迎信息
    welcome_messages = {
        "cli": "AIM Studio CLI 项目",
        "frontend": "AIM Studio 前端项目",
        "backend": "AIM Studio 后端项目",
        "fullstack": "AIM Studio 全栈项目",
        "story": "AIM Studio 漫剧创作项目",
        "unknown": "AIM Studio 项目",
    }

    output.write(f"""<session-context>
您正在启动一个 {welcome_messages.get(project_type, 'AIM Studio')} 会话。
请仔细阅读以下说明并遵循执行。

项目类型: {project_type}

""")

    # Get current context
    output.write("<current-state>\n")
    context_script = trellis_dir / "scripts" / "get_context.py"
    output.write(run_script(context_script))
    output.write("\n</current-state>\n\n")

    # Workflow
    output.write("<workflow>\n")
    workflow_content = read_file(trellis_dir / "workflow.md", "未找到 workflow.md")
    output.write(workflow_content)
    output.write("\n</workflow>\n\n")

    # Guidelines - 根据项目类型注入相应的规范
    output.write("<guidelines>\n")

    # CLI 项目
    if project_type == "cli":
        output.write("## CLI 开发规范\n")
        cli_index = read_file(
            trellis_dir / "spec" / "cli" / "index.md", "未配置 CLI 规范"
        )
        output.write(cli_index)
        output.write("\n\n")

    # Frontend 项目
    if project_type in ("frontend", "fullstack"):
        output.write("## 前端开发规范\n")
        frontend_index = read_file(
            trellis_dir / "spec" / "frontend" / "index.md", "未配置前端规范"
        )
        output.write(frontend_index)
        output.write("\n\n")

    # Backend 项目
    if project_type in ("backend", "fullstack", "cli"):
        output.write("## 后端开发规范\n")
        backend_index = read_file(
            trellis_dir / "spec" / "backend" / "index.md", "未配置后端规范"
        )
        output.write(backend_index)
        output.write("\n\n")

    # Story 项目
    if project_type == "story":
        output.write("## 漫剧创作规范\n")
        story_index = read_file(
            trellis_dir / "spec" / "story" / "index.md", "未配置漫剧规范"
        )
        output.write(story_index)
        output.write("\n\n")

    # Guides - 始终提供
    output.write("## 开发指南\n")
    guides_index = read_file(
        trellis_dir / "spec" / "guides" / "index.md", "未配置开发指南"
    )
    output.write(guides_index)

    output.write("\n</guidelines>\n\n")

    # 读取命令文件 - 必须使用 commands/aim/ 目录（新结构）
    def read_command_file(filename: str) -> str:
        """读取 commands/aim/ 目录下的命令文件"""
        aim_path = claude_dir / "commands" / "aim" / filename
        if aim_path.exists():
            return read_file(aim_path, "")
        return f"未找到命令文件: {filename}"

    # 根据项目类型选择不同的 start 指令
    if project_type == "story":
        start_md = read_command_file("story.md")
    else:
        start_md = read_command_file("start.md")

    output.write("<instructions>\n")
    output.write(start_md)
    output.write("\n</instructions>\n\n")

    # 项目类型特定的提示
    type_hints = {
        "cli": "注意：这是一个 CLI 工具项目，请参考 spec/cli/ 目录下的规范。",
        "frontend": "注意：这是一个前端项目，请参考 spec/frontend/ 目录下的规范。",
        "backend": "注意：这是一个后端项目，请参考 spec/backend/ 目录下的规范。",
        "fullstack": "注意：这是一个全栈项目，请同时参考 spec/frontend/ 和 spec/backend/ 目录下的规范。",
        "story": "注意：这是一个漫剧创作项目，请使用 /aim:story 命令开始创作。漫剧命令不适用于其他类型的项目。",
        "unknown": "注意：项目类型未知，请根据实际情况选择合适的工作流程。",
    }

    output.write(f"""<project-type-hint>
{type_hints.get(project_type, '')}
</project-type-hint>

""")

    output.write("""<ready>
上下文已加载。请等待用户的第一个消息，然后按照 <instructions> 中的说明处理用户请求。
</ready>""")

    result = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": output.getvalue(),
        }
    }

    # Output JSON - stdout is already configured for UTF-8
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
