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

function Install-WindowsTool([string]$Id, [string]$Name) {
    if ($null -eq (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw "No se encontro winget. Instala $Name manualmente y vuelve a ejecutar este script."
    }
    winget install --id $Id --exact --source winget --accept-source-agreements --accept-package-agreements
}

$python = Find-CommandPath "python"
$git = Find-CommandPath "git"
$uv = Find-CommandPath "uv"

if ($null -eq $python -and $InstallMissing) {
    Install-WindowsTool "Python.Python.3.12" "Python 3.12"
    $python = Find-CommandPath "python"
}
if ($null -eq $git -and $InstallMissing) {
    Install-WindowsTool "Git.Git" "Git"
    $git = Find-CommandPath "git"
}
if ($null -eq $uv -and $InstallMissing) {
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
    $uv = Find-CommandPath "uv"
}

$missing = @()
if ($null -eq $python) { $missing += "python" }
if ($null -eq $git) { $missing += "git" }
if ($null -eq $uv) { $missing += "uv" }
if ($missing.Count -gt 0) {
    throw "Faltan herramientas: $($missing -join ', '). Ejecuta .\scripts\bootstrap.ps1 -InstallMissing o instalalas manualmente."
}

uv sync --locked
Write-Output "Dependencias instaladas."
