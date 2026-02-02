from fastapi import Header, HTTPException
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("API_KEY")

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
