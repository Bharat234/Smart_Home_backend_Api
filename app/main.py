from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import energy, devices, auth
from app.database import influx_client, mongo_db

app = FastAPI(title="Smart Energy API", version="1.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(energy.router, prefix="/api/v1", tags=["Energy"])
app.include_router(devices.router, prefix="/api/v1", tags=["Devices"])
app.include_router(auth.router, prefix="/auth/v1", tags=["Authentication"])

@app.on_event("startup")
async def startup_db():
    print("Connected to InfluxDB:", influx_client.ping())
    print("MongoDB version:", mongo_db.command("serverStatus")["version"])