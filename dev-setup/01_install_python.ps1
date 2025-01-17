# Anaconda Installation and Configuration Script

$ANACONDA_VERSION = "2024.10-1"
$ANACONDA_DOWNLOAD_URL = "https://repo.anaconda.com/archive/Anaconda3-${ANACONDA_VERSION}-Windows-x86_64.exe"
$ANACONDA_INSTALLER = "$env:TEMP\anaconda-installer.exe"
$ANACONDA_INSTALL_LOCATION = "~\Anaconda3"

function Install-Anaconda {
    if (Test-Path "$ANACONDA_INSTALL_LOCATION\anaconda3") {
        Write-Host "Anaconda is already installed at $ANACONDA_INSTALL_LOCATION"
        return
    }
    
    Write-Host "Downloading Anaconda $ANACONDA_VERSION..."
    Invoke-WebRequest -Uri $ANACONDA_DOWNLOAD_URL -OutFile $ANACONDA_INSTALLER

    Write-Host "Installing Anaconda..."
    $ANACONDA_INSTALL_LOCATION = 
    Start-Process -FilePath $ANACONDA_INSTALLER -ArgumentList "/S /AddToPath=1 /RegisterPython=1 /NoRegistry=1 /D=$ANACONDA_INSTALL_LOCATION" -Wait

    # Verify Anaconda installation
    $anacondaPath = (Get-Command conda -ErrorAction SilentlyContinue).Source
    if ($anacondaPath) {
        $condaVersion = (conda --version)
        $pythonVersion = (python --version)
        Write-Host "Anaconda installed successfully:"
        Write-Host "- $condaVersion"
        Write-Host "- $pythonVersion"
        
        # Initialize conda for PowerShell
        conda init powershell
    } else {
        Write-Error "Anaconda installation failed"
        exit 1
    }

    # Clean up installer
    Remove-Item $ANACONDA_INSTALLER -ErrorAction SilentlyContinue
}

function Main {
    Install-Anaconda
}

Main
