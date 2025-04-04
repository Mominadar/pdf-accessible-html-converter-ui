import boto3
import urllib
import pymupdf  # PyMuPDF
import io
import os
import json

from services.api import ApiService
from services.db.dynamo import DynamoDBClient
from services.object_store.S3Client import S3Client
from utils.helpers import response_object
from utils.logger import Logger

STATE_MACHINE_ARN =  os.environ.get("STATE_MACHINE_ARN")
stepfunctions = boto3.client("stepfunctions", region_name=os.environ.get("STATE_MACHINE_REGION"))

SOURCE_BUCKET_NAME = os.environ["SOURCE_BUCKET_NAME"]
TARGET_BUCKET_NAME = os.environ["TARGET_BUCKET_NAME"]
BUCKET_REGION = os.environ["BUCKET_REGION"]

logger = Logger(name="NLLB Logger")
logger = Logger.get_logger()

db_client = DynamoDBClient()
s3_client = S3Client()

def split_pdf_by_chunks(source_bucket, file_key, target_bucket, page_chunk_size=5):
    """Splits a PDF into multi-page chunks and uploads to S3."""
    pdf_data = s3_client.get_file(file_key, bucket=source_bucket)

    pdf_document = pymupdf.open(stream=pdf_data, filetype="pdf")
    filename = os.path.basename(file_key)
    folder_name = f"{filename}_chunks/"
    
    total_pages = len(pdf_document)
    chunk_count = 0
    chunks = []
    for i in range(0, total_pages, page_chunk_size):
        new_pdf = pymupdf.open()
        new_pdf.insert_pdf(pdf_document, from_page=i, to_page=min(i + page_chunk_size - 1, total_pages - 1))

        pdf_bytes = io.BytesIO()
        new_pdf.save(pdf_bytes)
        pdf_bytes.seek(0)

        chunk_key = f"{folder_name}chunk_{chunk_count + 1}.pdf"
        s3_client.upload_file(chunk_key, pdf_bytes, bucket=target_bucket, ContentType="application/pdf")
        logger.info(f"Uploaded {chunk_key}")
        get_url = f"https://{TARGET_BUCKET_NAME}.s3.{BUCKET_REGION}.amazonaws.com/{chunk_key}"
        chunks.append({"chunk_key":chunk_key, "original_key": file_key, "get_url": get_url})
        chunk_count += 1
    return folder_name, chunks

def lambda_handler(event, context):
    event_name = event["Records"][0]["eventName"]
    if(not event_name or "ObjectCreated" not in event_name):
        return response_object(500, 'Action is not defined or valid!')
        
    logger.info(f'Event:  {event_name}')
    
    key = event["Records"][0]["s3"]["object"]["key"]   
    key = urllib.parse.unquote(key)
    logger.info(f"key: {key}")

    bucket = SOURCE_BUCKET_NAME
    target_bucket = TARGET_BUCKET_NAME

    page_chunk_size = event.get("page_chunk_size", 2)  # Default to 5 pages per chunk

    try:
        api_service = ApiService(db_client, s3_client)
        api_service.mark_file_status(key, "in_progress") 
    except Exception as e:
        logger.error(e)
        raise Exception("Could not find file config information")
    
    folder_name, chunks = split_pdf_by_chunks(bucket, key, target_bucket, page_chunk_size)
    total_chunks = len(chunks)
    logger.info(f"Total chunks uploaded: {total_chunks} in folder {folder_name}")
    
    stepfunctions.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        input=json.dumps({
            "chunks": chunks,
        })
    )

    return {"status": "Chunks uploaded & Step Functions started"}
