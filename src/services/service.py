from utils.exceptions.custom_app_exception import Custom_App_Exception
from utils.exceptions.error_codes import ErrorCode
from utils.exceptions.http_status import HttpStatusCode
from utils.wait_for_job import wait_job
from utils.fetch_and_display_result import fetch_display_result
from utils.invoke_bda import bda_invoke
from settings import config
from typing import Dict, Any
from models.uri_input import UriInput
from utils.logger import logger

class HealthCareService:

    async def invoice_process_service(self, request: UriInput) -> Dict[str, Any]:
        logger.info("Starting invoice process service")
        try:
            invocation_arn=bda_invoke.invoke_bda_job(config.project_arn,request)
            wait_job.wait_for_job(invocation_arn)
            result=fetch_display_result.fetch_and_display_results(invocation_arn)
            return result
        except Custom_App_Exception:
            raise
        except Exception as e:
            raise Custom_App_Exception(
                message=f"Unexpected service error: {str(e)}",
                code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
            )
        
service=HealthCareService()