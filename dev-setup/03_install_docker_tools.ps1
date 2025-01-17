# Docker and Container Tools Setup Script

function Install-DockerTools {
    # Ensure Hyper-V is enabled
    Enable-WindowsOptionalFeature -Online -FeatureName "Microsoft-Hyper-V" -All

    # Install Docker Desktop (requires manual download due to licensing)
    Write-Host "Please download and install Docker Desktop manually from the official website."
    Start-Process "https://www.docker.com/products/docker-desktop"

    # Install additional container tools
    winget install -e --id Kubernetes.kubectl
    winget install -e --id Helm.Helm
}

function Configure-DockerSettings {
    # Configure Docker Desktop settings
    $dockerConfig = @{
        "buildkit" = $true
        "experimental" = $true
        "features" = @{
            "buildkit" = $true
        }
    }

    $configPath = "$env:USERPROFILE\.docker\config.json"
    $dockerConfig | ConvertTo-Json | Out-File $configPath
}

function Setup-LocalRegistries {
    # Create local Docker registries for AI models and services
    docker run -d -p 5000:5000 --restart=always --name local-registry registry:2
}

Main