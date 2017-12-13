CloudFormation yaml and convenience scripts for execution.

# Setup 
1. install and update xcode and homebrew
1. `brew install python3`
1. `pip3 install boto3`
1. `brew install awscli`
1. create a new IAM access key (delete the pre-created one)
    1. N.B.: DON'T close the dialog that shows the secret before you copy it!
    1. Don't save these codes. If something happens to them, regenerate the key
1. `aws configure` and enter the info from the dialog (us-east2, json is fine.)

# Standards
1. Always have "Name:blah" tag
1. Always add a "Name:" tag to the main route table for the VPC. This is the
catchall route table that exists implicitly for each VPC.
1. Try to modularize the files as much as possible using Outputs and ImportValue

# Contents
## VPC
This file contains a CloudFormation configuration that will create a VPC with
private and public subnets for each of the three AZs in us-east-2. If you wanted
to use this for another Region, you simply need to modify it to apply to the
AZs of the target region. It also creates routes and attaches the public subs
to the 

## Security
To be created after VPC which installs security groups and network ACLs and
attaches them to the subnets in that file.

Basically there are private and public subnets in each region. Public is allowed
to communicate with the outside in both directions. Further there is a DMZ for
bastion nodes. SSH is allowed from DMZ into both types of subnets but only
only out from the DMZ. All subnets only accept SSH from the DMZ subnet.

# Concerns
1. Multi-zone architectures seem complex
    1. Is there a way to do a failover NAT? It needs to be located in one AZ
