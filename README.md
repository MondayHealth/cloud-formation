CloudFormation yaml and convenience scripts for execution.

# Setup 
1. install and update xcode and homebrew
1. `brew install python3`
1. `pip3 install boto3`
1. `brew install awscli`
1. create a new IAM access key (delete the pre-created one)
    1. N.B.: DONT close the dialog that shows the secret before you've copied it!
    1. Don't save these codes. If something happens to them, regenerate the key
1. `aws configure` and enter the info from the dialog (us-east2, json is fine.)

# Standards
1. Always have "Name:blah" tag
1. 

# Contents
## VPC
This file contains a CloudFormation configuration that will create a VPC with
private and public subnets for each of the three AZs in us-east-2. If you wanted
to use this for another Region, you simply need to modify it to apply to the
AZs of the target region. It also creates routes and attaches the public subs
to the 

