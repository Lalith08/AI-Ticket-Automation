import os
from fastapi import Header, HTTPException, status
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    # Fail fast so you don't run without security by mistake
    raise RuntimeError("API_KEY is not set. Create a .env file with API_KEY=...")

def require_api_key(x_api_key: str = Header(default=None, alias="X-API-Key")):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return True