import os
import random
import asyncio
import aiohttp

num_of_drivers = int(os.environ['DRIVER_NUMBER'])
time_interval = int(os.environ['POSITION_SEND_INTERVAL'])
service_host = os.environ['SERVICE_HOST']


def generate_position(driver_id):
    return {
        'driver_id': driver_id,
        'latitude': round(random.uniform(49.767749, 49.896666), 6),
        'longitude': round(random.uniform(23.906237, 24.116664), 6),
        'speed': random.randint(0, 120),
        'altitude': random.randint(250, 450)
    }


async def send_position(session, position):

    async with session.post(f'{service_host}/positions', json=position) as resp:
        text = await resp.text()
        return resp.status, text


async def main():
    while True:
        async with aiohttp.ClientSession() as session:
            tasks = [
                send_position(session, generate_position(i))
                for i in range(num_of_drivers)
            ]
            await asyncio.gather(*tasks)
            await asyncio.sleep(time_interval)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

