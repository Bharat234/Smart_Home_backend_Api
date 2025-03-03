import asyncio
import random
import time
from aiomqtt import Client
import os

async def simulate_device(device_id: str):
    async with Client(
        hostname="localhost",
        port=1883,
        client_id=device_id,
        tls_params={"certfile": os.path.abspath("device-cert.pem")}
    ) as client:
        while True:
            power = random.uniform(0.1, 5.0)
            payload = f'{{"device_id": "{device_id}", "power": {power}, "timestamp": {time.time()}}}'
            await client.publish(f"energy/{device_id}", payload)
            await asyncio.sleep(5)

async def main():
    tasks = [simulate_device(f"device-{i}") for i in range(100)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())