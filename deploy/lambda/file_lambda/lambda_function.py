from utils.logger import Logger

logger = Logger(name="NLLB Logger")
logger = Logger.get_logger()

from services.api import ApiClient
from utils.helpers import response_object
from utils.client import get_object_store_client, get_translation_client, get_db_client

from services.file_parsers.docx import TranslateDocxClient
from services.file_parsers.pdf import TranslatePdfClient
from services.file_parsers.md import TranslateMdClient
from services.file_parsers.xlf import TranslateXlfClient
import urllib.parse


object_store_client = get_object_store_client()
db_client = get_db_client()

pdf_client = TranslatePdfClient()
docx_client = TranslateDocxClient()
md_client = TranslateMdClient()
xlf_client = TranslateXlfClient()      

def lambda_handler(event, context):
    try:
        event_name = event["Records"][0]["eventName"]
        if(not event_name or "ObjectCreated" not in event_name):
            return response_object(500, 'Action is not defined or valid!')
            
        logger.info(f'Action:  {event_name}')
        
        apiClient = ApiClient(object_store_client=object_store_client, pdf_client=pdf_client, docx_client=docx_client, md_client=md_client, xlf_client=xlf_client, db_client=db_client)
    
        object_key = event["Records"][0]["s3"]["object"]["key"]   
        
        urls = object_store_client.get_url_from_key(object_key)
        get_url = urls["get_url"]
        put_url = urls["put_url"]
        
        object_key = urllib.parse.unquote(object_key)
        logger.info(f"key: {object_key}")
        apiClient.translate_file_async(get_url, put_url, object_key)
        return response_object(200, object_key)
            
    except Exception as e:
        logger.error(e)
        return response_object(500, str(e))   