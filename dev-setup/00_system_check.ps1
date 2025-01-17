# System Compatibility and Prerequisite Check Script

function Test-AdminRights {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Get-SystemSpecs {
    $cpu = Get-WmiObject Win32_Processor
    $ram = Get-WmiObject Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum
    $gpu = Get-WmiObject Win32_VideoController

    return @{
        CPU = $cpu.Name
        RAM = "{0} GB" -f ($ram.Sum / 1GB)
        GPU = $gpu.Name
        OSVersion = (Get-WmiObject Win32_OperatingSystem).Caption
    }
}

function Check-PrerequisiteTools {
    $tools = @{
        "Git" = (Get-Command git -ErrorAction SilentlyContinue)
        "Docker" = (Get-Command docker -ErrorAction SilentlyContinue)
        "PowerShell" = $PSVersionTable.PSVersion
    }

    return $tools
}

function Main {
    # Check Admin Rights
    if (-not (Test-AdminRights)) {
        Write-Error "This script requires administrator privileges. Please run as administrator."
        exit 1
    }

    # Display System Specs
    $systemSpecs = Get-SystemSpecs
    Write-Host "System Specifications:"
    $systemSpecs.GetEnumerator() | ForEach-Object { 
        Write-Host ("{0}: {1}" -f $_.Key, $_.Value) 
    }

    # Check Prerequisite Tools
    $prereqTools = Check-PrerequisiteTools
    Write-Host "`nPrerequisite Tools:"
    $prereqTools.GetEnumerator() | ForEach-Object {
        $status = if ($_.Value) { "Installed" } else { "Not Found" }
        Write-Host ("{0}: {1}" -f $_.Key, $status)
    }

    # Hyper-V Check
    $hyperVEnabled = (Get-WindowsOptionalFeature -Online | Where-Object { $_.FeatureName -eq "Microsoft-Hyper-V" }).State
    Write-Host "Hyper-V: $hyperVEnabled"
}

Main
