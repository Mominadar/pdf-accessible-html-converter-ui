from services.db.dynamo import DynamoDBClient
from services.object_store.S3Client import S3Client
from utils.logger import Logger

logger = Logger(name="NLLB Logger")
logger = Logger.get_logger()

from utils.helpers import response_object
import urllib.parse


from services.api import ApiService

def lambda_handler(event, context):
    try:
        logger.info(f"event: {event}")
        apiClient = ApiService(db_client=DynamoDBClient(), object_store_client=S3Client())
    
        object_key = event["chunk_key"]
        original_key = event["original_key"]         
        original_key = urllib.parse.unquote(original_key)
        logger.info(f"key: {object_key}, original_file {original_key}")
        apiClient.mark_file_status(original_key, "error", "Processing failed.")
        return response_object(200, {"object_key": object_key, "original_key": original_key})
            
    except Exception as e:
        logger.error(e)
        return response_object(500, str(e))   