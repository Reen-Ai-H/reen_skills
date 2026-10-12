#!/usr/bin/env python3
"""Create missing product-lifecycle files without overwriting project facts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TEMPLATES = {
    "AGENTS.md": "AGENTS.md",
    "docs/README.md": "docs-README.md",
    "docs/PRODUCT_SPEC.md": "PRODUCT_SPEC.md",
    "docs/DECISIONS.md": "DECISIONS.md",
    "docs/UX_FLOWS.md": "UX_FLOWS.md",
    "docs/DESIGN_SYSTEM.md": "DESIGN_SYSTEM.md",
    "docs/ACCEPTANCE.md": "ACCEPTANCE.md",
    "docs/AGENT_WORKFLOW.md": "AGENT_WORKFLOW.md",
    "PROGRESS.md": "PROGRESS.md",
    "BLOCKED.md": "BLOCKED.md",
}

AUTONOMOUS_CONFIG = '''model = "gpt-5.6-luna"
model_reasoning_effort = "max"
approval_policy = "never"
sandbox_mode = "danger-full-access"

[models.new_thread]
model = "gpt-5.6-luna"
model_reasoning_effort = "max"

[agents]
enabled = true
default_subagent_model = "gpt-5.6-luna"
default_subagent_reasoning_effort = "max"
'''


def append_ignore(project: Path, entry: str) -> bool:
    path = project / ".gitignore"
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    if entry in {line.strip() for line in current.splitlines()}:
        return False
    prefix = "" if not current or current.endswith("\n") else "\n"
    path.write_text(current + prefix + "\n# Machine-local Codex settings\n" + entry + "\n", encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument(
        "--autonomous-luna-max",
        action="store_true",
        help="Create machine-local Luna Max/full-access/no-approval project config if absent.",
    )
    args = parser.parse_args()

    project = args.project.expanduser().resolve()
    if not project.is_dir():
        parser.error(f"project directory does not exist: {project}")

    skill = Path(__file__).resolve().parents[1]
    template_dir = skill / "assets" / "templates"
    created: list[str] = []
    preserved: list[str] = []

    for relative, template in TEMPLATES.items():
        destination = project / relative
        if destination.exists():
            preserved.append(relative)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text((template_dir / template).read_text(encoding="utf-8"), encoding="utf-8")
        created.append(relative)

    if args.autonomous_luna_max:
        config = project / ".codex" / "config.toml"
        if config.exists():
            preserved.append(".codex/config.toml")
        else:
            config.parent.mkdir(parents=True, exist_ok=True)
            config.write_text(AUTONOMOUS_CONFIG, encoding="utf-8")
            created.append(".codex/config.toml")
        if append_ignore(project, ".codex/config.toml"):
            created.append(".gitignore entry: .codex/config.toml")

    print(json.dumps({"project": str(project), "created": created, "preserved": preserved}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
