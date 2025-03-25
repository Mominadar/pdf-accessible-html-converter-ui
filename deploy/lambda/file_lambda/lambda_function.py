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
        event_name = event["Records"][0]["eventName"]
        if(not event_name or "ObjectCreated" not in event_name):
            return response_object(500, 'Action is not defined or valid!')
            
        logger.info(f'Event:  {event_name}')
        
        apiClient = ApiService(db_client=DynamoDBClient(), object_store_client=S3Client())
    
        object_key = event["Records"][0]["s3"]["object"]["key"]   
        object_key = urllib.parse.unquote(object_key)
        logger.info(f"key: {object_key}")
        apiClient.convert_pdf_to_html(object_key)
        return response_object(200, object_key)
            
    except Exception as e:
        logger.error(e)
        return response_object(500, str(e))   