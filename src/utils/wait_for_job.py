from utils.logger import logger
from utils.aws_client import aws_service
from typing import Dict, Any
import time

class WaitForJob:    
    def wait_for_job(self,invocation_arn: str, max_attempts: int = 30)-> Dict[str, Any]:
        """Wait for BDA job to complete"""
        logger.info("Waiting for job completion...")

        for attempt in range(max_attempts):
            response = aws_service.bda_runtime_client.get_data_automation_status(
                invocationArn=invocation_arn
            )
            status = response["status"]
            logger.info(f"Job status: {status} (attempt {attempt + 1}/{max_attempts})")

            if status == "Success":
                logger.info("✓ Job completed successfully")
                return response

            if status in ["ClientError", "ServiceError"]:
                error_msg = response.get("errorMessage", str(response))
                raise RuntimeError(f"Job failed: {error_msg}")

            time.sleep(10)

        raise TimeoutError(f"Job did not complete within {max_attempts * 10} seconds")
    
wait_job=WaitForJob()