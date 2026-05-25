from fastapi import Security, HTTPException
import os
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv


load_dotenv()


API_KEY_HEADER = APIKeyHeader(name="financial-platform-api-key")

def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")
    