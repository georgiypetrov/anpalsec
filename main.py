import asyncio
from fastapi import FastAPI
from models import API
from web3_defisafety import defisafety_security_percentage
from web3_extract_data import is_token_erc20, is_contract
from web3_check_token_list import is_listed_token
from fastapi.middleware.cors import CORSMiddleware

MIN_TRANSACTIONS = 1000
MIN_USERS = 50
MIN_SECURITY_PERCENTAGE = 40

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/analytics/{address}")   
async def get_analytics(address, value: int = 0, is_approve = False):
        is_max_approve = True if is_approve and value == 1337 else 0
        address = address.lower()
        trx_data = await API.get_transactions_data(address)
        info = await API.get_address_info(address)
        addresses, trx_count, is_new, _ = trx_data
        is_token = is_token_erc20(address)
        is_contr = is_contract(address)
        report = ""
        print(info)
        if is_token:
                listed = is_listed_token(address)
                if not listed:
                        report += "ERC20 not listed in Token Lists registry/n"
                if is_max_approve and len(info['proxies']) > 0:
                        report += "DANGER! You're about to make infinite approve to proxy contract,\n   there is risk it will change logic and drain all your funds\n"
                if value > 0:
                        report + "Be careful! You're sending funds to ERC20 token, there is risk losing your funds\n"
        is_protocol, security_percentage = defisafety_security_percentage(address)
        if is_protocol:
                report += "Trust Score: " + str(security_percentage) + "\n"
                if security_percentage < MIN_SECURITY_PERCENTAGE:
                        report += "DANGER! This contract is known protocol with low trust score\n"
        if value > 0 and is_contr:
                report += "Be careful! You're sending tokens to contract address, maybe you wanted send to user address\n"
        if len(addresses) < MIN_USERS:
                report += "Be Careful! A few amount of addresses interacted with destination address: " + str(len(addresses)) + "\n"
        if trx_count < MIN_TRANSACTIONS:
                report += "Be Careful! The address has low amount of transactions: " + str(trx_count) + "\n"
        return report
