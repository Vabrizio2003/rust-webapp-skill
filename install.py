#!/usr/bin/env python3
"""
Install rust-webapp skill for Claude Code.

Usage:
    curl -sSL https://raw.githubusercontent.com/arseny/rust-webapp-skill/main/install.py | python3
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_URL = "https://github.com/arsenyinfo/rust-webapp-skill.git"
SKILL_NAME = "rust-webapp"


def main():
    skills_dir = Path.home() / ".claude" / "skills"
    target_dir = skills_dir / SKILL_NAME

    print(f"Installing {SKILL_NAME} skill...")

    # create skills directory if needed
    skills_dir.mkdir(parents=True, exist_ok=True)

    # remove existing installation
    if target_dir.exists():
        print(f"Removing existing installation at {target_dir}")
        shutil.rmtree(target_dir)

    # clone to temp dir and copy contents
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp) / "repo"
        print(f"Cloning from {REPO_URL}...")
        subprocess.run(
            ["git", "clone", "--depth", "1", REPO_URL, str(tmp_path)],
            check=True,
            capture_output=True,
        )

        # copy skill files (exclude git and install script)
        print(f"Installing to {target_dir}...")
        shutil.copytree(
            tmp_path,
            target_dir,
            ignore=shutil.ignore_patterns(".git", "install.py", "LICENSE", ".gitignore"),
        )

    # make scripts executable
    scripts_dir = target_dir / "scripts"
    if scripts_dir.exists():
        for script in scripts_dir.iterdir():
            if script.is_file():
                script.chmod(script.stat().st_mode | 0o111)

    print(f"\nInstalled to: {target_dir}")
    print("\nPrerequisites (install once):")
    print("  npm i -g neonctl")
    print("  brew install jq")
    print("  cargo install sqlx-cli --features postgres,native-tls")
    print("\nSet environment variables:")
    print("  export NEON_API_KEY=your-key")
    print("  export NEON_PROJECT_ID=your-project-id")
    print("\nDone!")


if __name__ == "__main__":
    main()
