import json

tokens = {}
all_token = {}

data = open(r'./defisafety.json', 'r')
for item in json.loads(data.read()):
    tokens[item['tokenAddress']]=item['breakdowns'][3]['percentage']
    if(item['tokenAddress'] != None):
        all_token[item['tokenAddress']] = True

def is_token(address):
    if address == None:
        return False
    else:
        return address in all_token

def defisafety_security_percentage(address):
    return tokens[address]