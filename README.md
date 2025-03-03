# Smart Home Energy Monitoring System

A scalable IoT backend system for monitoring energy consumption of smart home devices, built with FastAPI, InfluxDB, MongoDB, and Docker. Supports real-time data ingestion, user authentication, and integration with Alexa voice commands.
[Note : This Project is done with PowerShell ,Users with Linux/Mac should change some commands for some parts.] 

#[Do generate your own device_cert.pem and device_key.pem file using openssl (Required and is mentioned below)]

![Architecture Diagram](https://i.imgur.com/7QY3t8l.png)

## License
MIT License - See LICENSE

Let’s build a greener future! 🌱
Feel free to contribute via PRs or open issues for feature requests.

## Features
- **Real-Time Energy Monitoring**: Collect data from smart plugs/meters via MQTT/REST.
- **Data Visualization**: Built-in support for time-series analytics (InfluxDB + Grafana).
- **User Authentication**: OAuth2 with JWT tokens.
- **IoT Protocol Support**: MQTT (Zigbee/Bluetooth) + REST (WiFi/Ethernet).
- **Alexa Integration**: Voice control for energy queries. (Optional)

## Technologies
- **Backend**: Python FastAPI
- **Databases**: InfluxDB (time-series), MongoDB (metadata)
- **IoT**: MQTT (Mosquitto), AWS IoT Core (simulated devices)
- **Auth**: OAuth2/JWT
- **Infra**: Docker, Kubernetes (GCP/AWS)

## Security Implementation
Layer	Implementation
- User Auth	OAuth2 with JWT tokens (FastAPI OAuth2PasswordBearer)
- Device Auth	X.509 certificates for Zigbee/WiFi devices
- Data Integrity	HTTPS for APIs, TLS for MQTT
- Rate Limiting	100 requests/minute per IP (FastAPI + slowapi)

**Note: Do take Help from open-source LLM's if having problem with dependencies**.
---

### Prerequisites
- Docker & Docker Compose
- Python 3.9+
- ngrok (for Alexa testing) (Optional)
- OpenSSL (for Security)

## Install OpenSSL and MoongoDb: 
- OpenSSL from (https://code.google.com/archive/p/openssl-for-windows/downloads) (for Windows Users)
- Add to Env variables. (make sure openssl.exe and openssl.conf file are in same directory , if not provide path for both.)
- MongoDB Shell from (https://www.mongodb.com/try/download/shell)

```bash
# Clone the repo
git clone https://github.com/your-username/smart-energy-backend.git
cd smart-energy-backend

# Install Python dependencies
python -m venv venv
source venv/bin/activate  # Linux/Mac
# .\venv\Scripts\activate.psi   # Windows
pip install -r requirements.txt (Make sure all dependencies are donwloaded)

# Start services
docker-compose up -d influxdb mongodb mosquitto

# Install OpenSSL (if not installed)
# Option 1: Use WSL (Windows Subsystem for Linux)
# Option 2: Download for Windows: https://slproweb.com/products/Win32OpenSSL.html

# Generate self-signed certs (using OpenSSL in PATH)
openssl req -x509 -newkey rsa:4096 -nodes -out device-cert.pem -keyout device-key.pem -days 365 -subj "/CN=localhost"

WORKING:
-------------------------------------
INITIALIZE InfluxDb
Open https://localhost:8086
Login : Username / Password
Create Bucket : Bucket_Name
##(Ensure the bucket name, org name, username, password etc. and the permissions required (write permission enabled) in docker file, .env file and the InfluxDb are the same)
------------------------------------

Start Backend:
uvicorn app.main:app --reload

Ensuer MongoDb is Running:
mongosh --version
mongosh mongodb://localhost:27017/smart_energy(Name 

Register a Device :
Power Shell : 
cmd 1. $token = (Invoke-WebRequest -Uri http://localhost:8000/auth/v1/token -Method POST -Body "username=user1&password=secret").Content | ConvertFrom-Json | Select -ExpandProperty access_token

cmd 2. Invoke-WebRequest -Uri "http://localhost:8000/api/v1/devices" -Method POST -Headers @{ 
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
} -Body '{"device_id": "smartplug-1", "type": "plug", "location": "kitchen"}'

Post Energy Data:
cmd 3. Invoke-WebRequest -Uri "http://localhost:8000/api/v1/energy" -Method POST -Headers @{ 
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
} -Body '{"device_id": "smartplug-1", "power": 3.5}'

##(expected output/response presented :
  for registering device : {
  "device_id": "smartplug-1",
  "type": "plug",
  "location": "kitchen",
  "protocol": "wifi",
  "owner_id": "user1",
  "status": "active",
  "id": "65f1b2c8e7a8c6a9d4f3b2c8"
  }

  for sending energy data :
  {"status": "data_accepted"}
  )

Verification :
# Run in a Python shell
from influxdb_client import InfluxDBClient

client = InfluxDBClient(url="http://localhost:8086", token="my-super-secret-token")
query = 'from(bucket: "energy") |> range(start: -1h)'
result = client.query_api().query(query)
print(result.to_json())

Output :
[
  {
    "measurement": "energy_usage",
    "tags": {"device_id": "smartplug-1"},
    "fields": {"power": 3.5},
    "time": "2024-05-21T12:00:00Z"
  }
]
```
This README:
1. Provides clear setup/usage instructions  
2. Documents all key features  
3. Includes troubleshooting tips  
4. Shows API examples  
5. Supports both local/dev and production setups 🚀
