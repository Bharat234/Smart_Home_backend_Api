from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth import create_access_token, fake_users_db, pwd_context

router = APIRouter()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(400, "Invalid credentials")
    
    access_token = create_access_token(
        data={"sub": user["id"]},
        expires_delta=timedelta(days=1)
    )
    return {"access_token": access_token, "token_type": "bearer"}