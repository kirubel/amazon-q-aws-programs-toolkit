# Amazon Q Repeatable Tools for AWS Programs

## Overview
This document contains specific tools and scripts that Amazon Q can help create for repeatable use in AWS MAP, OLA, and ONE OLA programs.

## Infrastructure Assessment Tools

### 1. Server Inventory Analysis Script

```python
#!/usr/bin/env python3
"""
Server Inventory Analysis Tool
Analyzes on-premises server inventory and recommends AWS equivalents
"""

import pandas as pd
import json
from typing import Dict, List, Tuple

class ServerInventoryAnalyzer:
    def __init__(self):
        self.ec2_instance_mapping = {
            # CPU-based mappings
            (1, 2): "t3.small",
            (2, 4): "t3.medium", 
            (4, 8): "t3.large",
            (8, 16): "m5.2xlarge",
            (16, 32): "m5.4xlarge",
            # Add more mappings based on CPU/Memory ratios
        }
        
    def analyze_inventory(self, csv_file: str) -> Dict:
        """Analyze server inventory CSV and recommend AWS instances"""
        df = pd.read_csv(csv_file)
        recommendations = []
        
        for _, server in df.iterrows():
            cpu_cores = server.get('CPU_Cores', 0)
            memory_gb = server.get('Memory_GB', 0)
            storage_gb = server.get('Storage_GB', 0)
            
            # Recommend EC2 instance type
            instance_type = self._recommend_instance_type(cpu_cores, memory_gb)
            
            # Recommend storage type
            storage_type = self._recommend_storage_type(storage_gb, server.get('Storage_Type', ''))
            
            # Calculate costs
            monthly_cost = self._calculate_monthly_cost(instance_type, storage_gb)
            
            recommendation = {
                'server_name': server.get('Server_Name', ''),
                'current_specs': f"{cpu_cores}vCPU, {memory_gb}GB RAM, {storage_gb}GB Storage",
                'recommended_instance': instance_type,
                'recommended_storage': storage_type,
                'estimated_monthly_cost': monthly_cost,
                'migration_complexity': self._assess_migration_complexity(server)
            }
            recommendations.append(recommendation)
            
        return {
            'total_servers': len(recommendations),
            'total_estimated_cost': sum(r['estimated_monthly_cost'] for r in recommendations),
            'recommendations': recommendations
        }
    
    def _recommend_instance_type(self, cpu: int, memory: int) -> str:
        """Recommend EC2 instance type based on CPU and memory"""
        # Simple mapping logic - can be enhanced
        for (cpu_threshold, mem_threshold), instance_type in self.ec2_instance_mapping.items():
            if cpu <= cpu_threshold and memory <= mem_threshold:
                return instance_type
        return "m5.8xlarge"  # Default for high-spec servers
    
    def _recommend_storage_type(self, storage_gb: int, current_type: str) -> str:
        """Recommend EBS volume type"""
        if storage_gb < 100:
            return "gp3"
        elif "SSD" in current_type.upper():
            return "gp3"
        elif storage_gb > 1000:
            return "st1"  # Throughput optimized
        else:
            return "gp3"
    
    def _calculate_monthly_cost(self, instance_type: str, storage_gb: int) -> float:
        """Calculate estimated monthly cost (simplified)"""
        # Simplified cost calculation - should use actual AWS pricing
        instance_costs = {
            "t3.small": 15.33,
            "t3.medium": 30.66,
            "t3.large": 61.32,
            "m5.2xlarge": 281.28,
            "m5.4xlarge": 562.56,
            "m5.8xlarge": 1125.12
        }
        
        instance_cost = instance_costs.get(instance_type, 100)
        storage_cost = storage_gb * 0.10  # $0.10 per GB for gp3
        
        return instance_cost + storage_cost
    
    def _assess_migration_complexity(self, server: pd.Series) -> str:
        """Assess migration complexity based on server characteristics"""
        os_type = server.get('OS', '').lower()
        app_count = server.get('Application_Count', 0)
        
        if 'windows' in os_type and app_count > 5:
            return "High"
        elif app_count > 3:
            return "Medium"
        else:
            return "Low"

# Usage example
if __name__ == "__main__":
    analyzer = ServerInventoryAnalyzer()
    results = analyzer.analyze_inventory("server_inventory.csv")
    
    print(f"Analysis Results:")
    print(f"Total Servers: {results['total_servers']}")
    print(f"Estimated Monthly Cost: ${results['total_estimated_cost']:.2f}")
    
    # Save results to JSON
    with open("migration_recommendations.json", "w") as f:
        json.dump(results, f, indent=2)
```

### 2. Windows License Assessment Tool

```powershell
# Windows License Assessment Script
# Analyzes Windows Server licensing and calculates Hybrid Benefit savings

param(
    [string]$OutputPath = ".\license_assessment.csv"
)

function Get-WindowsLicenseInfo {
    $computers = Get-ADComputer -Filter {OperatingSystem -like "*Windows Server*"} -Properties OperatingSystem, OperatingSystemVersion
    $licenseInfo = @()
    
    foreach ($computer in $computers) {
        try {
            $os = Get-WmiObject -Class Win32_OperatingSystem -ComputerName $computer.Name -ErrorAction Stop
            $licenseStatus = Get-WmiObject -Class SoftwareLicensingProduct -ComputerName $computer.Name -ErrorAction Stop | 
                Where-Object {$_.Name -like "*Windows Server*" -and $_.LicenseStatus -eq 1}
            
            $info = [PSCustomObject]@{
                ComputerName = $computer.Name
                OperatingSystem = $os.Caption
                Version = $os.Version
                Edition = if ($os.Caption -like "*Standard*") {"Standard"} elseif ($os.Caption -like "*Datacenter*") {"Datacenter"} else {"Unknown"}
                ProcessorCount = $os.NumberOfProcessors
                LogicalProcessors = $os.NumberOfLogicalProcessors
                TotalPhysicalMemory = [math]::Round($os.TotalPhysicalMemory / 1GB, 2)
                LicenseStatus = if ($licenseStatus) {"Licensed"} else {"Unlicensed"}
                HybridBenefitEligible = $true
                EstimatedMonthlySavings = 0
            }
            
            # Calculate potential Hybrid Benefit savings
            if ($info.Edition -eq "Standard") {
                $info.EstimatedMonthlySavings = 50 # Simplified calculation
            } elseif ($info.Edition -eq "Datacenter") {
                $info.EstimatedMonthlySavings = 200 # Simplified calculation
            }
            
            $licenseInfo += $info
        }
        catch {
            Write-Warning "Could not retrieve information for $($computer.Name): $($_.Exception.Message)"
        }
    }
    
    return $licenseInfo
}

function Export-LicenseAssessment {
    param($LicenseData, $OutputPath)
    
    $LicenseData | Export-Csv -Path $OutputPath -NoTypeInformation
    
    # Generate summary report
    $totalServers = $LicenseData.Count
    $standardEdition = ($LicenseData | Where-Object {$_.Edition -eq "Standard"}).Count
    $datacenterEdition = ($LicenseData | Where-Object {$_.Edition -eq "Datacenter"}).Count
    $totalSavings = ($LicenseData | Measure-Object -Property EstimatedMonthlySavings -Sum).Sum
    
    $summary = @"
Windows Server License Assessment Summary
========================================
Total Servers Analyzed: $totalServers
Standard Edition: $standardEdition
Datacenter Edition: $datacenterEdition
Estimated Monthly Savings with Hybrid Benefit: `$$totalSavings

Detailed results saved to: $OutputPath
"@
    
    Write-Host $summary
    $summary | Out-File -FilePath ($OutputPath -replace ".csv", "_summary.txt")
}

# Main execution
Write-Host "Starting Windows License Assessment..."
$licenseData = Get-WindowsLicenseInfo
Export-LicenseAssessment -LicenseData $licenseData -OutputPath $OutputPath
Write-Host "Assessment completed!"
```

### 3. Storage Analysis and Migration Planning Tool

```python
#!/usr/bin/env python3
"""
Storage Analysis and Migration Planning Tool
Analyzes current storage usage and recommends AWS storage services
"""

import os
import json
import subprocess
from datetime import datetime
from typing import Dict, List

class StorageAnalyzer:
    def __init__(self):
        self.storage_recommendations = {
            'file_shares': 'Amazon FSx for Windows File Server',
            'backup_data': 'Amazon S3 Glacier',
            'database_files': 'Amazon EBS gp3',
            'archive_data': 'Amazon S3 Glacier Deep Archive',
            'frequently_accessed': 'Amazon EBS gp3',
            'infrequently_accessed': 'Amazon S3 IA'
        }
    
    def analyze_windows_storage(self) -> Dict:
        """Analyze Windows storage usage"""
        try:
            # Get disk usage information
            result = subprocess.run(['wmic', 'logicaldisk', 'get', 'size,freespace,caption'], 
                                  capture_output=True, text=True)
            
            storage_info = []
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        caption = parts[0]
                        free_space = int(parts[1]) if parts[1].isdigit() else 0
                        size = int(parts[2]) if parts[2].isdigit() else 0
                        used_space = size - free_space
                        
                        storage_info.append({
                            'drive': caption,
                            'total_gb': round(size / (1024**3), 2),
                            'used_gb': round(used_space / (1024**3), 2),
                            'free_gb': round(free_space / (1024**3), 2),
                            'usage_percent': round((used_space / size * 100), 2) if size > 0 else 0
                        })
            
            return self._generate_storage_recommendations(storage_info)
            
        except Exception as e:
            print(f"Error analyzing storage: {e}")
            return {}
    
    def _generate_storage_recommendations(self, storage_info: List[Dict]) -> Dict:
        """Generate AWS storage service recommendations"""
        recommendations = []
        total_storage = 0
        total_cost_estimate = 0
        
        for drive in storage_info:
            total_storage += drive['used_gb']
            
            # Determine storage type based on usage patterns
            if drive['usage_percent'] > 80:
                storage_type = 'frequently_accessed'
                aws_service = 'Amazon EBS gp3'
                monthly_cost = drive['used_gb'] * 0.08  # $0.08 per GB for gp3
            elif drive['usage_percent'] < 20:
                storage_type = 'infrequently_accessed'
                aws_service = 'Amazon S3 IA'
                monthly_cost = drive['used_gb'] * 0.0125  # $0.0125 per GB for S3 IA
            else:
                storage_type = 'standard'
                aws_service = 'Amazon EBS gp3'
                monthly_cost = drive['used_gb'] * 0.08
            
            total_cost_estimate += monthly_cost
            
            recommendation = {
                'current_drive': drive['drive'],
                'current_usage_gb': drive['used_gb'],
                'usage_pattern': storage_type,
                'recommended_service': aws_service,
                'estimated_monthly_cost': round(monthly_cost, 2),
                'migration_strategy': self._get_migration_strategy(storage_type)
            }
            recommendations.append(recommendation)
        
        return {
            'analysis_date': datetime.now().isoformat(),
            'total_storage_gb': round(total_storage, 2),
            'total_estimated_monthly_cost': round(total_cost_estimate, 2),
            'recommendations': recommendations,
            'migration_phases': self._create_migration_phases(recommendations)
        }
    
    def _get_migration_strategy(self, storage_type: str) -> str:
        """Get migration strategy based on storage type"""
        strategies = {
            'frequently_accessed': 'Direct migration to EBS with AWS DataSync',
            'infrequently_accessed': 'Migration to S3 with lifecycle policies',
            'standard': 'Hybrid approach with AWS Storage Gateway'
        }
        return strategies.get(storage_type, 'Standard migration approach')
    
    def _create_migration_phases(self, recommendations: List[Dict]) -> List[Dict]:
        """Create phased migration plan"""
        phases = [
            {
                'phase': 1,
                'description': 'Migrate frequently accessed data',
                'duration_weeks': 2,
                'drives': [r for r in recommendations if 'frequently_accessed' in r['usage_pattern']]
            },
            {
                'phase': 2,
                'description': 'Migrate standard usage data',
                'duration_weeks': 4,
                'drives': [r for r in recommendations if r['usage_pattern'] == 'standard']
            },
            {
                'phase': 3,
                'description': 'Archive infrequently accessed data',
                'duration_weeks': 2,
                'drives': [r for r in recommendations if 'infrequently_accessed' in r['usage_pattern']]
            }
        ]
        return phases

# Usage example
if __name__ == "__main__":
    analyzer = StorageAnalyzer()
    results = analyzer.analyze_windows_storage()
    
    # Save results
    with open("storage_analysis.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("Storage Analysis Results:")
    print(f"Total Storage: {results.get('total_storage_gb', 0)} GB")
    print(f"Estimated Monthly Cost: ${results.get('total_estimated_monthly_cost', 0)}")
    print(f"Migration Phases: {len(results.get('migration_phases', []))}")
```
