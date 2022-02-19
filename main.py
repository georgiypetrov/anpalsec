import asyncio
from fastapi import FastAPI
from models import API

app = FastAPI()

@app.get("/analytics/{address}")   
async def get_analytics(address):
    trx_data = await API.get_transactions_data(address)
    info = await API.get_address_info(address)
    print(info)
    addresses, trx_count, young_contract, earliest_timestamp = trx_data
    return {
            'addresses': len(addresses), 
            'trxCount': trx_count, 
            'isYoung': young_contract, 
            'earliestTimestamp': earliest_timestamp, 
            'type': info['type'], 
            'proxyCount': len(info['proxies'])
    }
