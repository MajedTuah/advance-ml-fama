# One-time setup for Windows. Run from the repo root in PowerShell:
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#   .\setup\setup_windows.ps1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

Write-Host "Creating .venv with Python 3.11"
if (Get-Command uv -ErrorAction SilentlyContinue) {
    uv venv --python 3.11 .venv                    # uv downloads Python 3.11 if you do not have it
    $env:VIRTUAL_ENV = (Join-Path $PWD ".venv")
    uv pip install -r requirements.txt
}
elseif (Get-Command py -ErrorAction SilentlyContinue) {
    py -3.11 -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python 3.11 not found. Install it, then run this script again:" -ForegroundColor Red
        Write-Host "    py install 3.11      (or download from https://www.python.org/downloads/)"
        Write-Host "  or install uv:  powershell -ExecutionPolicy ByPass -c `"irm https://astral.sh/uv/install.ps1 | iex`""
        exit 1
    }
    .\.venv\Scripts\python.exe -m pip install --upgrade pip
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
}
else {
    Write-Host "Neither uv nor the py launcher was found. Install Python 3.11 from https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "(tick 'Add python.exe to PATH'), or install uv, then run this script again."
    exit 1
}

Write-Host "Checking the environment"
.\.venv\Scripts\python.exe setup\check_env.py
Write-Host ""
Write-Host "Next time, start with:"
Write-Host "    .\.venv\Scripts\Activate.ps1"
Write-Host "    jupyter lab"
