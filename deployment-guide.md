# Deployment Guide for Amazon Q AWS Programs Tools

## Overview
This guide provides step-by-step instructions for deploying and using the Amazon Q tools for AWS MAP, OLA, and ONE OLA programs.

## Prerequisites

### System Requirements
- AWS CLI v2.x installed and configured
- Python 3.8 or higher
- PowerShell 5.1 or higher (for Windows tools)
- Bash shell (for Linux/macOS automation)
- Appropriate AWS IAM permissions

### Required AWS Permissions
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:*",
                "cloudformation:*",
                "iam:*",
                "fsx:*",
                "ds:*",
                "backup:*",
                "cloudwatch:*",
                "pricing:*"
            ],
            "Resource": "*"
        }
    ]
}
```

## Tool Deployment Instructions

### 1. Server Inventory Analysis Tool

**Installation:**
```bash
# Install required Python packages
pip install pandas boto3

# Make the script executable
chmod +x q-repeatable-tools.md
```

**Usage:**
```bash
# Prepare your server inventory CSV with columns:
# Server_Name, CPU_Cores, Memory_GB, Storage_GB, OS, Application_Count, Storage_Type

python3 server_inventory_analyzer.py server_inventory.csv
```

**Expected Output:**
- `migration_recommendations.json` - Detailed recommendations
- Console output with summary statistics

### 2. Windows License Assessment Tool

**Installation:**
```powershell
# Ensure PowerShell execution policy allows script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install Active Directory module if not present
Install-WindowsFeature -Name RSAT-AD-PowerShell
```

**Usage:**
```powershell
# Run the license assessment
.\windows_license_assessment.ps1 -OutputPath ".\license_assessment.csv"
```

**Expected Output:**
- `license_assessment.csv` - Detailed license information
- `license_assessment_summary.txt` - Summary report

### 3. Storage Analysis Tool

**Installation:**
```bash
# Install required packages
pip install pandas matplotlib

# For Windows systems, ensure WMI access is available
```

**Usage:**
```bash
# Run storage analysis
python3 storage_analyzer.py
```

**Expected Output:**
- `storage_analysis.json` - Comprehensive storage recommendations
- Migration phase planning

### 4. CloudFormation Templates Deployment

**VPC Infrastructure:**
```bash
# Deploy VPC infrastructure
aws cloudformation deploy \
    --template-file vpc-template.yaml \
    --stack-name migration-vpc \
    --parameter-overrides VpcCidr=10.0.0.0/16 \
    --region us-east-1
```

**Windows Server:**
```bash
# Deploy Windows Server
aws cloudformation deploy \
    --template-file windows-server-template.yaml \
    --stack-name migration-windows-server \
    --parameter-overrides \
        VpcId=vpc-xxxxxxxxx \
        SubnetId=subnet-xxxxxxxxx \
        KeyPairName=your-keypair \
    --capabilities CAPABILITY_IAM \
    --region us-east-1
```

**FSx for Windows File Server:**
```bash
# Deploy FSx file system
aws cloudformation deploy \
    --template-file fsx-template.yaml \
    --stack-name migration-fsx \
    --parameter-overrides \
        VpcId=vpc-xxxxxxxxx \
        SubnetIds=subnet-xxxxxxxxx,subnet-yyyyyyyyy \
        ActiveDirectoryId=d-xxxxxxxxxx \
    --region us-east-1
```

### 5. Migration Orchestration Script

**Installation:**
```bash
# Make the script executable
chmod +x migration_orchestration.sh

# Ensure AWS CLI is configured
aws configure list
```

**Usage:**
```bash
# Run the complete migration setup
./migration_orchestration.sh
```

**Expected Output:**
- Complete VPC infrastructure
- Windows Server instance
- Security groups and IAM roles
- Migration report HTML file

### 6. Cost Optimization Script

**Installation:**
```bash
# Install required packages
pip install boto3

# Ensure AWS credentials have CloudWatch and Pricing API access
```

**Usage:**
```bash
# Run cost optimization analysis
python3 cost_optimizer.py --region us-east-1 --output cost_report.json --csv cost_report.csv
```

**Expected Output:**
- `cost_report.json` - Detailed cost analysis
- `cost_report.csv` - CSV export for spreadsheet analysis
- Console summary of optimization opportunities

## Integration with Amazon Q

### Using Q for Tool Customization

**Example Q Prompts:**
```
"Modify the server inventory analyzer to include network interface analysis"

"Create a PowerShell script to assess SQL Server licensing for the OLA program"

"Generate a CloudFormation template for AWS Managed Microsoft AD with custom OU structure"

"Help me create a cost optimization dashboard using the analysis data"
```

### Q-Assisted Troubleshooting

**Common Issues and Q Solutions:**

1. **CloudFormation Stack Failures:**
   ```
   q chat "My CloudFormation stack failed with error 'InvalidParameterValue'. Here's the template: [paste template]"
   ```

2. **PowerShell Execution Errors:**
   ```
   q chat "I'm getting 'Access Denied' when running the Windows license assessment script. How do I fix permissions?"
   ```

3. **Python Dependencies:**
   ```
   q chat "Help me create a requirements.txt file for all the Python tools and set up a virtual environment"
   ```

## Best Practices

### Security Considerations
- Use IAM roles instead of access keys where possible
- Implement least privilege access principles
- Enable CloudTrail logging for audit purposes
- Use AWS Secrets Manager for sensitive configuration

### Performance Optimization
- Run analysis tools during off-peak hours
- Use pagination for large datasets
- Implement error handling and retry logic
- Cache results to avoid repeated API calls

### Cost Management
- Use AWS Cost Explorer to monitor tool usage costs
- Implement resource tagging for cost allocation
- Set up billing alerts for unexpected charges
- Clean up temporary resources after analysis

## Monitoring and Maintenance

### CloudWatch Monitoring
```bash
# Create CloudWatch dashboard for migration metrics
aws cloudwatch put-dashboard \
    --dashboard-name "Migration-Monitoring" \
    --dashboard-body file://dashboard-config.json
```

### Automated Reporting
```bash
# Set up scheduled reports using EventBridge
aws events put-rule \
    --name "WeeklyMigrationReport" \
    --schedule-expression "rate(7 days)" \
    --state ENABLED
```

### Tool Updates
- Regularly update AWS CLI and SDKs
- Monitor AWS service updates that may affect tools
- Version control all custom scripts and templates
- Test tools in non-production environments first

## Support and Troubleshooting

### Common Error Scenarios

1. **AWS API Rate Limiting:**
   - Implement exponential backoff
   - Use AWS SDK built-in retry mechanisms
   - Consider using AWS Config for inventory instead of direct API calls

2. **Insufficient Permissions:**
   - Review IAM policies
   - Use AWS IAM Policy Simulator for testing
   - Enable CloudTrail to identify missing permissions

3. **Resource Limits:**
   - Check AWS service quotas
   - Request quota increases if needed
   - Implement resource cleanup procedures

### Getting Help with Amazon Q

**Effective Q Prompts for Support:**
```
"I'm getting this error when running the cost optimization script: [error message]. How do I fix it?"

"Help me optimize this CloudFormation template for better performance and cost"

"Create a monitoring solution for tracking migration progress using the tools we've deployed"

"Generate a comprehensive test plan for validating the migration tools before production use"
```

## Conclusion

These tools provide a comprehensive foundation for AWS migration and optimization programs. Amazon Q can help customize, troubleshoot, and extend these tools based on specific customer requirements and scenarios.

For additional support and customization, leverage Amazon Q's capabilities to:
- Modify existing tools for specific use cases
- Create new automation scripts
- Troubleshoot deployment issues
- Generate documentation and reports
- Optimize performance and costs

Remember to always test tools in non-production environments before using them with customer data or production workloads.
