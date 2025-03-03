from pydantic import BaseModel
from datetime import datetime

class EnergyData(BaseModel):
    device_id: str
    power: float
    timestamp: datetime = datetime.now()

class DeviceCreate(BaseModel):
    device_id: str
    type: str
    location: str
    protocol: str

class DeviceInDB(DeviceCreate):
    owner_id: str
    status: str = "active"