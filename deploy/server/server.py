import sys
import nest_asyncio
import uvicorn

sys.path.append(".")

from services.lambda_service import LambdaService
from services.object_store.S3Client import S3Client
from utils.logger import Logger

logger = Logger(name="NLLB Logger")
logger = Logger.get_logger()

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, HTTPException
from services.db.dynamo import DynamoDBClient

from services.api import ApiService
from datetime import datetime
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

d = S3Client()
api_client = ApiService(DynamoDBClient(), S3Client())

@app.get("/")
def health_check():
    return datetime.now()

@app.post("/accessible-pdf/")
async def covnert_pdf_to_html(request: Request):
    try:
        req_params_dict = dict(request.query_params)
        action = req_params_dict["action"] if "action" in req_params_dict else None
        body = await request.json()

        if not action:
            raise HTTPException(status_code=500, detail="Action not defined")
        
        elif action == "health-check":
            return datetime.now()
        
        elif action == "convert":
            if "object_key" not in body:
                raise HTTPException(status_code=400, detail="Cannot find file")
         
            object_key = body["object_key"]
            lambda_client =  LambdaService()
            response = lambda_client.invoke(object_key)
            if(response):
                return "converting file"
            
            raise HTTPException(status_code=400, detail="Cannot convert file. Something went wrong")
        
        elif action == "upload-config":
            username = body["username"] if "username" in body else None
            file_name = body["file_name"] if "file_name" in body else None
            get_url = body["pdf_url"] if "pdf_url" in body else None
            converter = body["converter"] if "converter" in body else None
            if not username or not file_name or not get_url or not converter:
                raise HTTPException(status_code=400, detail="Required information not providied")
            
            return api_client.upload_config(username, file_name, get_url, converter)

        elif action == "get-files":
            username = body["username"] if "username" in body else None
            if not username:
                raise HTTPException(status_code=400, detail="Username not providied")
            files = api_client.get_file_statuses(username)
            return files
        
        elif action == "get-file":
            key = body["key"] if "key" in body else None
            if not key:
                raise HTTPException(status_code=400, detail="File name not providied")
            file = api_client.get_file(key)
            return file
        
        raise HTTPException(status_code=500, detail="Action not supported")
    except Exception as e:
        logger.error(e)
        if type(e) == HTTPException:
            raise e
        raise HTTPException(status_code=500, detail="Something went wrong")
    
nest_asyncio.apply()
uvicorn.run(app, port=8001)