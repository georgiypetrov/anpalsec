import asyncio
from models import API

async def main(address: str):
    data = await API.get_address_info(address)
    print(data)

if __name__ == '__main__':
    test_address = '0x7e5ce10826ee167de897d262fcc9976f609ecd2b'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(test_address))
