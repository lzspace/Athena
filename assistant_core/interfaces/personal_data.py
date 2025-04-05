"""
Script: personal_data.py
Category: Interfaces

Description:
Provides access to personalized information and user scripts stored in PersonalD/.
Used to enrich assistant responses with private context or trigger personal actions.
"""

import os
import json
import subprocess
from pathlib import Path

# Base directory for your personal data/scripts
PERSONALD_PATH = Path(__file__).resolve().parent.parent.parent / "PersonalD"

# ---------- Knowledge Access ----------

def load_preferences() -> dict:
    prefs_path = PERSONALD_PATH / "Knowledge" / "preferences.json"
    if prefs_path.exists():
        with open(prefs_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def load_facts(topic: str = "") -> str:
    facts_path = PERSONALD_PATH / "Knowledge" / "facts.md"
    if facts_path.exists():
        with open(facts_path, "r", encoding="utf-8") as f:
            content = f.read()
            if topic:
                return "\n".join([line for line in content.splitlines() if topic.lower() in line.lower()])
            return content
    return ""

# ---------- Script Execution ----------

def list_scripts() -> list[str]:
    scripts_dir = PERSONALD_PATH / "Scripts"
    return [f.name for f in scripts_dir.glob("*.py")]

def run_script(name: str, args: list[str] = []) -> str:
    script_path = PERSONALD_PATH / "Scripts" / name
    if not script_path.exists():
        return f"Script '{name}' not found."

    try:
        result = subprocess.run(
            ["python3", str(script_path)] + args,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip() or result.stderr.strip()
    except Exception as e:
        return f"Error running script: {e}"