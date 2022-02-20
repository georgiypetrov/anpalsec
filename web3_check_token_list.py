import json

tokens = {}

data = open(r'all_address.json', 'r')
for item in json.loads(data.read()):
    tokens[item.lower()]=True

def is_listed_token(address):
    return address in tokens