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
            converter =   event_body["converter"] if "converter" else ""
            if(not converter or converter not in ["agentic", "mistral"]):
                return response_object(400, "Converter not provided. Specify converter as 'mistral' or 'agentic' for conversion")
            
            pdf_path = event_body["pdf_url"] if "pdf_url" else ""
            if(not pdf_path):
                return response_object(400, 'PDF url is not provided')
    
            html =  apiClient.convert_pdf_to_html(converter, pdf_path)
            return response_object(200, html)
                
        # elif action == "get-presigned-url":
        #     logger.info(f'Get presigned urls') 

        #     client_action = event_body["client_action"]
        #     if(not client_action):
        #         return response_object(500, 'Something went wrong!')
                
        #     file_name = event_body["name"]
        #     if(not file_name):
        #         return response_object(500, 'file name is not given!')
                
        #     url =  object_store_client.create_url(file_name, client_action)
        #     return response_object(200, url)
                
        # elif action == "translate-file":
        #     logger.info(f'translating file')

        #     get_url = event_body["get_url"]
        #     put_url = event_body["put_url"]
        #     pdf_scale_down_ratio = event_body["scale"] if "scale" in event_body else None
        #     original_file_name = event_body["original_file_name"]
        #     if(not get_url or not put_url):
        #         return response_object(500, 'file url is not given!')
                
        #     source_language =  event_body["source_language"] 
        #     target_language = event_body["target_language"]
        #     if(not source_language or not target_language):
        #         return response_object(500, 'Source and target language are required!')
            
        #     model = event_body["model_id"]
        #     region = event_body["region"]
             
        #     if(not model):
        #         return response_object(500, 'Model not defined!')
            
        #     if region:
        #         extra_params =  {'region': region }

        #     apiClient.translate_file(get_url, put_url, original_file_name, source_language, target_language, model, scale=pdf_scale_down_ratio, extra_params=extra_params)
        #     return response_object(200, 'file translated!')
        
        # elif action == "delete-file":
        #     file_name = event_body["name"]
        #     if(not file_name):
        #         return response_object(500, 'file name is not given!')
                
        #     object_store_client.delete_file(file_name)
        #     return response_object(200, 'file cleared!')
        
        elif action == "upload-config":
            scale = event_body["scale"] if "scale" in event_body else 0.5
            source_language = event_body["source_language"]
            get_url = event_body["get_url"]
            username = event_body["username"]
            target_language = event_body["target_language"]
            model = event_body["model_id"] if "model_id" in event_body else None
            region = event_body["region"] if "region" in event_body else None
            original_file_name = event_body["original_file_name"]

            if(not get_url or not source_language or not target_language or not username or not original_file_name or not model):
                return response_object(500, 'Required values not given!')
                
            if(not region):
                extra_params = dict()
            if region:
                extra_params={'region': region}
                
            res = apiClient.upload_config(username, get_url, original_file_name, source_language, target_language, model, scale, extra_params)
            return response_object(200, res)
       
        elif action == "get-user-files":
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