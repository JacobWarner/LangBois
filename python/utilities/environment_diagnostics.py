import sys
import platform
import psutil
import GPUtil
import torch
import transformers
import langchain

def get_system_info():
    """Collect comprehensive system information"""
    return {
        "OS": platform.platform(),
        "Python Version": platform.python_version(),
        "CPU": {
            "Name": platform.processor(),
            "Cores": psutil.cpu_count(logical=False),
            "Logical Cores": psutil.cpu_count(logical=True)
        },
        "Memory": {
            "Total": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            "Available": f"{psutil.virtual_memory().available / (1024**3):.2f} GB"
        },
        "GPU": get_gpu_info(),
        "Libraries": get_library_versions()
    }

def get_gpu_info():
    """Retrieve GPU information"""
    try:
        gpus = GPUtil.getGPUs()
        gpu_info = []
        for gpu in gpus:
            gpu_info.append({
                "Name": gpu.name,
                "Driver": gpu.driver,
                "Memory": f"{gpu.memoryTotal} MB",
                "GPU Utilization": f"{gpu.load*100:.2f}%",
                "Memory Utilization": f"{gpu.memoryUtil*100:.2f}%"
            })
        return gpu_info
    except Exception as e:
        return [{"Error": str(e)}]

def get_library_versions():
    """Collect versions of key AI and ML libraries"""
    return {
        "Python": sys.version,
        "PyTorch": torch.__version__,
        "Transformers": transformers.__version__,
        "LangChain": langchain.__version__,
        "NumPy": __import__('numpy').__version__,
        "Pandas": __import__('pandas').__version__
    }

def check_cuda_availability():
    """Check CUDA availability and device details"""
    cuda_info = {
        "CUDA Available": torch.cuda.is_available(),
        "CUDA Version": torch.version.cuda if torch.cuda.is_available() else "N/A",
        "cuDNN Version": torch.backends.cudnn.version() if torch.cuda.is_available() else "N/A"
    }
    
    if torch.cuda.is_available():
        cuda_info["CUDA Devices"] = [
            {
                "Name": torch.cuda.get_device_name(i),
                "Compute Capability": torch.cuda.get_device_capability(i)
            } for i in range(torch.cuda.device_count())
        ]
    
    return cuda_info

def performance_benchmark():
    """Run basic performance benchmarks"""
    import time
    import numpy as np
    import torch

    benchmarks = {
        "NumPy Matrix Multiplication": numpy_benchmark(),
        "PyTorch Matrix Multiplication": torch_benchmark(),
        "Python List Comprehension": python_list_benchmark()
    }
    
    return benchmarks

def numpy_benchmark():
    """NumPy matrix multiplication benchmark"""
    start = time.time()
    matrix_size = 5000
    a = np.random.rand(matrix_size, matrix_size)
    b = np.random.rand(matrix_size, matrix_size)
    c = np.matmul(a, b)
    end = time.time()
    return {
        "Time": f"{end - start:.4f} seconds",
        "Matrix Size": f"{matrix_size}x{matrix_size}"
    }

def torch_benchmark():
    """PyTorch matrix multiplication benchmark"""
    start = time.time()
    matrix_size = 5000
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    a = torch.rand(matrix_size, matrix_size, device=device)
    b = torch.rand(matrix_size, matrix_size, device=device)
    c = torch.matmul(a, b)
    end = time.time()
    return {
        "Time": f"{end - start:.4f} seconds",
        "Matrix Size": f"{matrix_size}x{matrix_size}",
        "Device": str(device)
    }

def python_list_benchmark():
    """Python list comprehension benchmark"""
    start = time.time()
    result = [x**2 for x in range(10_000_000)]
    end = time.time()
    return {
        "Time": f"{end - start:.4f} seconds",
        "List Size": "10 million elements"
    }

def main():
    """Main diagnostic function to print all system information"""
    print("=== System Diagnostics ===")
    
    system_info = get_system_info()
    print("\n--- System Information ---")
    import json
    print(json.dumps(system_info, indent=2))

    print("\n--- CUDA Availability ---")
    cuda_info = check_cuda_availability()
    print(json.dumps(cuda_info, indent=2))

    print("\n--- Performance Benchmarks ---")
    benchmarks = performance_benchmark()
    print(json.dumps(benchmarks, indent=2))

    # Optional: Generate a comprehensive report
    generate_diagnostic_report(system_info, cuda_info, benchmarks)

def generate_diagnostic_report(system_info, cuda_info, benchmarks):
    """
    Generate a comprehensive diagnostic report in Markdown format
    
    Args:
        system_info (dict): Collected system information
        cuda_info (dict): CUDA availability details
        benchmarks (dict): Performance benchmark results
    """
    import os
    from datetime import datetime

    report_dir = os.path.join(os.path.expanduser("~"), "AIDevDiagnostics")
    os.makedirs(report_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(report_dir, f"system_diagnostic_report_{timestamp}.md")

    with open(report_path, 'w') as report_file:
        # Report Header
        report_file.write(f"# AI Development Environment Diagnostic Report\n")
        report_file.write(f"**Generated:** {datetime.now()}\n\n")

        # System Information Section
        report_file.write("## System Information\n")
        report_file.write(f"- **Operating System:** {system_info['OS']}\n")
        report_file.write(f"- **Python Version:** {system_info['Python Version']}\n")
        
        # CPU Details
        report_file.write("### CPU\n")
        report_file.write(f"- **Name:** {system_info['CPU']['Name']}\n")
        report_file.write(f"- **Physical Cores:** {system_info['CPU']['Cores']}\n")
        report_file.write(f"- **Logical Cores:** {system_info['CPU']['Logical Cores']}\n")

        # Memory Details
        report_file.write("### Memory\n")
        report_file.write(f"- **Total Memory:** {system_info['Memory']['Total']}\n")
        report_file.write(f"- **Available Memory:** {system_info['Memory']['Available']}\n")

        # GPU Details
        report_file.write("## GPU Information\n")
        for gpu in system_info['GPU']:
            report_file.write(f"### {gpu['Name']}\n")
            report_file.write(f"- **Driver:** {gpu.get('Driver', 'N/A')}\n")
            report_file.write(f"- **Memory:** {gpu.get('Memory', 'N/A')}\n")
            report_file.write(f"- **GPU Utilization:** {gpu.get('GPU Utilization', 'N/A')}\n")
            report_file.write(f"- **Memory Utilization:** {gpu.get('Memory Utilization', 'N/A')}\n")

        # CUDA Information
        report_file.write("## CUDA Availability\n")
        report_file.write(f"- **CUDA Available:** {cuda_info['CUDA Available']}\n")
        report_file.write(f"- **CUDA Version:** {cuda_info['CUDA Version']}\n")
        report_file.write(f"- **cuDNN Version:** {cuda_info['cuDNN Version']}\n")

        if cuda_info['CUDA Available']:
            report_file.write("### CUDA Devices\n")
            for device in cuda_info.get('CUDA Devices', []):
                report_file.write(f"- **Name:** {device['Name']}\n")
                report_file.write(f"  - **Compute Capability:** {device['Compute Capability']}\n")

                # Performance Benchmarks Section
        report_file.write("## Performance Benchmarks\n")
        
        report_file.write("### NumPy Matrix Multiplication\n")
        for key, value in benchmarks['NumPy Matrix Multiplication'].items():
            report_file.write(f"- **{key}:** {value}\n")
        
        report_file.write("\n### PyTorch Matrix Multiplication\n")
        for key, value in benchmarks['PyTorch Matrix Multiplication'].items():
            report_file.write(f"- **{key}:** {value}\n")
        
        report_file.write("\n### Python List Comprehension\n")
        for key, value in benchmarks['Python List Comprehension'].items():
            report_file.write(f"- **{key}:** {value}\n")

        # Library Versions
        report_file.write("\n## Installed Library Versions\n")
        library_versions = get_library_versions()
        for lib, version in library_versions.items():
            report_file.write(f"- **{lib}:** {version}\n")

        # Recommendations Section
        report_file.write("\n## Recommendations\n")
        recommendations = generate_recommendations(system_info, cuda_info)
        for recommendation in recommendations:
            report_file.write(f"- {recommendation}\n")

    print(f"\nDiagnostic report generated: {report_path}")
    return report_path

def generate_recommendations(system_info, cuda_info):
    """
    Generate system recommendations based on diagnostic information
    
    Args:
        system_info (dict): Collected system information
        cuda_info (dict): CUDA availability details
    
    Returns:
        list: Recommendations for system optimization
    """
    recommendations = []

    # Memory Recommendations
    total_memory = float(system_info['Memory']['Total'].replace(' GB', ''))
    if total_memory < 32:
        recommendations.append(f"Consider upgrading RAM. Current total memory is {total_memory} GB, which may be insufficient for complex AI workloads.")

    # GPU Recommendations
    if not cuda_info['CUDA Available']:
        recommendations.append("No CUDA-compatible GPU detected. Consider using a CUDA-enabled GPU for accelerated computing.")
    else:
        gpu_memory = [gpu.get('Memory', '0 MB') for gpu in system_info['GPU']]
        if any(int(mem.split()) < 8192 for mem in gpu_memory):
            recommendations.append("Consider upgrading GPU with more than 8GB VRAM for better AI/ML performance.")

    # Python and Library Recommendations
    python_version = system_info['Python Version']
    if not python_version.startswith(('3.9', '3.10', '3.11')):
        recommendations.append(f"Consider upgrading Python. Current version {python_version} may not be optimal for latest AI libraries.")

    # Storage Recommendations
    import shutil
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    if free_gb < 100:
        recommendations.append(f"Low disk space. Only {free_gb} GB free. Recommended to have at least 100 GB for AI development.")

    # Performance Recommendations
    if total_memory < 64:
        recommendations.append("For optimal AI/ML workloads, consider 64GB+ RAM, especially for large model training.")

    return recommendations

def export_system_info_json():
    """
    Export system information to a JSON file for potential future use
    """
    import json
    import os

    system_info = get_system_info()
    cuda_info = check_cuda_availability()
    benchmarks = performance_benchmark()

    export_data = {
        "system_info": system_info,
        "cuda_info": cuda_info,
        "benchmarks": benchmarks
    }

    export_dir = os.path.join(os.path.expanduser("~"), "AIDevDiagnostics")
    os.makedirs(export_dir, exist_ok=True)

    export_path = os.path.join(export_dir, f"system_diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    with open(export_path, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"System information exported to: {export_path}")
    return export_path

def continuous_monitoring():
    """
    Set up a continuous monitoring service for system resources
    Logs system performance metrics periodically
    """
    import time
    import logging
    from threading import Thread

    logging.basicConfig(
        filename='ai_dev_system_monitor.log', 
        level=logging.INFO, 
        format='%(asctime)s - %(message)s'
    )

    def monitor_resources():
        while True:
            # CPU Usage
            cpu_percent = psutil.cpu_percent(interval=1)
            logging.info(f"CPU Usage: {cpu_percent}%")

            # Memory Usage
            memory = psutil.virtual_memory()
            logging.info(f"Memory Usage: {memory.percent}%")

            # GPU Usage (if available)
            if torch.cuda.is_available():
                gpu_memory = torch.cuda.memory_allocated() / torch.cuda.max_memory_allocated() * 100
                logging.info(f"GPU Memory Usage: {gpu_memory:.2f}%")

            # Sleep for 5 minutes
            time.sleep(300)

    # Start monitoring in a separate thread
    monitor_thread = Thread(target=monitor_resources, daemon=True)
    monitor_thread.start()

def ai_environment_health_check():
    """
    Comprehensive health check for AI development environment
    
    Performs:
    - System diagnostics
    - Library compatibility check
    - Performance benchmarking
    - Recommendations generation
    """
    print("=== AI Development Environment Health Check ===")

    # System Information
    system_info = get_system_info()
    print("\n--- System Information Summary ---")
    print(f"OS: {system_info['OS']}")
    print(f"Python: {system_info['Python Version']}")
    print(f"CPU: {system_info['CPU']['Name']}")
    print(f"Memory: {system_info['Memory']['Total']}")

    # CUDA and GPU Check
    cuda_info = check_cuda_availability()
    print("\n--- CUDA and GPU Status ---")
    print(f"CUDA Available: {cuda_info['CUDA Available']}")
    if cuda_info['CUDA Available']:
        print(f"CUDA Version: {cuda_info['CUDA Version']}")
        print("CUDA Devices:")
        for device in cuda_info.get('CUDA Devices', []):
            print(f"  - {device['Name']} (Compute: {device['Compute Capability']})")

    # Library Versions
    library_versions = get_library_versions()
    print("\n--- Key Library Versions ---")
    for lib, version in library_versions.items():
        print(f"{lib}: {version}")

    # Performance Benchmarks
    print("\n--- Performance Benchmarks ---")
    benchmarks = performance_benchmark()
    for benchmark_name, results in benchmarks.items():
        print(f"\n{benchmark_name}:")
        for key, value in results.items():
            print(f"  {key}: {value}")

    # Generate Recommendations
    recommendations = generate_recommendations(system_info, cuda_info)
    print("\n--- Recommendations ---")
    for recommendation in recommendations:
        print(f"- {recommendation}")

    # Optional: Generate detailed report
    generate_diagnostic_report(system_info, cuda_info, benchmarks)

def main():
    """Main execution point for diagnostics"""
    ai_environment_health_check()
    export_system_info_json()
    continuous_monitoring()

if __name__ == "__main__":
    main()



