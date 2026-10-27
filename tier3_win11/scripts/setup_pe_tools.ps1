[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$toolsDir = "C:\Tools"
if (-not (Test-Path $toolsDir)) {
    New-Item -ItemType Directory -Path $toolsDir -Force | Out-Null
}

$pebearUrl = "https://github.com/hasherezade/pe-bear/releases/download/v0.7.2/PE-bear_0.7.2_qt5_x64_win_vs17.zip"
$dieUrl = "https://github.com/horsicq/DIE-engine/releases/download/3.21/die_win64_portable_3.21_x64.zip"

$pebearZip = Join-Path $toolsDir "pe-bear.zip"
$dieZip = Join-Path $toolsDir "die.zip"

Write-Host "[1/4] Downloading PE-bear v0.7.2..."
Invoke-WebRequest -Uri $pebearUrl -OutFile $pebearZip -UserAgent "PowerShell"

Write-Host "[2/4] Downloading Detect It Easy (DIE) v3.21..."
Invoke-WebRequest -Uri $dieUrl -OutFile $dieZip -UserAgent "PowerShell"

Write-Host "[3/4] Extracting archives..."
$pebearExtract = Join-Path $toolsDir "PE-bear"
$dieExtract = Join-Path $toolsDir "DIE"

Expand-Archive -Path $pebearZip -DestinationPath $pebearExtract -Force
Expand-Archive -Path $dieZip -DestinationPath $dieExtract -Force

Remove-Item $pebearZip -Force -ErrorAction SilentlyContinue
Remove-Item $dieZip -Force -ErrorAction SilentlyContinue

Write-Host "[4/4] Creating Desktop shortcuts..."
$wsh = New-Object -ComObject WScript.Shell
$desktop = [Environment]::GetFolderPath("Desktop")

$pebearItem = Get-ChildItem -Path $pebearExtract -Filter "PE-bear.exe" -Recurse | Select-Object -First 1
if ($pebearItem) {
    $sc = $wsh.CreateShortcut((Join-Path $desktop "PE-bear.lnk"))
    $sc.TargetPath = $pebearItem.FullName
    $sc.WorkingDirectory = $pebearItem.DirectoryName
    $sc.Save()
    Write-Host "[+] PE-bear shortcut created: $($pebearItem.FullName)"
}

$dieItem = Get-ChildItem -Path $dieExtract -Filter "die.exe" -Recurse | Select-Object -First 1
if ($dieItem) {
    $sc = $wsh.CreateShortcut((Join-Path $desktop "Detect It Easy.lnk"))
    $sc.TargetPath = $dieItem.FullName
    $sc.WorkingDirectory = $dieItem.DirectoryName
    $sc.Save()
    Write-Host "[+] DIE shortcut created: $($dieItem.FullName)"
}

Write-Host "=== SETUP COMPLETED SUCCESSFULLY ==="
