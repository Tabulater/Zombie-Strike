# Create release directory
$releaseDir = "ZombieStrike_Release_$(Get-Date -Format 'yyyyMMdd')"
$releasePath = Join-Path $PSScriptRoot $releaseDir

# Create directories
New-Item -ItemType Directory -Path $releasePath -Force | Out-Null
New-Item -ItemType Directory -Path "$releasePath\Assets" -Force | Out-Null
New-Item -ItemType Directory -Path "$releasePath\Assets\Enemy" -Force | Out-Null
New-Item -ItemType Directory -Path "$releasePath\Assets\Enemy\Attack" -Force | Out-Null
New-Item -ItemType Directory -Path "$releasePath\Assets\Enemy\Idle" -Force | Out-Null
New-Item -ItemType Directory -Path "$releasePath\Assets\Enemy\Run" -Force | Out-Null
New-Item -ItemType Directory -Path "$releasePath\Assets\Idle" -Force | Out-Null
New-Item -ItemType Directory -Path "$releasePath\Assets\Recharge" -Force | Out-Null
New-Item -ItemType Directory -Path "$releasePath\Assets\Run" -Force | Out-Null

# Copy Python files
Copy-Item "$PSScriptRoot\Tatipamula_Culminating.py" -Destination $releasePath
Copy-Item "$PSScriptRoot\readme.md" -Destination $releasePath

# Copy Assets (excluding source files)
$assetFiles = Get-ChildItem -Path "$PSScriptRoot\Assets" -File
foreach ($file in $assetFiles) {
    Copy-Item $file.FullName -Destination "$releasePath\Assets"
}

# Copy subdirectories
$subDirs = @('Enemy/Attack', 'Enemy/Idle', 'Enemy/Run', 'Idle', 'Recharge', 'Run')
foreach ($dir in $subDirs) {
    $sourceDir = "$PSScriptRoot\Assets\$dir"
    $destDir = "$releasePath\Assets\$dir"
    if (Test-Path $sourceDir) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        Get-ChildItem -Path $sourceDir -File | ForEach-Object {
            Copy-Item $_.FullName -Destination $destDir
        }
    }
}

# Create requirements.txt
@"
pygame==2.5.2
"@ | Out-File -FilePath "$releasePath\requirements.txt" -Encoding utf8

# Copy installation and readme files
Copy-Item "$PSScriptRoot\INSTALL.txt" -Destination $releasePath
Copy-Item "$PSScriptRoot\readme.md" -Destination $releasePath

# Create a quick start guide
@"
QUICK START GUIDE
================

1. Extract the ZIP file to a folder of your choice
2. Double-click 'Launch Game.bat' to start playing!

For detailed installation instructions, see INSTALL.txt
For game information, see readme.md

CONTROLS:
- Arrow Keys: Move and Jump
- Space: Shoot
- R: Reload
- Left Click: Throw grenade (hold to aim)
- ESC: Pause/Quit to menu

Need help? Check INSTALL.txt for troubleshooting.
"@ | Out-File -FilePath "$releasePath\QUICKSTART.txt" -Encoding utf8

# Create a zip file
$zipPath = "$PSScriptRoot\$releaseDir.zip"
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}

Add-Type -Assembly "System.IO.Compression.FileSystem"
[IO.Compression.ZipFile]::CreateFromDirectory($releasePath, $zipPath)

Write-Host "Release created at: $zipPath"
Write-Host "To distribute the game, share the zip file and include the installation instructions from README.txt"
