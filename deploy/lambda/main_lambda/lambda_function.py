import json
from services.db.dynamo import DynamoDBClient
from services.object_store.S3Client import S3Client
from utils.helpers import response_object
from utils.logger import Logger
from datetime import datetime

logger = Logger(name="PAHTML Logger")
logger = Logger.get_logger()

from services.api import ApiService
            
def lambda_handler(event, context):
    try:
        action = event["queryStringParameters"]["action"]
        if(not action):
            return response_object(500, 'Action is not defined!')
            
        logger.info(f'Action:  {action}')
        
        apiClient = ApiService(DynamoDBClient(), S3Client())
    
        event_body = json.loads(event["body"])
        # event_body = {
        #      "converter":"mistral",
        #      "pdf_url" : "https://pdf-accessible-html-converter.s3.eu-north-1.amazonaws.com/2.pdf"
        # }
        
        if action == "health-check":
            logger.info(f'Checking health')
            return response_object(200, datetime.now().isoformat())
           
        elif action == "convert":
            logger.info(f'Converting')
            if "object_key" not in event_body:
                return response_object(400, "Cannot find file")

            object_key = event_body["object_key"]
            html = apiClient.convert_pdf_to_html(object_key)
            return response_object(200, html)
                
        elif action == "upload-config":
            username = event_body["username"] if "username" in event_body else None
            file_name = event_body["file_name"] if "file_name" in event_body else None
            get_url = event_body["pdf_url"] if "pdf_url" in event_body else None
            converter = event_body["converter"] if "converter" in event_body else None

            if not username or not file_name or not get_url or not converter:
                raise response_object(400, detail="Required information not providied")
            
            res = apiClient.upload_config(username, file_name, get_url, converter)
            return response_object(200, res)
            
        elif action == "get-files":
            username = event_body["username"]
            if(not username):
                return response_object(500, "username is required!")
            files = apiClient.get_file_statuses(username)
            return response_object(200, files)
        
        elif action == "get-file":
            key = event_body["key"]
            if(not key):
                raise response_object(400, detail="key is required!")
            file = apiClient.get_file(key) 
            return response_object(200, file) 
        
        return response_object(500, 'Action is not correct!')       
        
    except Exception as e:
        logger.error(e)
        return response_object(500, str(e))      