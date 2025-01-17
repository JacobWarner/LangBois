# Conda Environment Setup Script

$CONDA_ENV_NAME = "ai-dev"

function Create-CondaEnvironment {
    $pythonVersion = (python --version)
    
    # Create base AI development environment
    conda create -n $CONDA_ENV_NAME python=$pythonVersion -y
    conda activate $CONDA_ENV_NAME

    # Install core data science and AI packages
    conda install -n $CONDA_ENV_NAME -y \
        numpy \
        pandas \
        scipy \
        scikit-learn \
        matplotlib \
        seaborn \
        jupyter \
        pytorch \
        transformers \
        tensorflow \
        cudatoolkit

    # Install additional AI/ML libraries via pip in the conda environment
    conda run -n $CONDA_ENV_NAME pip install \
        langchain \
        openai \
        huggingface_hub \
        sentence-transformers
}

function Set-CondaDefaults {
    # Configure Conda defaults
    conda config --set auto_activate_base false
    conda config --add channels conda-forge
    conda config --set channel_priority strict
    conda config --set default_env $CONDA_ENV_NAME
}

function Main {
    Create-CondaEnvironment
    Set-CondaDefaults
}

Main