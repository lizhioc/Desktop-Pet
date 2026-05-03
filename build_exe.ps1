$ErrorActionPreference = "Stop"

Remove-Item -Recurse -Force -Path build, dist -ErrorAction SilentlyContinue

$iconPath = Join-Path $PSScriptRoot "assets\icons\feather.ico"
$assetData = "assets;assets"

python -m PyInstaller `
    --clean `
    --noconfirm `
    --onefile `
    --windowed `
    --name DesktopPet `
    --icon "$iconPath" `
    --add-data "$assetData" `
    main.py

Write-Host ""
Write-Host "Build finished: dist\DesktopPet.exe"
