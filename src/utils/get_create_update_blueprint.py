from utils.logger import logger
from settings import config
from botocore.exceptions import ClientError
import json, time
from utils.aws_client import aws_service


class GetOrCreateAndUpdateBlueprint:  
    def get_or_create_blueprint(self) -> str | None:
        """Create or retrieve existing blueprint for invoice extraction"""

        schema = {
            "class": "IntakeForm",
            "description": "Blueprint for extracting structured data from medical intake form",
            "properties": {
                "patient_name": {
                    "type": "string",
                    "inferenceType": "explicit",
                    "instruction": "Extract the patient name"
                },
                "patient_id": {
                    "type": "string",
                    "inferenceType": "explicit",
                    "instruction": "Extract the patient_id"
                },
                "patient_address": {
                    "type": "string",
                    "inferenceType": "explicit",
                    "instruction": "Extract the patients address completely"
                },
                "patient_phone_number": {
                    "type": "string",
                    "inferenceType": "explicit",
                    "instruction": "Extract the patients phone number"
                },
                "Hospital_name": {
                    "type": "string",
                    "inferenceType": "explicit",
                    "instruction": "Extract the hospital name the patient visited"
                },
                "Reason_for_visit": {
                    "type": "string",
                    "inferenceType": "explicit",
                    "instruction": "Extract the reason the patient visited the hospital"
                },
                "Prescribed_medication": {
                    "type": "string",
                    "inferenceType": "explicit",
                    "instruction": "Extract the medicines prescribed by the doctor"
                }
            }
        }

        try:
            logger.info(f"Creating blueprint '{config.blueprint_name}'...")

            response = aws_service.bda_client.create_blueprint(
                blueprintName=config.blueprint_name,
                type="DOCUMENT",
                blueprintStage="LIVE",
                schema=json.dumps(schema)       # Must be a JSON string, not a dict
            )

            arn = response["blueprint"]["blueprintArn"]
            logger.info(f"✓ Blueprint created")
            return arn

        except ClientError as e:
            code = e.response["Error"]["Code"]

            if code == "ConflictException":
                # Blueprint already exists — fetch its ARN instead of failing
                logger.info(f"Blueprint '{config.blueprint_name}' already exists")
                try:
                    response = aws_service.bda_client.list_blueprints()
                    for bp in response.get("blueprints", []):
                        if bp.get("blueprintName") == config.blueprint_name:
                            arn = bp["blueprintArn"]
                            logger.info(f"✓ Found existing blueprint")
                            return arn
                    logger.warning(f"Could not find blueprint '{config.blueprint_name}'")
                    return None
                except Exception as list_error:
                    logger.warning(f"Error listing blueprints: {list_error}")
                    return None
            else:
                logger.error(f"Error creating blueprint: {e}")
                return None   
    def update_project_with_blueprint(self,project_arn: str, blueprint_arn: str) -> str:
        """Update existing BDA project with custom output configuration"""
        standard_output_config = {
            "document": {
                "extraction": {
                    "granularity": {"types": ["DOCUMENT"]},
                    "boundingBox": {"state": "ENABLED"}
                },
                "generativeField": {"state": "ENABLED"},
                "outputFormat": {
                    "textFormat": {"types": ["MARKDOWN"]},
                    "additionalFileFormat": {"state": "ENABLED"}
                }
            }
        }

        custom_output_config = {
            "blueprints": [
                {
                    "blueprintArn": blueprint_arn,
                    "blueprintStage": "LIVE"
                }
            ]
        }

        try:
            logger.info(f"Updating project with custom output configuration...")

            aws_service.bda_client.update_data_automation_project(
                projectArn=project_arn,
                standardOutputConfiguration=standard_output_config,
                customOutputConfiguration=custom_output_config
            )
            logger.info(f"✓ Project updated with blueprint")

            # Project update is async — poll until COMPLETED
            logger.info("Waiting for project update to complete...")
            max_attempts = 20
            for attempt in range(max_attempts):
                status_response = aws_service.bda_client.get_data_automation_project(
                    projectArn=project_arn
                )
                status = status_response["project"]["status"]
                logger.info(f"Project status: {status} (attempt {attempt + 1}/{max_attempts})")

                if status == "COMPLETED":
                    logger.info("✓ Project is ready")
                    return project_arn
                elif status == "FAILED":
                    raise RuntimeError("Project update failed")

                time.sleep(10)

            raise TimeoutError("Project did not become ready in time")

        except ClientError as e:
            logger.error(f"Error updating project: {e}")
            raise

get_create_update_blueprint=GetOrCreateAndUpdateBlueprint()

