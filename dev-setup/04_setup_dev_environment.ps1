# Comprehensive Development Environment Setup

function Install-DevTools {
    # Install development and productivity tools
    winget install -e --id Git.Git
    winget install -e --id Microsoft.VisualStudioCode
    winget install -e --id GitHub.CLI

    # Configure Git
    git config --global user.name "Your Name"
    # Configure Git (continued)
    git config --global user.email "your.email@example.com"
    git config --global core.editor "code --wait"

    # Install GitHub Copilot CLI
    npm install -g @githubnext/copilot-cli
}
    
function Setup-VSCodeExtensions {
    # Install essential VS Code extensions for AI and Python development
    $extensions = @(
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-toolsai.jupyter",
        "GitHub.copilot",
        "GitHub.copilot-chat",
        "ms-azuretools.vscode-docker",
        "tabnine.tabnine-vscode"
    )

    foreach ($ext in $extensions) {
        code --install-extension $ext
    }
}
    
function Configure-PythonDevEnvironment {
    # Create a global gitignore
    $gitignoreContent = "
    # Python
    __pycache__/
    *.py[cod]
    *$py.class
    *.so
    .Python
    build/
    develop-eggs/
    dist/
    downloads/
    eggs/
    .eggs/
    lib/
    lib64/
    parts/
    sdist/
    var/
    wheels/
    *.egg-info/
    .installed.cfg
    *.egg
    
    # Environments
    .env
    .venv
    env/
    venv/
    ENV/
    env.bak/
    venv.bak/
    
    # IDE
    .vscode/
    .idea/
    
    # Jupyter
    .ipynb_checkpoints
    
    # Misc
    .DS_Store
    "
    
    $gitignorePath = "$env:USERPROFILE\.gitignore_global"
    $gitignoreContent | Out-File $gitignorePath -Encoding UTF8

    git config --global core.excludesfile $gitignorePath
}

Main