import argparse
from typing import Union

import boto3
from botocore.exceptions import ClientError

BUCKET_NAME: str = "mh.cloudformation.templates"
STACK_PREFIX: str = "MondayHealth"
FILE_NAME: str = "vpc.yaml"
NOTIF_ARN: str = "CFChanges"


def s3_path_for_template(name: str) -> str:
    return "https://s3.amazonaws.com/" + BUCKET_NAME + "/" + name


def get_update_arn() -> Union[None, str]:
    cf = boto3.client("sns")
    """ :type : pyboto3.sns """
    results = cf.list_topics()
    for result in results['Topics']:
        arn = result['TopicArn']
        if arn.split(":")[-1] == NOTIF_ARN:
            return arn
    return None


def validate_template(name: str) -> bool:
    cf = boto3.client('cloudformation')
    """ :type : pyboto3.cloudformation """
    with open(name, 'rb') as data:
        encoded = data.read().decode()

    try:
        cf.validate_template(TemplateBody=encoded)
    except ClientError as v:
        print(v)
        return False

    return True


def store_file(filename: str) -> None:
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(BUCKET_NAME)
    with open(filename, 'rb') as data:
        bucket.put_object(Key=filename, Body=data)


def stack_exists(name: str) -> bool:
    cf = boto3.client('cloudformation')
    """ :type : pyboto3.cloudformation """
    results = cf.list_stacks()
    for result in results['StackSummaries']:
        if name == result['StackName']:
            if result['StackStatus'] == 'DELETE_COMPLETE':
                # Entries for deleted stacks hang around in results even though
                # they are not visible in the console.
                return False
            return True
    return False


def update_stack(stack_name: str, template_name: str) -> None:
    cf = boto3.client('cloudformation')
    """ :type : pyboto3.cloudformation """
    t_name = s3_path_for_template(template_name)
    # arn = get_update_arn()
    cf.update_stack(StackName=stack_name, TemplateURL=t_name)


def create_stack(stack_name: str, template_name: str) -> None:
    cf = boto3.client('cloudformation')
    """ :type : pyboto3.cloudformation """
    t_path = s3_path_for_template(template_name)
    cf.create_stack(StackName=stack_name, TemplateURL=t_path)


def add_or_update_template(file_name: str) -> None:
    if not validate_template(file_name):
        print("Invalid template: stopping.")
        return

    stack = STACK_PREFIX + file_name.split(".")[0].upper()
    print("Updating", stack, "with configuration", file_name)

    store_file(file_name)
    if not stack_exists(stack):
        print("Stack does not exist, creating...")
        create_stack(stack, file_name)
    else:
        print("Stack exists, updating...")
        update_stack(stack, file_name)


def run_from_command_line() -> None:
    parser = argparse.ArgumentParser(description="Update a named CF template.")
    parser.add_argument('name', metavar='name', type=str,
                        help='The name of the file before the extension.')
    args = parser.parse_args()
    add_or_update_template(args.name + ".yaml")


if __name__ == "__main__":
    run_from_command_line()
