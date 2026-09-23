#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
agent_root="${repo_root}/src/customer-support-agent"

cd "${agent_root}"
uv sync
uv run ruff check .
uv run pytest
uv run python -m compileall -q .

python - "${repo_root}/evals/customer-support.jsonl" <<'PY'
import json
import pathlib
import sys

dataset = pathlib.Path(sys.argv[1])
rows = [json.loads(line) for line in dataset.read_text().splitlines() if line.strip()]
assert len(rows) == 5
assert all({"name", "input", "expected_behavior"} <= row.keys() for row in rows)
PY

echo "Workshop validation completed successfully."
