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
    
        object_key = event["Payload"]["chunk_key"]
        original_key = event["Payload"]["original_key"] 
        get_url = event["Payload"]["get_url"]   
        
        object_key = urllib.parse.unquote(object_key)
        logger.info(f"key: {object_key}")
        apiClient.convert_pdf_to_html(object_key, original_key, get_url)
        return response_object(200, {"object_key": object_key, "original_key": original_key})
            
    except Exception as e:
        logger.error(e)
        return response_object(500, str(e))   