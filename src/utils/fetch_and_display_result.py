from utils.logger import logger
from settings import config
import json
from typing import Dict, Any
from utils.aws_client import aws_service

class FetchAndDisplayResult:   
    def fetch_s3_content(self,s3_uri: str) -> Dict[str, Any]:
        """Fetch and parse a JSON file from S3 given its full s3:// URI.

        Args:
            s3_uri: Full S3 path, e.g. s3://bucket-name/path/to/file.json

        Returns:
            Parsed JSON content as a Python dict.
        """
        s3_key = s3_uri.replace(f"s3://{config.s3_bucket}/", "")
        logger.info(f"Fetching S3 object")

        obj = aws_service.s3_client.get_object(Bucket=config.s3_bucket, Key=s3_key)
        content = json.loads(obj["Body"].read())
        return content
 
    def fetch_and_display_results(self,invocation_arn: str) -> Dict[str, Any]:
        """Fetch and display both standard and custom outputs directly from S3"""
        logger.info("Fetching results from S3...")

        # Get the S3 location of the output metadata file
        status_response = aws_service.bda_runtime_client.get_data_automation_status(
            invocationArn=invocation_arn
        )
        job_metadata_uri = status_response["outputConfiguration"]["s3Uri"]

        # Download and parse the job metadata
        metadata = self.fetch_s3_content(job_metadata_uri)

        print("\n" + "=" * 80)
        print("BDA EXTRACTION RESULTS")
        print("=" * 80)
        print(f"\nJob ID: {metadata['job_id']}")
        print(f"Status: {metadata['job_status']}")

        # Iterate over segments (one per logical document in the file)
        for segment_idx, segment in enumerate(
            metadata["output_metadata"][0]["segment_metadata"]
        ):
            print(f"\n{'─' * 80}")
            print(f"SEGMENT {segment_idx}")
            print(f"{'─' * 80}")

            # ── Standard Output ──────────────────────────────────────────
            if "standard_output_path" in segment:
                standard_output = self.fetch_s3_content(segment["standard_output_path"])
                print("\n[STANDARD OUTPUT]")
                print(json.dumps(standard_output, indent=2))

            # ── Custom Output ────────────────────────────────────────────
            if "custom_output_path" in segment:
                custom_output = self.fetch_s3_content(segment["custom_output_path"])

                print("\n[CUSTOM OUTPUT - Blueprint Extraction]")
                print(f"Blueprint : {custom_output.get('matched_blueprint', {}).get('name', 'N/A')}")
                print(f"Confidence: {custom_output.get('matched_blueprint', {}).get('confidence', 'N/A')}")
                print(f"Status    : {segment.get('custom_output_status', 'N/A')}")
                print("\nExtracted Fields:")
                print(json.dumps(custom_output.get("inference_result", {}), indent=2))
                return custom_output.get("inference_result", {})
            else:
                print("\n[CUSTOM OUTPUT]")
                print(f"Status: {segment.get('custom_output_status', 'NO_MATCH')}")
                print("No custom output generated for this segment")


fetch_display_result=FetchAndDisplayResult()
