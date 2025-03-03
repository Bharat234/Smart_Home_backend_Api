from fastapi import APIRouter, Depends, HTTPException
from app.schemas.energy import EnergyData
from app.database import write_energy_data, devices_collection
from app.services.auth import get_current_user

router = APIRouter()

def validate_device_ownership(user_id: str, device_id: str):
    device = devices_collection.find_one({"device_id": device_id})
    return device and device["owner_id"] == user_id

@router.post("/energy", status_code=202)
async def post_energy_data(
    data: EnergyData,
    user: dict = Depends(get_current_user)  # JWT payload has "sub"
):
    if not validate_device_ownership(user["sub"], data.device_id):
        raise HTTPException(403, detail="Device access denied")
    write_energy_data(data)
    return {"status": "data_accepted"}