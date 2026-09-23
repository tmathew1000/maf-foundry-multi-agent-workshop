$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$agentRoot = Join-Path $repoRoot "src\customer-support-agent"

Push-Location $agentRoot
try {
    uv sync
    uv run ruff check .
    uv run pytest
    uv run python -m compileall -q .
}
finally {
    Pop-Location
}

Get-Content (Join-Path $repoRoot "evals\customer-support.jsonl") |
    ForEach-Object { $_ | ConvertFrom-Json | Out-Null }

Write-Host "Workshop validation completed successfully."

