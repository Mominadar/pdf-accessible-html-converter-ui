
import json
import os
import boto3

from utils.logger import Logger

BUCKET_NAME = os.environ["SOURCE_BUCKET_NAME"]
LAMBDA_NAME = os.environ["FILE_LAMBDA_NAME"]
LAMBDA_REGION = os.environ["FILE_LAMBDA_REGION"]

logger = Logger(name="Lambda Service")
logger = Logger.get_logger()

class LambdaService:
    def __init__(self):
        self.client = boto3.client("lambda", region_name=LAMBDA_REGION)

    def invoke(self, object_key):
        try:
            body = {
            "Records": [
                {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "awsRegion": "eu-north-1",
                "eventTime": "2024-11-19T09:19:10.123Z",
                "eventName": "ObjectCreated:Put",
                "userIdentity": {
                    "principalId": "AWS:AIDAYS2NU23EMW4WBUB43"
                },
                "requestParameters": {
                    "sourceIPAddress": "39.58.207.226"
                },
                "responseElements": {
                    "x-amz-request-id": "FC8W2JNPY7N503ZW",
                    "x-amz-id-2": "xV5qkbH5zUB1ffer7LHjgONQ4wmznqqCbZGj208m5jpHyBBe7TkUbQmcrZkAED7RR9jyDysFZ9MaseKculh3skxnwXlstPTa"
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "fileupload",
                    "bucket": {
                    "name": BUCKET_NAME,
                    "ownerIdentity": {
                        "principalId": "A1NZFMY2MHAY58"
                    },
                    "arn": f"arn:aws:s3:::{BUCKET_NAME}"
                    },
                    "object": {
                    "key": object_key,
                    "size": 60839,
                    "eTag": "96a042950395d6f9a2acfca42d7657c0",
                    "sequencer": "00673C580E12BD32CE"
                    }
                }
                }
            ]
            }
            payload = json.dumps(body)
            # Invoke the second Lambda asynchronously
            response = self.client.invoke(
                FunctionName=LAMBDA_NAME,  # Replace with your background Lambda name
                InvocationType="Event",  # ASYNC execution
                Payload=payload
            )

            logger.info("✅ Background Lambda triggered:", response)
            return True
        except Exception as e:
            logger.error(f"Error invoking lambda {str(e)}")
            return False
