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
    python export.py --duration 10               # Set video duration (5/10/15/30/45/60 seconds)
    python export.py --check                     # Check for violations before export
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from common.paths import get_project_root, get_tasks_dir


# =============================================================================
# Duration Options
# =============================================================================

DURATION_OPTIONS = ["5", "10", "15", "30", "45", "60"]

# =============================================================================
# Violation Detection
# =============================================================================

# Keywords that may indicate real person references (celebrities, public figures)
REAL_PERSON_KEYWORDS = [
    # Chinese celebrities
    "明星", "演员", "歌手", "主持人", "网红", "名人", "偶像",
    "刘德华", "周杰伦", "成龙", "李连杰", "甄子丹", "吴京",
    "赵丽颖", "杨幂", "范冰冰", "李冰冰", "Angelababy", "迪丽热巴",
    "肖战", "王一博", "蔡徐坤", "李易峰", "吴亦凡", "鹿晗",
    "特朗普", "拜登", "奥巴马", "普京", "马斯克", "乔布斯",
    # International celebrities
    "Leonardo DiCaprio", "Brad Pitt", "Tom Cruise", "Jennifer Lawrence",
    "Taylor Swift", "Beyonce", "K-pop", "BTS", "Blackpink",
    "周杰伦", "王菲", "张学友", "刘德华", "郭富城", "黎明",
    # General real person terms
    "真人", "照片", "写真", "肖像", "脸", "颜值",
    "真实照片", "本人", "本人照片", "自拍照",
]

# Keywords that may indicate copyright issues
COPYRIGHT_KEYWORDS = [
    # Copyright protected terms
    "版权", "侵权", "盗版", "抄袭", "原创",
    "小说改编", "影视改编", "动漫改编", "游戏改编",
    "IP", "知识产权", "授权", "许可",
    "哈利波特", "漫威", "DC", "迪士尼", "皮克斯",
    " Batman", "Spider-Man", "Superman", "Iron Man",
    "金庸", "古龙", "琼瑶", "JK罗琳", "马丁",
    "腾讯", "网易", "字节", "B站",
]

# Keywords that may indicate sensitive content
SENSITIVE_KEYWORDS = [
    "暴力", "血腥", "色情", "裸露", "赌博", "毒品",
    "政治", "宗教", "邪教", "恐怖", "自杀", "自残",
    "未成年人", "儿童", "小孩", "幼儿",
]


def detect_violations(content: str) -> dict:
    """
    Detect potential violations in content.

    Returns:
        dict with 'has_violation', 'real_person', 'copyright', 'sensitive' flags
    """
    result = {
        "has_violation": False,
        "real_person": [],
        "copyright": [],
        "sensitive": [],
    }

    # Check for real person references
    for keyword in REAL_PERSON_KEYWORDS:
        if keyword.lower() in content.lower():
            result["real_person"].append(keyword)
            result["has_violation"] = True

    # Check for copyright issues
    for keyword in COPYRIGHT_KEYWORDS:
        if keyword in content:
            result["copyright"].append(keyword)
            result["has_violation"] = True

    # Check for sensitive content
    for keyword in SENSITIVE_KEYWORDS:
        if keyword in content:
            result["sensitive"].append(keyword)
            result["has_violation"] = True

    return result


def check_violations_in_project(project_root: Path) -> dict:
    """Check all project files for potential violations."""
    spec_dir = project_root / ".aim-studio" / "spec"

    all_violations = {
        "characters": [],
        "world": [],
        "scenes": [],
        "has_violation": False,
    }

    # Check character file
    char_file = spec_dir / "story" / "character.md"
    if char_file.exists():
        content = read_file(char_file)
        violations = detect_violations(content)
        if violations["has_violation"]:
            all_violations["characters"] = violations
            all_violations["has_violation"] = True

    # Check world file
    world_file = spec_dir / "story" / "world.md"
    if world_file.exists():
        content = read_file(world_file)
        violations = detect_violations(content)
        if violations["has_violation"]:
            all_violations["world"] = violations
            all_violations["has_violation"] = True

    # Check scenes
    tasks_dir = get_tasks_dir(project_root)
    if tasks_dir.exists():
        for ep_dir in tasks_dir.iterdir():
            if ep_dir.is_dir() and "EP" in ep_dir.name.upper():
                for scene_file in ep_dir.glob("*.md"):
                    content = read_file(scene_file)
                    violations = detect_violations(content)
                    if violations["has_violation"]:
                        all_violations["scenes"].append({
                            "file": str(scene_file.relative_to(project_root)),
                            "violations": violations,
                        })
                        all_violations["has_violation"] = True

    return all_violations


def print_violation_report(violations: dict) -> None:
    """Print a detailed violation report."""
    print("\n" + "=" * 60)
    print("🚨 违规检测报告")
    print("=" * 60)

    if not violations["has_violation"]:
        print("\n✅ 未检测到违规内容，可以继续导出！")
        return

    print("\n⚠️  检测到以下潜在违规内容：\n")

    # Real person violations
    if violations.get("characters") and violations["characters"].get("real_person"):
        print("【真人素材风险】")
        for keyword in violations["characters"]["real_person"]:
            print(f"  - 关键词: {keyword}")
        print()

    if violations.get("world") and violations["world"].get("real_person"):
        print("【世界观真人素材风险】")
        for keyword in violations["world"]["real_person"]:
            print(f"  - 关键词: {keyword}")
        print()

    # Copyright violations
    if violations.get("characters") and violations["characters"].get("copyright"):
        print("【版权风险】")
        for keyword in violations["characters"]["copyright"]:
            print(f"  - 关键词: {keyword}")
        print()

    if violations.get("world") and violations["world"].get("copyright"):
        print("【世界观版权风险】")
        for keyword in violations["world"]["copyright"]:
            print(f"  - 关键词: {keyword}")
        print()

    # Sensitive content
    if violations.get("characters") and violations["characters"].get("sensitive"):
        print("【敏感内容风险】")
        for keyword in violations["characters"]["sensitive"]:
            print(f"  - 关键词: {keyword}")
        print()

    # Scene violations
    if violations.get("scenes"):
        print("【场景违规详情】")
        for scene in violations["scenes"][:5]:  # Show first 5
            print(f"  - {scene['file']}")
            if scene["violations"].get("real_person"):
                print(f"    真人: {', '.join(scene['violations']['real_person'][:3])}")
            if scene["violations"].get("copyright"):
                print(f"    版权: {', '.join(scene['violations']['copyright'][:3])}")
        if len(violations["scenes"]) > 5:
            print(f"  ... 还有 {len(violations['scenes']) - 5} 个场景")
        print()

    print("=" * 60)
    print("💡 建议处理方式：")
    print("  1. 修改角色设定 - 使用虚构角色替代真人")
    print("  2. 替换版权内容 - 使用原创元素替代受版权保护的内容")
    print("  3. 简化敏感描述 - 移除可能引发争议的描述")
    print("  4. 强制导出 - 仍要导出（风险自负）")
    print("=" * 60)


def get_user_choice() -> str:
    """Get user's choice for handling violations."""
    print("\n请选择处理方式（输入数字）：")
    print("  1. 修改角色设定 - 手动修改角色文件")
    print("  2. 替换版权内容 - 手动修改版权相关内容")
    print("  3. 简化敏感描述 - 移除敏感描述后重试")
    print("  4. 强制导出 - 仍要导出（风险自负）")
    print("  5. 退出 - 不导出")

    while True:
        choice = input("\n请输入选项 (1-5): ").strip()
        if choice in ["1", "2", "3", "4", "5"]:
            return choice
        print("无效选择，请重新输入。")


# =============================================================================
# File Operations
# =============================================================================

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
    duration: str = "10",
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

    # Duration
    output.append(f"[DURATION: {duration}s]")
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


def generate_simple_prompt(scene_content: str, scene_name: str, duration: str = "10") -> str:
    """
    Generate a simple, minimal prompt for quick copy.
    Just the essential scene description.
    """

    lines = scene_content.split("\n")
    output = []

    output.append(f"Scene: {scene_name}")
    output.append(f"Duration: {duration}s")
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
    duration: str = "10",
    skip_violations: bool = False,
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

        # Check violations if not skipped
        if not skip_violations:
            violations = detect_violations(content)
            if violations["has_violation"]:
                print(f"  ⚠️  场景 {scene_name} 包含潜在违规内容")

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
            prompt = generate_simple_prompt(content, scene_name, duration)
        else:
            prompt = generate_seedance_prompt(
                content,
                character_prompts,
                world_prompt,
                scene_name,
                duration=duration,
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
        "--duration",
        type=str,
        default="10",
        choices=DURATION_OPTIONS,
        help="Video duration in seconds (5/10/15/30/45/60)",
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
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check for violations, do not export",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force export even with violations",
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

    # Check violations first
    print("🔍 正在检查违规内容...")
    violations = check_violations_in_project(project_root)
    print_violation_report(violations)

    # If --check only, exit here
    if args.check:
        sys.exit(0 if not violations["has_violation"] else 1)

    # Handle violations
    if violations["has_violation"] and not args.force:
        choice = get_user_choice()

        if choice == "1":
            print("\n请手动修改角色设定文件后重试：")
            print(f"  {spec_dir / 'story' / 'character.md'}")
            sys.exit(1)
        elif choice == "2":
            print("\n请手动修改版权相关内容后重试。")
            sys.exit(1)
        elif choice == "3":
            print("\n请移除敏感描述后重试。")
            sys.exit(1)
        elif choice == "4":
            print("\n⚠️  强制导出已启用，风险自负！")
        elif choice == "5":
            print("\n已退出导出。")
            sys.exit(0)

    # Create output directory
    output_dir = project_root / args.output
    output_dir.mkdir(exist_ok=True)

    print(f"\n导出设置：")
    print(f"  - 格式: {args.format}")
    print(f"  - 时长: {args.duration}秒")
    print(f"  - 输出: {output_dir}")
    print("")

    exported_files = []

    # Determine which episodes to export
    if args.ep == "all":
        episodes = find_episodes(tasks_dir)
        for ep_name, ep_dir in episodes:
            print(f"导出 {ep_name}...")
            files = export_episode(
                ep_name, ep_dir, spec_dir, output_dir,
                args.format, args.duration, args.force
            )
            exported_files.extend(files)
    elif "-" in str(args.ep):
        # Range like 1-3
        start, end = map(int, args.ep.split("-"))
        for ep_num in range(start, end + 1):
            ep_name = f"EP{ep_num:02d}"
            ep_dir = tasks_dir / ep_name
            if ep_dir.exists():
                print(f"导出 {ep_name}...")
                files = export_episode(
                    ep_name, ep_dir, spec_dir, output_dir,
                    args.format, args.duration, args.force
                )
                exported_files.extend(files)
    elif args.ep:
        # Single episode
        ep_num = int(args.ep)
        ep_name = f"EP{ep_num:02d}"
        ep_dir = tasks_dir / ep_name

        if ep_dir.exists():
            print(f"导出 {ep_name}...")
            exported_files = export_episode(
                ep_name, ep_dir, spec_dir, output_dir,
                args.format, args.duration, args.force
            )
        else:
            print(f"Error: Episode {ep_name} not found in {tasks_dir}")
            sys.exit(1)
    else:
        print("Error: 请指定 --ep 或 --all")
        parser.print_help()
        sys.exit(1)

    print("")
    print(f"✅ 已导出 {len(exported_files)} 个文件:")
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
    print("完成！文件已准备好用于 Seedance。")


if __name__ == "__main__":
    main()
