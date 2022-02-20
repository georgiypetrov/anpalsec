import socketio
import asyncio
from web3 import Web3
from utils import extract_addresses_from_transactions

sio = socketio.AsyncClient(logger=False, engineio_logger=False)
w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/qjXOAXBstwICKl3R3EW6TC5lJbssTn4F'))

class ZerionAPI:
    URI = 'wss://api-v4.zerion.io/'
    API_TOKEN = 'Demo.ukEVQp6L5vfgxcz4sBke7XvS873GMYHy'
    ORIGIN = 'http://localhost:3000'
    TRANSACTIONS_LIMIT = 100
    MAX_TRANSACTIONS = 10000
    MAX_PERIOD = 60 * 60 * 24 * 30 # 1 month
    
    def __init__(self):
        self.ADDRESS_INFO = None
        self.TRANSACTIONS = None
        self.CONNECTED_TO_SOCKET = False

    async def connect_to_socket(self):
        if sio.connected:
            return
        await sio.connect(
            f'{self.URI}/?api_token={self.API_TOKEN}',
            headers={'Origin': self.ORIGIN},
            namespaces=['/address'],
            transports=['websocket']
        )
        while not self.CONNECTED_TO_SOCKET:
            await asyncio.sleep(0)

    async def get_address_info(self, address):
        self.ADDRESS_INFO = None
        await self.connect_to_socket()
        
        await sio.emit('get', {
            'scope': ['info'],
            'payload': {
                'address': address,
            }
        }, namespace='/address')

        while not self.ADDRESS_INFO:
            await asyncio.sleep(0)

        return self.ADDRESS_INFO

    async def _get_last_transactions(self, address, offset=0):
        self.TRANSACTIONS = None
        print("getting address info: ", address)
        await self.connect_to_socket()
        print(offset)
        await sio.emit('get', {
            'scope': ['transactions'],
            'payload': {
                'address': address,
                'transactions_limit': self.TRANSACTIONS_LIMIT,
                'transactions_offset': offset                
            }
        }, namespace='/address')

        while not self.TRANSACTIONS:
            await asyncio.sleep(0)
            
        print("received")
        return self.TRANSACTIONS

    async def get_transactions_data(self, address):
        addresses = set()
        batch = None
        is_new = False
        trx_count = 0
        timestamp = w3.eth.getBlock('latest')['timestamp']
        earliest_timestamp = timestamp
        while trx_count < self.MAX_TRANSACTIONS and \
        timestamp - earliest_timestamp < self.MAX_PERIOD and \
        (batch is None or len(batch) > 0):
            print(timestamp - earliest_timestamp)
            batch = await self._get_last_transactions(address, trx_count)
            trx_count += len(batch)
            if len(batch) < self.TRANSACTIONS_LIMIT:
                is_new = True
            earliest_timestamp = batch[-1]['mined_at'] if len(batch) > 0  else earliest_timestamp
            addresses.update(extract_addresses_from_transactions(batch))
            print(len(addresses), earliest_timestamp)
        print(timestamp - earliest_timestamp)
        return addresses, trx_count, is_new, earliest_timestamp


API = ZerionAPI()

@sio.event(namespace='/address')
def connect():
    print('commected')
    API.CONNECTED_TO_SOCKET = True

@sio.on('received address info', namespace='/address')
def received_address_assets(data):
    API.ADDRESS_INFO = data['payload']['info']

@sio.on('received address transactions', namespace='/address')
def received_address_assets(data):
    API.TRANSACTIONS = data['payload']['transactions']
