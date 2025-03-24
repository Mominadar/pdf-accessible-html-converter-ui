
import json
import re
from urllib.parse import unquote
from datetime import datetime

def response_object(status_code:int, body, headers={
                    "Access-Control-Allow-Origin": "*", 
                    'Content-Type': "application/json", 
                     'Access-Control-Allow-Methods': '*',

                }):
    return {
            'statusCode': status_code,
            'body': json.dumps(body),
            'headers': headers,
    }

def decode_url(url):
    return unquote(url)

def get_current_date_str():
    # Get the current date and time
    current_datetime = datetime.now()
    # Convert to string
    datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")  # DateTime as string: "YYYY-MM-DD HH:MM:SS"
    return datetime_str

def get_bucket_from_url(s3_url):
    # Extract bucket and key from URL
    pattern = r'https://(.*?).s3.(.*?).amazonaws.com/(.*)'
    match = re.match(pattern, s3_url)
    
    if not match:
        raise ValueError("Invalid S3 URL format")
    
    bucket_name = match.group(1)
    return bucket_name