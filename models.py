import socketio
import asyncio

sio = socketio.AsyncClient(logger=False, engineio_logger=False)

class ZerionAPI:
    URI = 'wss://api-v4.zerion.io/'
    API_TOKEN = 'Demo.ukEVQp6L5vfgxcz4sBke7XvS873GMYHy'
    ORIGIN = 'http://localhost:3000'
    
    def __init__(self):
        self.ADDRESS_INFO = None
        self.TRANSACTIONS = None
        self.CONNECTED_TO_SOCKET = False

    async def connect_to_socket(self):
        await sio.connect(
            f'{self.URI}/?api_token={self.API_TOKEN}',
            headers={'Origin': self.ORIGIN},
            namespaces=['/address'],
            transports=['websocket']
        )
        while not self.CONNECTED_TO_SOCKET:
            await asyncio.sleep(0)

    async def disconnect_from_socket(self):
        self.CONNECTED_TO_SOCKET = False
        await sio.disconnect()

    async def get_address_info(self, address):
        self.ADDRESS_INFO = None
        print("getting address info: ", address)
        await self.connect_to_socket()
        
        await sio.emit('get', {
            'scope': ['info'],
            'payload': {
                'address': address,
            }
        }, namespace='/address')

        while not self.ADDRESS_INFO:
            await asyncio.sleep(0)
            
        await self.disconnect_from_socket()
        print("received")
        return self.ADDRESS_INFO


API = ZerionAPI()

@sio.event(namespace='/address')
async def connect():
    print('Connected to /address namespace!')
    API.CONNECTED_TO_SOCKET = True

@sio.on('received address info', namespace='/address')
def received_address_assets(data):
    API.ADDRESS_INFO = data['payload']
