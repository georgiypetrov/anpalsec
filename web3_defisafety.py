from audioop import add
import json

tokens = {}
all_token = {}

data = open(r'./defisafety.json', 'r')
for item in json.loads(data.read()):
    if(item['tokenAddress'] != None):
        tokens[item['tokenAddress'].lower()]=item['breakdowns'][3]['percentage']
        all_token[item['tokenAddress'].lower()] = True

def is_token(address):
    if address == None:
        return False
    else:
        return address in all_token

def defisafety_security_percentage(address):
    _is_token = is_token(address)
    return _is_token, tokens[address] if _is_token else 0