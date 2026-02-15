"""
CLI Adapter for Claude Code.

Simplified adapter for Claude Code only. All other platforms have been removed.

Usage:
    from common.cli_adapter import CLIAdapter

    adapter = CLIAdapter()
    cmd = adapter.build_run_command(
        agent="dispatch",
        session_id="abc123",
        prompt="Start the pipeline"
    )
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

Platform = Literal["claude"]


@dataclass
class CLIAdapter:
    """Adapter for Claude Code CLI tool."""

    platform: Platform = "claude"

    # =========================================================================
    # Agent Name Mapping
    # =========================================================================

    def get_agent_name(self, agent: str) -> str:
        """Get agent name (no mapping needed for Claude Code).

        Args:
            agent: Original agent name (e.g., 'plan', 'dispatch')

        Returns:
            Agent name (unchanged for Claude Code)
        """
        return agent

    # =========================================================================
    # Agent Path
    # =========================================================================

    @property
    def config_dir_name(self) -> str:
        """Get config directory name.

        Returns:
            Directory name '.claude'
        """
        return ".claude"

    def get_config_dir(self, project_root: Path) -> Path:
        """Get config directory path.

        Args:
            project_root: Project root directory

        Returns:
            Path to .claude config directory
        """
        return project_root / self.config_dir_name

    def get_agent_path(self, agent: str, project_root: Path) -> Path:
        """Get path to agent definition file.

        Args:
            agent: Agent name
            project_root: Project root directory

        Returns:
            Path to agent .md file
        """
        return self.get_config_dir(project_root) / "agents" / f"{agent}.md"

    def get_commands_path(self, project_root: Path, *parts: str) -> Path:
        """Get path to commands directory or specific command file.

        Args:
            project_root: Project root directory
            *parts: Additional path parts (e.g., 'aim', 'finish-work.md')

        Returns:
            Path to commands directory or file
        """
        if not parts:
            return self.get_config_dir(project_root) / "commands"

        return self.get_config_dir(project_root) / "commands" / Path(*parts)

    def get_aim_command_path(self, name: str) -> str:
        """Get relative path to an aim command file.

        Args:
            name: Command name without extension (e.g., 'finish-work', 'check-backend')

        Returns:
            Relative path string for use in JSONL entries
        """
        return f"{self.config_dir_name}/commands/aim/{name}.md"

    # =========================================================================
    # Environment Variables
    # =========================================================================

    def get_non_interactive_env(self) -> dict[str, str]:
        """Get environment variables for non-interactive mode.

        Returns:
            Dict of environment variables to set
        """
        return {"CLAUDE_NON_INTERACTIVE": "1"}

    # =========================================================================
    # CLI Command Building
    # =========================================================================

    def build_run_command(
        self,
        agent: str,
        prompt: str,
        session_id: str | None = None,
        skip_permissions: bool = True,
        verbose: bool = True,
        json_output: bool = True,
    ) -> list[str]:
        """Build CLI command for running an agent.

        Args:
            agent: Agent name
            prompt: Prompt to send to the agent
            session_id: Optional session ID
            skip_permissions: Whether to skip permission prompts
            verbose: Whether to enable verbose output
            json_output: Whether to use JSON output format

        Returns:
            List of command arguments
        """
        cmd = ["claude", "-p"]
        cmd.extend(["--agent", agent])

        if session_id:
            cmd.extend(["--session-id", session_id])

        if skip_permissions:
            cmd.append("--dangerously-skip-permissions")

        if json_output:
            cmd.extend(["--output-format", "stream-json"])

        if verbose:
            cmd.append("--verbose")

        cmd.append(prompt)

        return cmd

    def build_resume_command(self, session_id: str) -> list[str]:
        """Build CLI command for resuming a session.

        Args:
            session_id: Session ID to resume

        Returns:
            List of command arguments
        """
        return ["claude", "--resume", session_id]

    def get_resume_command_str(self, session_id: str, cwd: str | None = None) -> str:
        """Get human-readable resume command string.

        Args:
            session_id: Session ID to resume
            cwd: Optional working directory to cd into

        Returns:
            Command string for display
        """
        cmd = self.build_resume_command(session_id)
        cmd_str = " ".join(cmd)

        if cwd:
            return f"cd {cwd} && {cmd_str}"
        return cmd_str

    # =========================================================================
    # Platform Detection Helpers
    # =========================================================================

    @property
    def is_claude(self) -> bool:
        """Check if platform is Claude Code (always True)."""
        return True

    @property
    def cli_name(self) -> str:
        """Get CLI executable name."""
        return "claude"

    @property
    def supports_cli_agents(self) -> bool:
        """Check if platform supports running agents via CLI (always True)."""
        return True

    # =========================================================================
    # Session ID Handling
    # =========================================================================

    @property
    def supports_session_id_on_create(self) -> bool:
        """Check if platform supports specifying session ID on creation (always True)."""
        return True


# =============================================================================
# Factory Function
# =============================================================================


def get_cli_adapter(platform: str = "claude") -> CLIAdapter:
    """Get CLI adapter for Claude Code.

    Args:
        platform: Platform name (only 'claude' is supported)

    Returns:
        CLIAdapter instance

    Raises:
        ValueError: If platform is not 'claude'
    """
    if platform != "claude":
        raise ValueError(f"Unsupported platform: {platform} (only 'claude' is supported)")

    return CLIAdapter()


def detect_platform(project_root: Path) -> Platform:
    """Detect platform (always returns 'claude').

    Args:
        project_root: Project root directory

    Returns:
        'claude'
    """
    return "claude"


def get_cli_adapter_auto(project_root: Path) -> CLIAdapter:
    """Get CLI adapter (always returns Claude Code adapter).

    Args:
        project_root: Project root directory

    Returns:
        CLIAdapter instance for Claude Code
    """
    return CLIAdapter()
