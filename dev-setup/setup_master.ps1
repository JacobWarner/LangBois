# Master AI Development Environment Setup Script

param (
    [switch]$SkipSystemCheck = $false,
    [switch]$SkipPythonInstall = $false,
    [switch]$SkipCondaSetup = $false,
    [switch]$SkipDockerSetup = $false,
    [switch]$SkipDevTools = $false,
    [switch]$SkipAIDependencies = $false
)

function Write-Status {
    param([string]$Message, [string]$Color = 'Green')
    Write-Host $Message -ForegroundColor $Color
}

function Main {
    # Ensure script runs with admin privileges
    if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
        Write-Error "Please run this script as Administrator"
        exit 1
    }

    # Execution order of setup scripts
    $setupScripts = @(
        @{Name = "00_system_check.ps1"; Skip = $SkipSystemCheck},
        @{Name = "01_install_python.ps1"; Skip = $SkipPythonInstall},
        @{Name = "02_setup_conda.ps1"; Skip = $SkipCondaSetup},
        @{Name = "03_install_docker_tools.ps1"; Skip = $SkipDockerSetup},
        @{Name = "04_setup_dev_environment.ps1"; Skip = $SkipDevTools},
        @{Name = "05_install_ai_dependencies.ps1"; Skip = $SkipAIDependencies}
    )

    foreach ($script in $setupScripts) {
        if (-not $script.Skip) {
            Write-Status "Executing $($script.Name)..."
            & ".\$($script.Name)"
            
            if ($LASTEXITCODE -ne 0) {
                Write-Error "Script $($script.Name) failed. Stopping setup."
                exit 1
            }
        } else {
            Write-Status "Skipping $($script.Name)" -Color 'Yellow'
        }
    }

    # Final configuration and verification
    Verify-Environment
}

function Verify-Environment {
    Write-Status "Verifying AI Development Environment..."
    
    # Check Python installation
    $pythonVersion = python --version
    Write-Host "Python Version: $pythonVersion"

    # Check Conda environment
    conda info --envs

    # Check Docker installation
    docker version

    # Check AI library installations
    pip list | Select-String -Pattern "torch|transformers|langchain|openai"
}

# Usage examples:
# .\setup_ai_dev_environment.ps1 
# .\setup_ai_dev_environment.ps1 -SkipSystemCheck
# .\setup_ai_dev_environment.ps1 -SkipPythonInstall -SkipDockerSetup

Main
