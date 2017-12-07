from typing import Union

import boto3
from botocore.exceptions import ClientError

BUCKET_NAME: str = "mh.cloudformation.templates"
STACK_NAME: str = "MondayHealthNetworkingDefault"
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
            return True
    return False


def update_stack(stack_name: str, template_name: str) -> None:
    cf = boto3.client('cloudformation')
    """ :type : pyboto3.cloudformation """
    t_name = s3_path_for_template(template_name)
    arn = get_update_arn()
    cf.update_stack(StackName=stack_name, TemplateURL=t_name,
                    NotificationARNs=[arn])


def create_stack(stack_name: str, template_name: str) -> None:
    cf = boto3.client('cloudformation')
    """ :type : pyboto3.cloudformation """
    t_path = s3_path_for_template(template_name)
    cf.create_stack(StackName=stack_name, TemplateURL=t_path)


def do_work() -> None:
    if not validate_template(FILE_NAME):
        print("Invalid template: stopping.")
        return

    store_file(FILE_NAME)
    if not stack_exists(STACK_NAME):
        create_stack(STACK_NAME, FILE_NAME)
    else:
        update_stack(STACK_NAME, FILE_NAME)


if __name__ == "__main__":
    do_work()
