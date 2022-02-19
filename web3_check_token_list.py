import json

tokens = {}

data = open(r'all_address.json', 'r')
for item in json.loads(data.read()):
    tokens[item]=True

def is_listed_token(address):
    return tokens[address]