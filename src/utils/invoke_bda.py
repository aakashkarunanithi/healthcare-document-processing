from utils.logger import logger
from settings import config
from utils.aws_client import aws_service
from models.uri_input import UriInput 



class InvokeBDA:
    def invoke_bda_job(self,project_arn: str,request: UriInput) -> str:
        """Invoke BDA job with project that has custom output configured"""
        logger.info("Submitting BDA job...")

        payload = {
            "inputConfiguration": {
                "s3Uri": request.uri
            },
            "outputConfiguration": {
                "s3Uri": config.output_s3_uri
            },
            "dataAutomationConfiguration": {
                "dataAutomationProjectArn": project_arn,
                "stage": "LIVE"
            },
            "dataAutomationProfileArn": config.profile_arn
        }

        response = aws_service.bda_runtime_client.invoke_data_automation_async(**payload)

        invocation_arn = response["invocationArn"]
        logger.info(f"✓ Job submitted")
        return invocation_arn
    

bda_invoke=InvokeBDA()