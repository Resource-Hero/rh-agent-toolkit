#!/usr/bin/env python3
"""Repository checks run in CI. Stdlib only. Usage: python3 tools/check.py

- marketplace.json and every plugin.json parse, and every marketplace source exists
- every SKILL.md has a name matching its folder and a description of at most 1024 characters
- every relative Markdown link inside a skill resolves within its plugin
- every .xml file under a skill's assets/ is well-formed
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_DESCRIPTION = 1024


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fields = {}
    for key in ("name", "description"):
        f = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', m.group(1), re.M)
        if f:
            fields[key] = f.group(1)
    return fields


def main():
    errors = []
    marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    for entry in marketplace["plugins"]:
        src = ROOT / entry["source"]
        manifest = src / ".claude-plugin" / "plugin.json"
        if not manifest.is_file():
            errors.append(f"marketplace: {entry['name']} has no {manifest.relative_to(ROOT)}")
            continue
        if json.loads(manifest.read_text())["name"] != entry["name"]:
            errors.append(f"{manifest.relative_to(ROOT)}: name differs from marketplace entry")

    for skill_md in sorted(ROOT.glob("plugins/*/skills/*/SKILL.md")):
        rel = skill_md.relative_to(ROOT)
        text = skill_md.read_text()
        fm = frontmatter(text)
        if fm.get("name") != skill_md.parent.name:
            errors.append(f"{rel}: name does not match folder")
        if not fm.get("description"):
            errors.append(f"{rel}: no description")
        elif len(fm["description"]) > MAX_DESCRIPTION:
            errors.append(f"{rel}: description is {len(fm['description'])} characters (max {MAX_DESCRIPTION})")
        plugin_root = skill_md.parents[2].resolve()
        for md in skill_md.parent.rglob("*.md"):
            for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", md.read_text()):
                if re.match(r"[a-z]+:", target):
                    continue
                path = (md.parent / target).resolve()
                if not path.exists():
                    errors.append(f"{md.relative_to(ROOT)}: broken link {target}")
                elif plugin_root not in path.parents:
                    errors.append(f"{md.relative_to(ROOT)}: link {target} leaves its plugin")

    for xml_file in sorted(ROOT.glob("plugins/*/skills/*/assets/**/*.xml")):
        try:
            ET.parse(xml_file)
        except ET.ParseError as e:
            errors.append(f"{xml_file.relative_to(ROOT)}: {e}")

    for e in errors:
        print("ERROR", e)
    print(f"{len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
