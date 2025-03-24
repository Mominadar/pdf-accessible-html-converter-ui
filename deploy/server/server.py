import os
import sys
sys.path.append(".")

# from utils.helpers import response_object
# from utils.logger import Logger

# logger = Logger(name="NLLB Logger")
# logger = Logger.get_logger()

import nest_asyncio
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, HTTPException
# from pydantic import BaseModel
from fastapi.responses import HTMLResponse

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

api_client = ApiService()

@app.get("/")
def health_check():
    return datetime.now()

@app.post("/accessible-pdf/", response_class=HTMLResponse)
async def covnert_pdf_to_html(request: Request):
    try:
        body = await request.json()
        if "converter" not in body or body["converter"] not in ["agentic","mistral"]:
            raise HTTPException(status_code=400, detail="Converter not provided. Specify converter as 'mistral' or 'agentic' for conversion")
        if "pdf_url" not in body:
            raise HTTPException(status_code=400, detail="PDF url not provided")

        pdf_path = body["pdf_url"]
        converter = body["converter"]
        html = api_client.convert_pdf_to_html(converter, pdf_path)
        return html
    except Exception as e:
        print("Error",e)
        raise HTTPException(status_code=500, detail="Something went wrong")

nest_asyncio.apply()
uvicorn.run(app, port=8001)