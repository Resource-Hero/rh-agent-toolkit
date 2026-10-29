#!/usr/bin/env bash
# Run a plugin's routing evals with `claude plugin eval`.
# The eval runner drops plugins whose dependencies aren't installed, and rh-connect
# has no skills, so this copies the plugin to a temp dir without `dependencies` first.
# Usage: tools/run_evals.sh <plugin> [extra claude plugin eval args, e.g. --case 'confuse-*']
set -euo pipefail
plugin="${1:?usage: tools/run_evals.sh <plugin> [eval args]}"; shift
root="$(cd "$(dirname "$0")/.." && pwd)"
src="$root/plugins/$plugin"
[ -d "$src/evals" ] || { echo "no evals in $src" >&2; exit 1; }
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
cp -r "$src" "$tmp/$plugin"; rm -rf "$tmp/$plugin/evals/results"
python3 - "$tmp/$plugin/.claude-plugin/plugin.json" <<'PY'
import json, sys
p = sys.argv[1]; d = json.load(open(p)); d.pop("dependencies", None)
json.dump(d, open(p, "w"), indent=2)
PY
(cd "$tmp" && claude plugin eval "./$plugin" --ablation none -j 4 "$@")
mkdir -p "$src/evals/results"; cp -r "$tmp/$plugin/evals/results/." "$src/evals/results/"
