# Quick Reference Guide

## File Structure
```
amazon-q-aws-programs/
├── README.md                           # Main overview and navigation guide
├── SOLUTION-OVERVIEW.md                # 🎯 START HERE - Complete solution explanation
├── QUICK-REFERENCE.md                  # This file - quick commands and tips
├── amazon-q-aws-programs-guide.md     # Comprehensive program guide
├── deployment-guide.md                 # Step-by-step deployment instructions
├── q-repeatable-tools.md              # Assessment and analysis tools
├── automation-scripts.md              # Deployment and optimization scripts
└── cloudformation-templates.md        # Infrastructure templates
```

## 🚀 First Time Users
**Read `SOLUTION-OVERVIEW.md` first** to understand:
- What this solution does (and doesn't do)
- Required inputs and data formats
- Key assumptions and limitations
- Expected business outcomes

## Quick Commands

### Assessment Tools
```bash
# Server inventory analysis
python3 server_inventory_analyzer.py server_inventory.csv

# Windows license assessment
powershell .\windows_license_assessment.ps1 -OutputPath ".\license_assessment.csv"

# Storage analysis
python3 storage_analyzer.py
```

### Infrastructure Deployment
```bash
# Deploy VPC
aws cloudformation deploy --template-file vpc-template.yaml --stack-name migration-vpc

# Deploy Windows Server
aws cloudformation deploy --template-file windows-server-template.yaml --stack-name migration-windows-server --capabilities CAPABILITY_IAM

# Deploy FSx
aws cloudformation deploy --template-file fsx-template.yaml --stack-name migration-fsx
```

### Automation
```bash
# Full migration setup
./migration_orchestration.sh

# Cost optimization analysis
python3 cost_optimizer.py --region us-east-1 --output cost_report.json --csv cost_report.csv
```

## Amazon Q Integration Tips

### Best Prompts for Tool Customization
- "Modify [tool name] to include [specific requirement]"
- "Create a [language] script for [specific assessment]"
- "Help me troubleshoot this error: [error message]"
- "Optimize this script for [specific scenario]"

### Common Q Use Cases
1. **Tool Modification**: Adapt existing tools for specific customer needs
2. **Error Resolution**: Troubleshoot deployment and execution issues
3. **Feature Addition**: Add new capabilities to existing tools
4. **Documentation**: Generate customer-specific reports and guides
5. **Optimization**: Improve performance and cost efficiency

## Program-Specific Quick Start

### MAP (Migration Acceleration Program)
1. Run server inventory analysis
2. Deploy VPC infrastructure
3. Execute migration orchestration
4. Generate migration reports

### OLA (Optimization and Licensing Assessment)
1. Run Windows license assessment
2. Execute cost optimization analysis
3. Generate business case reports
4. Plan optimization implementation

### ONE OLA (Windows Server and Storage)
1. Focus on Windows-specific tools
2. Deploy FSx for file servers
3. Implement AD integration
4. Optimize storage configurations

## Common File Locations
- **Tools Output**: Current directory (unless specified otherwise)
- **CloudFormation Templates**: Extract from .md files to .yaml files
- **Reports**: JSON and CSV formats in current directory
- **Logs**: Check CloudFormation console and CloudWatch

## Prerequisites Checklist
- [ ] AWS CLI v2.x installed and configured
- [ ] Python 3.8+ with required packages (pandas, boto3)
- [ ] PowerShell 5.1+ (for Windows tools)
- [ ] Appropriate AWS IAM permissions
- [ ] AWS account with sufficient service limits

## Emergency Troubleshooting
1. **Permission Issues**: Check IAM policies and CloudTrail logs
2. **API Rate Limits**: Implement retry logic and exponential backoff
3. **Resource Limits**: Check AWS service quotas
4. **Template Errors**: Validate CloudFormation syntax
5. **Script Failures**: Check Python/PowerShell versions and dependencies

## Quick Amazon Q Prompts
```
"Help me set up the prerequisites for these AWS migration tools"
"My CloudFormation deployment failed, here's the error: [paste error]"
"Create a monitoring dashboard for these migration tools"
"Generate a customer presentation from these assessment results"
"Optimize this tool for a customer with 1000+ servers"
```
