import os
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()  # Load .env file

# InfluxDB Connection
influx_client = InfluxDBClient(
    url=os.getenv("INFLUX_URL"),
    token=os.getenv("INFLUX_TOKEN"),
    org=os.getenv("INFLUX_ORG")
)

# MongoDB Connection
mongo_client = MongoClient(os.getenv("MONGO_URI"))
mongo_db = mongo_client[os.getenv("MONGO_DB", "smart_energy")]

# Collections
devices_collection = mongo_db["devices"]
users_collection = mongo_db["users"]

def write_energy_data(data):
    # Hardcode test data
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point("energy_usage")
        .tag("device_id", "test-device")
        .field("power", 1.5)
        .time(datetime.utcnow())
    )
    write_api.write(
        bucket=os.getenv("INFLUX_BUCKET"),
        org=os.getenv("INFLUX_ORG"),
        record=point
    )