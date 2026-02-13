#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export script for generating Seedance-ready prompts

Usage:
    python export.py --ep 1                    # Export episode 1
    python export.py --ep 1-3                   # Export episodes 1-3
    python export.py --all                      # Export all episodes
    python export.py --scene 1                  # Export scene 1 of current episode
    python export.py --format seedance          # Seedance format (default)
    python export.py --format simple             # Simple format for quick copy
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from common.paths import get_project_root, get_tasks_dir


def read_file(file_path: Path) -> str:
    """Read file content."""
    try:
        return file_path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        return ""


def get_character_prompt(character_name: str, spec_dir: Path) -> str:
    """Generate character prompt for Seedance."""
    character_file = spec_dir / "story" / "character.md"
    if not character_file.exists():
        return ""

    content = read_file(character_file)

    # Extract character section
    lines = content.split("\n")
    in_character = False
    character_lines = []

    for line in lines:
        if f"## {character_name}" in line or f"## {character_name}：" in line:
            in_character = True
            continue
        if in_character:
            if line.startswith("## "):
                break
            character_lines.append(line)

    if character_lines:
        # Extract key information: appearance, personality, clothing
        prompt_parts = []

        # Extract appearance
        for line in character_lines:
            if "外观" in line or "外貌" in line or "Appearance" in line:
                prompt_parts.append(line.split(":", 1)[-1].strip())

            if "服装" in line or "Clothing" in line:
                prompt_parts.append(line.split(":", 1)[-1].strip())

        return ", ".join(prompt_parts) if prompt_parts else ""

    return ""


def get_world_prompt(spec_dir: Path) -> str:
    """Generate world prompt for Seedance."""
    world_file = spec_dir / "story" / "world.md"
    if not world_file.exists():
        return ""

    content = read_file(world_file)

    # Extract style keywords
    keywords = []

    # Look for style/tone keywords
    for line in content.split("\n"):
        if "风格" in line or "Style" in line or "视觉" in line or "Visual" in line:
            # Extract keywords after colon
            if ":" in line:
                keywords.append(line.split(":", 1)[-1].strip())

    return ", ".join(keywords)[:200] if keywords else "cinematic, high quality"


def parse_scene_file(scene_path: Path) -> dict:
    """Parse scene file and extract Seedance-relevant content."""
    content = read_file(scene_path)

    if not content:
        return {}

    scene_data = {
        "content": content,
        "has_seedance_format": False,
    }

    # Check for Seedance 2.0 format (六要素)
    required_elements = ["主体描述", "动作", "环境", "镜头", "音频", "风格"]
    if any(elem in content for elem in required_elements):
        scene_data["has_seedance_format"] = True

    return scene_data


def generate_seedance_prompt(
    scene_content: str,
    character_prompts: dict,
    world_prompt: str,
    scene_name: str,
    previous_context: str = "",
) -> str:
    """
    Generate a clean, copy-paste ready prompt for Seedance.

    Format: Pure text, no markdown, ready for video generation.
    """

    # Extract key information from scene content
    lines = scene_content.split("\n")

    output = []

    # Scene header
    output.append(f"=== {scene_name} ===")
    output.append("")

    # Character prompts
    if character_prompts:
        output.append("[CHARACTERS]")
        for name, prompt in character_prompts.items():
            if prompt:
                output.append(f"{name}: {prompt}")
        output.append("")

    # Environment
    output.append("[ENVIRONMENT]")
    # Extract environment description
    for line in lines:
        if "环境" in line or "场景" in line:
            env_text = line.split(":", 1)[-1].strip() if ":" in line else line
            if env_text:
                output.append(env_text)
                break
    output.append("")

    # Previous context
    if previous_context:
        output.append("[PREVIOUS CONTEXT]")
        output.append(previous_context[:200])
        output.append("")

    # Main content - extract the actual scene description
    output.append("[SCENE]")

    # Extract main scene content (skip headers and metadata)
    in_main_content = False
    for line in lines:
        # Skip metadata lines
        if any(marker in line for marker in ["#", "##", "---", "**", "日期", "时间", "时长"]):
            continue

        # Skip empty lines at start
        if not in_main_content and not line.strip():
            continue

        # Start main content
        if line.strip() and not in_main_content:
            in_main_content = True

        if in_main_content:
            # Clean the line - remove markdown
            cleaned_line = line.strip()
            cleaned_line = cleaned_line.replace("**", "").replace("*", "")
            cleaned_line = cleaned_line.replace("[", "").replace("]", "")

            if cleaned_line:
                output.append(cleaned_line)

    output.append("")

    # Style prompt
    if world_prompt:
        output.append("[STYLE]")
        output.append(world_prompt)

    # Return as pure text
    return "\n".join(output)


def generate_simple_prompt(scene_content: str, scene_name: str) -> str:
    """
    Generate a simple, minimal prompt for quick copy.
    Just the essential scene description.
    """

    lines = scene_content.split("\n")
    output = []

    output.append(f"Scene: {scene_name}")
    output.append("")

    # Extract just the dialogue and action
    for line in lines:
        # Skip headers and metadata
        if line.startswith("#") or line.startswith("##"):
            continue
        if "日期" in line or "时间" in line or "时长" in line:
            continue
        if "主体描述" in line or "动作" in line:
            continue

        # Clean and add
        cleaned = line.strip().replace("**", "").replace("*", "")
        if cleaned:
            output.append(cleaned)

    return "\n".join(output)


def find_episodes(tasks_dir: Path) -> list:
    """Find all episode directories."""
    episodes = []

    if not tasks_dir.exists():
        return episodes

    for item in tasks_dir.iterdir():
        if item.is_dir() and "EP" in item.name.upper():
            episodes.append((item.name, item))

    # Sort by episode number
    episodes.sort(key=lambda x: x[0])
    return episodes


def find_scenes(episode_dir: Path) -> list:
    """Find all scene files in an episode directory."""
    scenes = []

    if not episode_dir.exists():
        return scenes

    for item in episode_dir.iterdir():
        if item.is_file() and (item.suffix == ".md" or item.suffix == ".txt"):
            if "task.json" in item.name or "prd" in item.name:
                continue
            scenes.append(item)

    scenes.sort(key=lambda x: x.name)
    return scenes


def export_episode(
    episode_name: str,
    episode_dir: Path,
    spec_dir: Path,
    output_dir: Path,
    format_type: str = "seedance",
) -> list:
    """Export a single episode."""

    # Get character and world prompts
    world_prompt = get_world_prompt(spec_dir)

    # Find scenes
    scenes = find_scenes(episode_dir)

    output_files = []

    for scene_file in scenes:
        scene_name = scene_file.stem
        content = read_file(scene_file)

        # Get character prompts for this scene (simplified - use all characters)
        character_prompts = {}
        character_file = spec_dir / "story" / "character.md"
        if character_file.exists():
            char_content = read_file(character_file)
            # Extract character names from ## headers
            for line in char_content.split("\n"):
                if line.startswith("## ") and not line.startswith("###"):
                    char_name = line.replace("##", "").strip()
                    # Generate prompt for this character
                    char_prompt = get_character_prompt(char_name, spec_dir)
                    if char_prompt:
                        character_prompts[char_name] = char_prompt

        # Generate prompt based on format
        if format_type == "simple":
            prompt = generate_simple_prompt(content, scene_name)
        else:
            prompt = generate_seedance_prompt(
                content,
                character_prompts,
                world_prompt,
                scene_name,
            )

        # Write to output directory
        output_file = output_dir / f"{episode_name}_{scene_name}.txt"
        output_file.write_text(prompt, encoding="utf-8")
        output_files.append(output_file)

    return output_files


def main():
    parser = argparse.ArgumentParser(
        description="Export script for Seedance video generation"
    )
    parser.add_argument(
        "--ep",
        type=str,
        help="Episode number(s). Examples: 1, 1-3, all",
    )
    parser.add_argument(
        "--scene",
        type=int,
        help="Scene number within episode",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="seedance",
        choices=["seedance", "simple"],
        help="Export format: seedance (full) or simple (minimal)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="export",
        help="Output directory name",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open output directory after export",
    )

    args = parser.parse_args()

    # Get project paths
    project_root = get_project_root()
    tasks_dir = get_tasks_dir(project_root)
    spec_dir = project_root / ".aim-studio" / "spec"

    # Check if story project
    if not (spec_dir / "story").exists():
        print("Error: This is not a story project. No spec/story/ directory found.")
        sys.exit(1)

    # Create output directory
    output_dir = project_root / args.output
    output_dir.mkdir(exist_ok=True)

    print(f"Exporting to: {output_dir}")
    print(f"Format: {args.format}")
    print("")

    exported_files = []

    # Determine which episodes to export
    if args.ep == "all":
        episodes = find_episodes(tasks_dir)
        for ep_name, ep_dir in episodes:
            print(f"Exporting {ep_name}...")
            files = export_episode(ep_name, ep_dir, spec_dir, output_dir, args.format)
            exported_files.extend(files)
    elif "-" in str(args.ep):
        # Range like 1-3
        start, end = map(int, args.ep.split("-"))
        for ep_num in range(start, end + 1):
            ep_name = f"EP{ep_num:02d}"
            ep_dir = tasks_dir / ep_name
            if ep_dir.exists():
                print(f"Exporting {ep_name}...")
                files = export_episode(ep_name, ep_dir, spec_dir, output_dir, args.format)
                exported_files.extend(files)
    elif args.ep:
        # Single episode
        ep_num = int(args.ep)
        ep_name = f"EP{ep_num:02d}"
        ep_dir = tasks_dir / ep_name

        if ep_dir.exists():
            print(f"Exporting {ep_name}...")
            exported_files = export_episode(ep_name, ep_dir, spec_dir, output_dir, args.format)
        else:
            print(f"Error: Episode {ep_name} not found in {tasks_dir}")
            sys.exit(1)
    else:
        print("Error: Please specify --ep or --all")
        parser.print_help()
        sys.exit(1)

    print("")
    print(f"Exported {len(exported_files)} files:")
    for f in exported_files:
        print(f"  - {f.relative_to(project_root)}")

    # Optionally open output directory
    if args.open:
        import subprocess

        if sys.platform == "win32":
            os.startfile(output_dir)
        elif sys.platform == "darwin":
            subprocess.run(["open", str(output_dir)])
        else:
            subprocess.run(["xdg-open", str(output_dir)])

    print("")
    print("Done! Files are ready for Seedance.")


if __name__ == "__main__":
    main()
