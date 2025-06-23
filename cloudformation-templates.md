# CloudFormation Templates for AWS Programs

## 1. Windows Server Migration Template

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Windows Server Migration Template for MAP/OLA Programs'

Parameters:
  InstanceType:
    Type: String
    Default: t3.medium
    AllowedValues: [t3.small, t3.medium, t3.large, m5.large, m5.xlarge, m5.2xlarge]
    Description: EC2 instance type for Windows Server
  
  KeyPairName:
    Type: AWS::EC2::KeyPair::KeyName
    Description: EC2 Key Pair for Windows Server access
  
  VpcId:
    Type: AWS::EC2::VPC::Id
    Description: VPC ID where the instance will be launched
  
  SubnetId:
    Type: AWS::EC2::Subnet::Id
    Description: Subnet ID for the Windows Server
  
  WindowsVersion:
    Type: String
    Default: Windows_Server-2022-English-Full-Base
    AllowedValues: 
      - Windows_Server-2019-English-Full-Base
      - Windows_Server-2022-English-Full-Base
    Description: Windows Server AMI version

Resources:
  WindowsServerSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for Windows Server migration
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 3389
          ToPort: 3389
          CidrIp: 10.0.0.0/8
          Description: RDP access from internal network
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 10.0.0.0/8
          Description: HTTP access
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 10.0.0.0/8
          Description: HTTPS access
        - IpProtocol: icmp
          FromPort: -1
          ToPort: -1
          CidrIp: 10.0.0.0/8
          Description: ICMP for network diagnostics
      Tags:
        - Key: Name
          Value: WindowsServer-SG
        - Key: Purpose
          Value: Migration

  WindowsServerRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
        - arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy
      Tags:
        - Key: Purpose
          Value: WindowsServerMigration

  WindowsServerInstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Roles:
        - !Ref WindowsServerRole

  WindowsServerInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !Sub '{{resolve:ssm:/aws/service/ami-windows-latest/${WindowsVersion}}}'
      InstanceType: !Ref InstanceType
      KeyName: !Ref KeyPairName
      SubnetId: !Ref SubnetId
      SecurityGroupIds:
        - !Ref WindowsServerSecurityGroup
      IamInstanceProfile: !Ref WindowsServerInstanceProfile
      UserData:
        Fn::Base64: !Sub |
          <powershell>
          # Install CloudWatch Agent
          Invoke-WebRequest -Uri "https://s3.amazonaws.com/amazoncloudwatch-agent/windows/amd64/latest/amazon-cloudwatch-agent.msi" -OutFile "C:\amazon-cloudwatch-agent.msi"
          Start-Process msiexec.exe -ArgumentList '/i C:\amazon-cloudwatch-agent.msi /quiet' -Wait
          
          # Configure CloudWatch Agent
          $config = @{
            "metrics" = @{
              "namespace" = "CWAgent"
              "metrics_collected" = @{
                "cpu" = @{
                  "measurement" = @("cpu_usage_idle", "cpu_usage_iowait", "cpu_usage_user", "cpu_usage_system")
                  "metrics_collection_interval" = 60
                }
                "disk" = @{
                  "measurement" = @("used_percent")
                  "metrics_collection_interval" = 60
                  "resources" = @("*")
                }
                "mem" = @{
                  "measurement" = @("mem_used_percent")
                  "metrics_collection_interval" = 60
                }
              }
            }
          }
          
          $config | ConvertTo-Json -Depth 10 | Out-File -FilePath "C:\Program Files\Amazon\AmazonCloudWatchAgent\config.json"
          
          # Start CloudWatch Agent
          & "C:\Program Files\Amazon\AmazonCloudWatchAgent\amazon-cloudwatch-agent-ctl.ps1" -a fetch-config -m ec2 -c file:"C:\Program Files\Amazon\AmazonCloudWatchAgent\config.json" -s
          
          # Install additional migration tools
          # Chocolatey for package management
          Set-ExecutionPolicy Bypass -Scope Process -Force
          [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
          iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
          
          # Install useful tools
          choco install -y 7zip
          choco install -y notepadplusplus
          choco install -y googlechrome
          
          # Signal completion
          cfn-signal.exe -e 0 --stack ${AWS::StackName} --resource WindowsServerInstance --region ${AWS::Region}
          </powershell>
      Tags:
        - Key: Name
          Value: WindowsServer-Migration
        - Key: Purpose
          Value: MAP-Migration
        - Key: Environment
          Value: Migration
    CreationPolicy:
      ResourceSignal:
        Count: 1
        Timeout: PT15M

  DataVolume:
    Type: AWS::EC2::Volume
    Properties:
      Size: 100
      VolumeType: gp3
      Iops: 3000
      Throughput: 125
      AvailabilityZone: !GetAtt WindowsServerInstance.AvailabilityZone
      Tags:
        - Key: Name
          Value: WindowsServer-DataVolume
        - Key: Purpose
          Value: Migration

  DataVolumeAttachment:
    Type: AWS::EC2::VolumeAttachment
    Properties:
      Device: xvdf
      InstanceId: !Ref WindowsServerInstance
      VolumeId: !Ref DataVolume

Outputs:
  InstanceId:
    Description: Instance ID of the Windows Server
    Value: !Ref WindowsServerInstance
    Export:
      Name: !Sub '${AWS::StackName}-InstanceId'
  
  PrivateIP:
    Description: Private IP address of the Windows Server
    Value: !GetAtt WindowsServerInstance.PrivateIp
    Export:
      Name: !Sub '${AWS::StackName}-PrivateIP'
  
  SecurityGroupId:
    Description: Security Group ID for the Windows Server
    Value: !Ref WindowsServerSecurityGroup
    Export:
      Name: !Sub '${AWS::StackName}-SecurityGroupId'
```

## 2. FSx for Windows File Server Template

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Amazon FSx for Windows File Server for storage migration'

Parameters:
  VpcId:
    Type: AWS::EC2::VPC::Id
    Description: VPC ID for FSx file system
  
  SubnetIds:
    Type: List<AWS::EC2::Subnet::Id>
    Description: Subnet IDs for FSx file system (minimum 2 for Multi-AZ)
  
  StorageCapacity:
    Type: Number
    Default: 1024
    MinValue: 32
    MaxValue: 65536
    Description: Storage capacity in GB
  
  ThroughputCapacity:
    Type: Number
    Default: 16
    AllowedValues: [8, 16, 32, 64, 128, 256, 512, 1024, 2048]
    Description: Throughput capacity in MB/s
  
  ActiveDirectoryId:
    Type: String
    Description: AWS Managed Microsoft AD directory ID
  
  BackupRetentionPeriod:
    Type: Number
    Default: 7
    MinValue: 0
    MaxValue: 90
    Description: Backup retention period in days

Resources:
  FSxSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for FSx Windows File Server
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 445
          ToPort: 445
          CidrIp: 10.0.0.0/8
          Description: SMB/CIFS access
        - IpProtocol: tcp
          FromPort: 135
          ToPort: 135
          CidrIp: 10.0.0.0/8
          Description: RPC endpoint mapper
        - IpProtocol: tcp
          FromPort: 1024
          ToPort: 65535
          CidrIp: 10.0.0.0/8
          Description: Dynamic RPC ports
      Tags:
        - Key: Name
          Value: FSx-WindowsFileServer-SG

  WindowsFileSystem:
    Type: AWS::FSx::FileSystem
    Properties:
      FileSystemType: WINDOWS
      StorageCapacity: !Ref StorageCapacity
      SubnetIds: !Ref SubnetIds
      SecurityGroupIds:
        - !Ref FSxSecurityGroup
      WindowsConfiguration:
        ActiveDirectoryId: !Ref ActiveDirectoryId
        ThroughputCapacity: !Ref ThroughputCapacity
        AutomaticBackupRetentionDays: !Ref BackupRetentionPeriod
        DailyAutomaticBackupStartTime: "02:00"
        WeeklyMaintenanceStartTime: "7:02:00"
        DeploymentType: MULTI_AZ_1
        PreferredSubnetId: !Select [0, !Ref SubnetIds]
      Tags:
        - Key: Name
          Value: WindowsFileServer-Migration
        - Key: Purpose
          Value: StorageMigration

  BackupVault:
    Type: AWS::Backup::BackupVault
    Properties:
      BackupVaultName: FSx-WindowsFileServer-Backup
      EncryptionKeyArn: !Sub 'arn:aws:kms:${AWS::Region}:${AWS::AccountId}:alias/aws/backup'

  BackupPlan:
    Type: AWS::Backup::BackupPlan
    Properties:
      BackupPlan:
        BackupPlanName: FSx-WindowsFileServer-BackupPlan
        BackupPlanRule:
          - RuleName: DailyBackups
            TargetBackupVault: !Ref BackupVault
            ScheduleExpression: cron(0 2 ? * * *)
            StartWindowMinutes: 60
            CompletionWindowMinutes: 120
            Lifecycle:
              MoveToColdStorageAfterDays: 30
              DeleteAfterDays: 365

  BackupSelection:
    Type: AWS::Backup::BackupSelection
    Properties:
      BackupPlanId: !Ref BackupPlan
      BackupSelection:
        SelectionName: FSx-WindowsFileServer-Selection
        IamRoleArn: !Sub 'arn:aws:iam::${AWS::AccountId}:role/service-role/AWSBackupDefaultServiceRole'
        Resources:
          - !GetAtt WindowsFileSystem.ResourceARN

Outputs:
  FileSystemId:
    Description: FSx Windows File System ID
    Value: !Ref WindowsFileSystem
    Export:
      Name: !Sub '${AWS::StackName}-FileSystemId'
  
  DNSName:
    Description: FSx Windows File System DNS Name
    Value: !GetAtt WindowsFileSystem.DNSName
    Export:
      Name: !Sub '${AWS::StackName}-DNSName'
  
  SecurityGroupId:
    Description: Security Group ID for FSx
    Value: !Ref FSxSecurityGroup
    Export:
      Name: !Sub '${AWS::StackName}-SecurityGroupId'
```

## 3. AWS Managed Microsoft AD Template

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'AWS Managed Microsoft AD for Windows Server migration'

Parameters:
  VpcId:
    Type: AWS::EC2::VPC::Id
    Description: VPC ID for the directory
  
  SubnetIds:
    Type: List<AWS::EC2::Subnet::Id>
    Description: Subnet IDs for the directory (must be in different AZs)
  
  DomainName:
    Type: String
    Default: corp.example.com
    Description: Fully qualified domain name
  
  NetBiosName:
    Type: String
    Default: CORP
    Description: NetBIOS name for the domain
  
  AdminPassword:
    Type: String
    NoEcho: true
    MinLength: 8
    MaxLength: 64
    Description: Password for the default administrative user

Resources:
  ManagedAD:
    Type: AWS::DirectoryService::MicrosoftAD
    Properties:
      Name: !Ref DomainName
      Password: !Ref AdminPassword
      ShortName: !Ref NetBiosName
      VpcSettings:
        VpcId: !Ref VpcId
        SubnetIds: !Ref SubnetIds
      Edition: Standard

  DHCPOptions:
    Type: AWS::EC2::DHCPOptions
    Properties:
      DomainName: !Ref DomainName
      DomainNameServers: !GetAtt ManagedAD.DnsIpAddresses
      Tags:
        - Key: Name
          Value: ManagedAD-DHCP-Options

  DHCPOptionsAssociation:
    Type: AWS::EC2::VPCDHCPOptionsAssociation
    Properties:
      VpcId: !Ref VpcId
      DhcpOptionsId: !Ref DHCPOptions

Outputs:
  DirectoryId:
    Description: Directory ID of the AWS Managed Microsoft AD
    Value: !Ref ManagedAD
    Export:
      Name: !Sub '${AWS::StackName}-DirectoryId'
  
  DnsIpAddresses:
    Description: DNS IP addresses of the directory
    Value: !Join [',', !GetAtt ManagedAD.DnsIpAddresses]
    Export:
      Name: !Sub '${AWS::StackName}-DnsIpAddresses'
  
  DomainName:
    Description: Domain name
    Value: !Ref DomainName
    Export:
      Name: !Sub '${AWS::StackName}-DomainName'
```
