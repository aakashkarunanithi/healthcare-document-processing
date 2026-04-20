import boto3
from settings import config
from botocore.client import BaseClient

class AWSService:
    def get_client(service: str) -> BaseClient:
        return boto3.client(service,region_name=config.aws_region)
    s3_client=get_client("s3")
    bda_client=get_client("bedrock-data-automation")
    bda_runtime_client=get_client("bedrock-data-automation-runtime")

aws_service=AWSService()
