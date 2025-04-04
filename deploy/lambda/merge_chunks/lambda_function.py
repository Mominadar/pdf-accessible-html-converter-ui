import io
import json
import ast
import os

from services.api import ApiService
from services.db.dynamo import DynamoDBClient
from services.object_store.S3Client import S3Client
from utils.logger import Logger

BUCKET_NAME = os.environ["TARGET_BUCKET_NAME"]
BUCKET_REGION = os.environ["BUCKET_REGION"]

logger = Logger(name="NLLB Logger")
logger = Logger.get_logger()

db_client = DynamoDBClient()
s3_client = S3Client()

def merge_chunks(chunks): 
    file_id = ast.literal_eval(chunks[0]["body"])["original_key"]
   
    logger.info(f"original file: {file_id}")
    merged_content = "<html><body>\n"

    for chunk in chunks:
        item = ast.literal_eval(chunk["body"])
        key = item["object_key"]
        response = s3_client.get_file(key, BUCKET_NAME)
        merged_content += response.decode("utf-8") + "\n"

    merged_content += "</body></html>"

    bytes = io.BytesIO(merged_content.encode("utf-8"))
    merged_key = file_id.replace(".pdf", ".html")
    s3_client.upload_file(bucket=BUCKET_NAME, filename=merged_key, file=bytes, ContentType="text/html")

    try:
        api_service = ApiService(db_client, s3_client)
        api_service.mark_file_status(file_id, "done") 
    except Exception as e:
        logger.error(e)
        raise Exception("Could not find file config information")
    
    return {"merged_file": f"https://{BUCKET_NAME}.s3.{BUCKET_REGION}.amazonaws.com/{merged_key}"}

def lambda_handler(event, context):
    logger.info(f"event {event}")
    file = merge_chunks(event)
    return {
        'statusCode': 200,
        'body': json.dumps(file)
    }
