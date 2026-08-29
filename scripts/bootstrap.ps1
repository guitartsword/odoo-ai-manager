param(
    [switch]$InstallMissing
)

$ErrorActionPreference = "Stop"

function Find-CommandPath([string]$Name) {
    $command = Get-Command $Name -ErrorAction SilentlyContinue
    if ($null -eq $command) {
        return $null
    }
    return $command.Source
}

function Refresh-Path {
    $machinePath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($null -ne $machinePath -or $null -ne $userPath) {
        $env:Path = "$machinePath;$userPath"
    }
}

function Test-SupportedPython([string]$Path) {
    if ($null -eq $Path) {
        return $false
    }
    & $Path -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)" 2>$null
    return $LASTEXITCODE -eq 0
}

function Install-WindowsTool([string]$Id, [string]$Name) {
    if ($null -eq (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw "No se encontro winget. Instala $Name manualmente y vuelve a ejecutar este script."
    }
    winget install --id $Id --exact --source winget --accept-source-agreements --accept-package-agreements
}

$python = Find-CommandPath "python"
$git = Find-CommandPath "git"
$uv = Find-CommandPath "uv"
$pythonIsSupported = Test-SupportedPython $python

if (-not $pythonIsSupported -and $InstallMissing) {
    Install-WindowsTool "Python.Python.3.12" "Python 3.12"
    Refresh-Path
    $python = Find-CommandPath "python"
    $pythonIsSupported = Test-SupportedPython $python
}
if ($null -eq $git -and $InstallMissing) {
    Install-WindowsTool "Git.Git" "Git"
    Refresh-Path
    $git = Find-CommandPath "git"
}
if ($null -eq $uv -and $InstallMissing) {
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    Refresh-Path
    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
    $uv = Find-CommandPath "uv"
}

$missing = @()
if (-not $pythonIsSupported) { $missing += "Python 3.12+" }
if ($null -eq $git) { $missing += "git" }
if ($null -eq $uv) { $missing += "uv" }
if ($missing.Count -gt 0) {
    throw "Faltan herramientas: $($missing -join ', '). Ejecuta .\scripts\bootstrap.ps1 -InstallMissing o instalalas manualmente."
}

if (Test-Path -LiteralPath (Join-Path (Get-Location) "pyproject.toml")) {
    uv sync --locked
    Write-Output "Dependencias instaladas."
} else {
    Write-Output "Herramientas listas. No se encontro pyproject.toml; ejecuta este script de nuevo dentro del checkout."
}
