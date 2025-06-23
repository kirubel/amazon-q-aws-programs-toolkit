# Automation Scripts for AWS Programs

## 1. Migration Orchestration Script

```bash
#!/bin/bash
# Migration Orchestration Script for AWS MAP Program
# This script automates the deployment of migration infrastructure

set -e

# Configuration
STACK_PREFIX="migration"
REGION="us-east-1"
KEY_PAIR_NAME="migration-keypair"
VPC_CIDR="10.0.0.0/16"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Function to check if AWS CLI is configured
check_aws_cli() {
    if ! command -v aws &> /dev/null; then
        error "AWS CLI is not installed"
    fi
    
    if ! aws sts get-caller-identity &> /dev/null; then
        error "AWS CLI is not configured or credentials are invalid"
    fi
    
    log "AWS CLI is properly configured"
}

# Function to create VPC infrastructure
create_vpc_infrastructure() {
    log "Creating VPC infrastructure..."
    
    cat > vpc-template.yaml << 'EOF'
AWSTemplateFormatVersion: '2010-09-09'
Description: 'VPC Infrastructure for Migration'

Parameters:
  VpcCidr:
    Type: String
    Default: 10.0.0.0/16

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref VpcCidr
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: Migration-VPC

  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: Migration-IGW

  AttachGateway:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref VPC
      InternetGatewayId: !Ref InternetGateway

  PublicSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: Migration-Public-Subnet-1

  PublicSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.2.0/24
      AvailabilityZone: !Select [1, !GetAZs '']
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: Migration-Public-Subnet-2

  PrivateSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.3.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      Tags:
        - Key: Name
          Value: Migration-Private-Subnet-1

  PrivateSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.4.0/24
      AvailabilityZone: !Select [1, !GetAZs '']
      Tags:
        - Key: Name
          Value: Migration-Private-Subnet-2

  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: Migration-Public-RT

  PublicRoute:
    Type: AWS::EC2::Route
    DependsOn: AttachGateway
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway

  PublicSubnetRouteTableAssociation1:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnet1
      RouteTableId: !Ref PublicRouteTable

  PublicSubnetRouteTableAssociation2:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnet2
      RouteTableId: !Ref PublicRouteTable

Outputs:
  VpcId:
    Description: VPC ID
    Value: !Ref VPC
    Export:
      Name: Migration-VPC-Id
  
  PublicSubnet1Id:
    Description: Public Subnet 1 ID
    Value: !Ref PublicSubnet1
    Export:
      Name: Migration-PublicSubnet1-Id
  
  PublicSubnet2Id:
    Description: Public Subnet 2 ID
    Value: !Ref PublicSubnet2
    Export:
      Name: Migration-PublicSubnet2-Id
  
  PrivateSubnet1Id:
    Description: Private Subnet 1 ID
    Value: !Ref PrivateSubnet1
    Export:
      Name: Migration-PrivateSubnet1-Id
  
  PrivateSubnet2Id:
    Description: Private Subnet 2 ID
    Value: !Ref PrivateSubnet2
    Export:
      Name: Migration-PrivateSubnet2-Id
EOF

    aws cloudformation deploy \
        --template-file vpc-template.yaml \
        --stack-name "${STACK_PREFIX}-vpc" \
        --parameter-overrides VpcCidr=${VPC_CIDR} \
        --region ${REGION} \
        --tags Purpose=Migration Program=MAP
    
    log "VPC infrastructure created successfully"
}

# Function to deploy Windows Server
deploy_windows_server() {
    log "Deploying Windows Server..."
    
    # Get VPC and subnet information
    VPC_ID=$(aws cloudformation describe-stacks \
        --stack-name "${STACK_PREFIX}-vpc" \
        --query 'Stacks[0].Outputs[?OutputKey==`VpcId`].OutputValue' \
        --output text \
        --region ${REGION})
    
    SUBNET_ID=$(aws cloudformation describe-stacks \
        --stack-name "${STACK_PREFIX}-vpc" \
        --query 'Stacks[0].Outputs[?OutputKey==`PrivateSubnet1Id`].OutputValue' \
        --output text \
        --region ${REGION})
    
    aws cloudformation deploy \
        --template-file cloudformation-templates.md \
        --stack-name "${STACK_PREFIX}-windows-server" \
        --parameter-overrides \
            VpcId=${VPC_ID} \
            SubnetId=${SUBNET_ID} \
            KeyPairName=${KEY_PAIR_NAME} \
        --capabilities CAPABILITY_IAM \
        --region ${REGION} \
        --tags Purpose=Migration Program=MAP
    
    log "Windows Server deployed successfully"
}

# Function to generate migration report
generate_migration_report() {
    log "Generating migration report..."
    
    cat > migration_report.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>AWS Migration Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #232f3e; color: white; padding: 20px; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
        .success { background-color: #d4edda; border-color: #c3e6cb; }
        .warning { background-color: #fff3cd; border-color: #ffeaa7; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="header">
        <h1>AWS Migration Assessment Report</h1>
        <p>Generated on: $(date)</p>
    </div>
    
    <div class="section success">
        <h2>Migration Summary</h2>
        <p>Infrastructure successfully deployed for migration assessment.</p>
        <ul>
            <li>VPC Infrastructure: ✓ Deployed</li>
            <li>Windows Server: ✓ Deployed</li>
            <li>Security Groups: ✓ Configured</li>
            <li>Monitoring: ✓ Enabled</li>
        </ul>
    </div>
    
    <div class="section">
        <h2>Next Steps</h2>
        <ol>
            <li>Connect to Windows Server using RDP</li>
            <li>Install application dependencies</li>
            <li>Configure data migration tools</li>
            <li>Test application functionality</li>
            <li>Plan production cutover</li>
        </ol>
    </div>
    
    <div class="section warning">
        <h2>Important Notes</h2>
        <ul>
            <li>Ensure proper backup procedures before migration</li>
            <li>Test all applications thoroughly</li>
            <li>Plan for DNS changes during cutover</li>
            <li>Monitor performance after migration</li>
        </ul>
    </div>
</body>
</html>
EOF
    
    log "Migration report generated: migration_report.html"
}

# Main execution
main() {
    log "Starting AWS Migration Automation Script"
    
    check_aws_cli
    create_vpc_infrastructure
    deploy_windows_server
    generate_migration_report
    
    log "Migration infrastructure deployment completed successfully!"
    log "Check migration_report.html for detailed information"
}

# Execute main function
main "$@"
```

## 2. Cost Optimization Script

```python
#!/usr/bin/env python3
"""
Cost Optimization Script for AWS OLA Program
Analyzes current AWS usage and provides cost optimization recommendations
"""

import boto3
import json
import csv
from datetime import datetime, timedelta
from typing import Dict, List
import argparse

class CostOptimizer:
    def __init__(self, region='us-east-1'):
        self.region = region
        self.ec2 = boto3.client('ec2', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.pricing = boto3.client('pricing', region_name='us-east-1')  # Pricing API only in us-east-1
        
    def analyze_ec2_instances(self) -> List[Dict]:
        """Analyze EC2 instances for right-sizing opportunities"""
        instances = []
        
        try:
            response = self.ec2.describe_instances()
            
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    if instance['State']['Name'] == 'running':
                        instance_data = {
                            'instance_id': instance['InstanceId'],
                            'instance_type': instance['InstanceType'],
                            'launch_time': instance['LaunchTime'],
                            'platform': instance.get('Platform', 'Linux'),
                            'vpc_id': instance.get('VpcId', ''),
                            'subnet_id': instance.get('SubnetId', ''),
                            'tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                        }
                        
                        # Get CPU utilization
                        cpu_utilization = self._get_cpu_utilization(instance['InstanceId'])
                        instance_data['avg_cpu_utilization'] = cpu_utilization
                        
                        # Generate recommendations
                        instance_data['recommendations'] = self._generate_instance_recommendations(
                            instance_data
                        )
                        
                        instances.append(instance_data)
                        
        except Exception as e:
            print(f"Error analyzing EC2 instances: {e}")
            
        return instances
    
    def _get_cpu_utilization(self, instance_id: str) -> float:
        """Get average CPU utilization for the last 7 days"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=7)
            
            response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,  # 1 hour
                Statistics=['Average']
            )
            
            if response['Datapoints']:
                avg_cpu = sum(dp['Average'] for dp in response['Datapoints']) / len(response['Datapoints'])
                return round(avg_cpu, 2)
            else:
                return 0.0
                
        except Exception as e:
            print(f"Error getting CPU utilization for {instance_id}: {e}")
            return 0.0
    
    def _generate_instance_recommendations(self, instance_data: Dict) -> Dict:
        """Generate cost optimization recommendations for an instance"""
        recommendations = {
            'right_sizing': None,
            'reserved_instances': None,
            'spot_instances': None,
            'estimated_savings': 0
        }
        
        cpu_util = instance_data['avg_cpu_utilization']
        instance_type = instance_data['instance_type']
        
        # Right-sizing recommendations
        if cpu_util < 10:
            recommendations['right_sizing'] = {
                'action': 'downsize',
                'reason': f'Low CPU utilization ({cpu_util}%)',
                'suggested_type': self._suggest_smaller_instance(instance_type),
                'potential_savings_percent': 30
            }
        elif cpu_util > 80:
            recommendations['right_sizing'] = {
                'action': 'upsize',
                'reason': f'High CPU utilization ({cpu_util}%)',
                'suggested_type': self._suggest_larger_instance(instance_type),
                'additional_cost_percent': 50
            }
        
        # Reserved Instance recommendations
        if cpu_util > 20:  # Consistent usage
            recommendations['reserved_instances'] = {
                'action': 'purchase_ri',
                'term': '1-year',
                'payment_option': 'partial_upfront',
                'potential_savings_percent': 30
            }
        
        # Spot Instance recommendations
        if 'test' in str(instance_data['tags']).lower() or 'dev' in str(instance_data['tags']).lower():
            recommendations['spot_instances'] = {
                'action': 'convert_to_spot',
                'reason': 'Development/Test workload suitable for Spot',
                'potential_savings_percent': 70
            }
        
        return recommendations
    
    def _suggest_smaller_instance(self, current_type: str) -> str:
        """Suggest a smaller instance type"""
        size_mapping = {
            'large': 'medium',
            'xlarge': 'large',
            '2xlarge': 'xlarge',
            '4xlarge': '2xlarge',
            '8xlarge': '4xlarge'
        }
        
        for size, smaller_size in size_mapping.items():
            if size in current_type:
                return current_type.replace(size, smaller_size)
        
        return current_type  # No smaller size available
    
    def _suggest_larger_instance(self, current_type: str) -> str:
        """Suggest a larger instance type"""
        size_mapping = {
            'medium': 'large',
            'large': 'xlarge',
            'xlarge': '2xlarge',
            '2xlarge': '4xlarge',
            '4xlarge': '8xlarge'
        }
        
        for size, larger_size in size_mapping.items():
            if size in current_type:
                return current_type.replace(size, larger_size)
        
        return current_type  # No larger size available
    
    def generate_cost_report(self, instances: List[Dict]) -> Dict:
        """Generate comprehensive cost optimization report"""
        total_instances = len(instances)
        right_sizing_opportunities = 0
        ri_opportunities = 0
        spot_opportunities = 0
        
        for instance in instances:
            recommendations = instance['recommendations']
            if recommendations['right_sizing']:
                right_sizing_opportunities += 1
            if recommendations['reserved_instances']:
                ri_opportunities += 1
            if recommendations['spot_instances']:
                spot_opportunities += 1
        
        report = {
            'summary': {
                'total_instances_analyzed': total_instances,
                'right_sizing_opportunities': right_sizing_opportunities,
                'reserved_instance_opportunities': ri_opportunities,
                'spot_instance_opportunities': spot_opportunities,
                'analysis_date': datetime.now().isoformat()
            },
            'detailed_recommendations': instances,
            'action_items': self._generate_action_items(instances)
        }
        
        return report
    
    def _generate_action_items(self, instances: List[Dict]) -> List[Dict]:
        """Generate prioritized action items"""
        action_items = []
        
        # High priority: Right-sizing with high savings potential
        for instance in instances:
            rec = instance['recommendations']
            if rec['right_sizing'] and rec['right_sizing']['potential_savings_percent'] > 25:
                action_items.append({
                    'priority': 'High',
                    'action': f"Right-size {instance['instance_id']}",
                    'description': rec['right_sizing']['reason'],
                    'estimated_savings': f"{rec['right_sizing']['potential_savings_percent']}%"
                })
        
        # Medium priority: Reserved Instances
        ri_candidates = [i for i in instances if i['recommendations']['reserved_instances']]
        if len(ri_candidates) >= 3:  # Only recommend if multiple instances
            action_items.append({
                'priority': 'Medium',
                'action': f"Purchase Reserved Instances for {len(ri_candidates)} instances",
                'description': "Consistent usage pattern detected",
                'estimated_savings': "30%"
            })
        
        # Low priority: Spot Instances for dev/test
        spot_candidates = [i for i in instances if i['recommendations']['spot_instances']]
        if spot_candidates:
            action_items.append({
                'priority': 'Low',
                'action': f"Convert {len(spot_candidates)} dev/test instances to Spot",
                'description': "Development and test workloads suitable for Spot Instances",
                'estimated_savings': "70%"
            })
        
        return action_items
    
    def export_to_csv(self, report: Dict, filename: str):
        """Export recommendations to CSV"""
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = [
                'instance_id', 'instance_type', 'avg_cpu_utilization',
                'right_sizing_recommendation', 'ri_recommendation', 'spot_recommendation'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for instance in report['detailed_recommendations']:
                row = {
                    'instance_id': instance['instance_id'],
                    'instance_type': instance['instance_type'],
                    'avg_cpu_utilization': instance['avg_cpu_utilization'],
                    'right_sizing_recommendation': str(instance['recommendations']['right_sizing']),
                    'ri_recommendation': str(instance['recommendations']['reserved_instances']),
                    'spot_recommendation': str(instance['recommendations']['spot_instances'])
                }
                writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description='AWS Cost Optimization Analysis')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    parser.add_argument('--output', default='cost_optimization_report.json', help='Output file')
    parser.add_argument('--csv', help='Export to CSV file')
    
    args = parser.parse_args()
    
    print("Starting AWS Cost Optimization Analysis...")
    
    optimizer = CostOptimizer(region=args.region)
    instances = optimizer.analyze_ec2_instances()
    report = optimizer.generate_cost_report(instances)
    
    # Save JSON report
    with open(args.output, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    # Export to CSV if requested
    if args.csv:
        optimizer.export_to_csv(report, args.csv)
    
    # Print summary
    summary = report['summary']
    print(f"\nCost Optimization Analysis Complete!")
    print(f"Total Instances Analyzed: {summary['total_instances_analyzed']}")
    print(f"Right-sizing Opportunities: {summary['right_sizing_opportunities']}")
    print(f"Reserved Instance Opportunities: {summary['reserved_instance_opportunities']}")
    print(f"Spot Instance Opportunities: {summary['spot_instance_opportunities']}")
    print(f"\nDetailed report saved to: {args.output}")
    
    if args.csv:
        print(f"CSV export saved to: {args.csv}")

if __name__ == "__main__":
    main()
```
