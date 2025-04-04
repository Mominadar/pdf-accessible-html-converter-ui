import io
from services.agentic.agentic_service import AgenticService
from services.mistral.mistral_service import MistralService
from utils.helpers import get_current_date_str
from utils.logger import Logger

logger = Logger(name="NLLB Logger")
logger = Logger.get_logger()

class ApiService():
    def __init__(self, db_client, object_store_client):        
        self.db_client = db_client
        self.object_store_client = object_store_client

    def mark_file_status(self, object_key, status):
        try:
            self.db_client.find_by_id(object_key)
            self.db_client.put(object_key, "file_status", status) 
        except Exception as e:
            logger.error(e)
            raise Exception("Could not find file config information")
        
    def convert_pdf_to_html(self, object_key, original_key, get_url):
        config = None
        try:
            config = self.db_client.find_by_id(original_key)
        except Exception as e:
            logger.error(e)
            raise Exception("Could not find file config information")
        
        try: 
            # self.db_client.put(object_key, "file_status", "in_progress") 
            converter =  config["converter"]
            put_url =  get_url.replace(".pdf", ".html")
            if(not get_url or not put_url or not converter):
                raise Exception('Something went wrong. Config incomplete!')
            
            if converter not in ["agentic", "mistral"]:
                raise Exception("Invalid converter")

            logger.info(f"Using converter: {converter}")
            if converter == "agentic":
                agentic_service = AgenticService()
                html = agentic_service.convert_pdf_to_html(get_url)
            elif converter == "mistral":
                mistral_service = MistralService()
                html = mistral_service.convert_pdf_to_html(get_url)
            
            put_url = self.upload_html_file(put_url, html)
            # self.db_client.put(object_key, "file_status", "done")
            return put_url
        except Exception as e:
            logger.error(e)
            self.db_client.put(object_key, "file_status", "error")
            self.db_client.put(object_key, "error_reason", str(e))

    def upload_html_file(self, put_url, html):
        buffer = io.BytesIO(html.encode("utf-8"))  # Encode as UTF-8
        filename = put_url[put_url.rfind("/")+1:]
        self.object_store_client.upload_file(filename, buffer)
        return put_url
       
    def upload_config(self, username, original_file_name, get_url, converter):
        try:
            if not original_file_name.lower().endswith(".pdf"):
                raise Exception ("File format not supported")
            
            put_url = self.object_store_client.get_put_url(get_url)
            # store config in db to be picked up when file is processed
            current_utc_time = get_current_date_str()
            self.db_client.create({
                'object_key': {"S" :original_file_name},
                'username': {"S" : username},
                'converter' : {"S" : converter},
                'get_url' : {"S" : get_url},
                'put_url' : {"S" : put_url},
                'last_modified_at' : {"S" : current_utc_time},
                'created_at' : {"S" : current_utc_time},
                'file_status': {"S" :"in_progress"},
            })

            return put_url

        except Exception as e:
            logger.error(f'Error in upload: {str(e)}')
            self.db_client.create({
                'object_key': {"S" : original_file_name},
                'username': {"S" : username},
                'converter' : {"S" : converter},
                'get_url' : {"S" : get_url},
                'put_url' : {"S" : ""},
                'last_modified_at' : {"S" : get_current_date_str()},
                'created_at' : {"S" : get_current_date_str()},
                'file_status': {"S" :"error"},
                'error_reason': {"S" :str(e)},
            })
            raise
    
    def get_file_statuses(self, username):
        try:
            files = self.db_client.find('username', username)
            return files

        except Exception as e:
            logger.error(f'Error in getting files list: {str(e)}')
            raise
    
    def get_file(self, key):
        try:
            file = self.db_client.find_by_id(key)
            return file
        except Exception as e:
            logger.error(f'Error in getting file: {str(e)}')
            raise
    
        