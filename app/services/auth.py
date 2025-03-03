import os
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/v1/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mock user database (replace with real implementation)
fake_users_db = {
    "user1": {
        "id": "user1", 
        "hashed_password": pwd_context.hash("secret"),
    }
}

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire, "sub": "user1"})
    return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm="HS256")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(401, "Invalid credentials")