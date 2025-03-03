from fastapi import APIRouter, Depends, HTTPException
from app.schemas.energy import DeviceCreate, DeviceInDB
from app.database import devices_collection
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/devices", response_model=DeviceInDB)
async def register_device(
    device: DeviceCreate,
    user: dict = Depends(get_current_user)  # JWT payload includes "sub" as user ID
):
    existing = devices_collection.find_one({"device_id": device.device_id})
    if existing:
        raise HTTPException(400, "Device ID already exists")
    
    device_data = device.dict()
    device_data["owner_id"] = user["sub"]  # Use "sub" instead of "id"
    
    result = devices_collection.insert_one(device_data)
    return {**device_data, "id": str(result.inserted_id)}