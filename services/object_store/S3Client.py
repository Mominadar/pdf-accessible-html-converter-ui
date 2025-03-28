from utils.logger import Logger
import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()
logger = Logger(name="S3 Logger")
logger = Logger.get_logger()

SOURCE_BUCKET_NAME = os.environ["SOURCE_BUCKET_NAME"]
TARGET_BUCKET_NAME = os.environ["TARGET_BUCKET_NAME"]
BUCKET_REGION = os.environ["BUCKET_REGION"]

class S3Client:
    def __init__(self) -> None:
        self.client = boto3.client(service_name='s3', region_name=BUCKET_REGION)
        
    def upload_file(self, filename, file, bucket=TARGET_BUCKET_NAME):
        try:
            self.client.upload_fileobj(file, bucket, filename, ExtraArgs={"ContentType": "text/html; charset=utf-8"})
        except FileNotFoundError:
            logger.error(
                f"Couldn't find {filename} For a PUT operation, the key must be the "
                f"name of a file that exists on your computer."
            )
            raise
        except Exception as e:
            logger.error(e)
            raise
    
    def get_put_url(self, get_url):
        filename = get_url[get_url.rfind("/")+1: get_url.rfind(".pdf")]
        url = f"https://{TARGET_BUCKET_NAME}.s3.{BUCKET_REGION}.amazonaws.com/{filename}.html"
        return url
        
    def delete_file(self, bucket, file_name):
        try:
            self.client.delete_object(
                    Bucket=bucket,
                    Key=file_name,
                )
            return json.dumps({'success':True})
        except Exception as e:
            logger.error(f'Could not remove file. {file_name}, {str(e)}')
            raise