from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass 
class Config:
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    s3_bucket: str
    project_arn: str
    profile_arn: str
    output_s3_uri: str
    blueprint_name: str

def get_config() -> Config:
    return Config(
        aws_region=os.getenv("AWS_REGION", ""),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", ""),
        s3_bucket=os.getenv("S3_BUCKET", ""),
        project_arn=os.getenv("PROJECT_ARN", ""),
        profile_arn=os.getenv("PROFILE_ARN", ""),
        output_s3_uri=os.getenv("OUTPUT_S3_URI", ""),
        blueprint_name=os.getenv("BLUEPRINT_NAME", "")

        
    )

config= get_config()