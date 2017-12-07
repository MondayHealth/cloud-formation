CloudFormation yaml and convenience scripts for execution.

### installation
1. install and update xcode and homebrew
1. `brew install python3`
1. `pip3 install boto3`
1. `brew install awscli`
1. create a new IAM access key (delete the pre-created one)
    1. N.B.: DONT close the dialog that shows the secret before you've copied it!
    1. Don't save these codes. If something happens to them, regenerate the key
1. `aws configure` and enter the info from the dialog (us-east2, json is fine.)



