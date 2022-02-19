def extract_addresses_from_transactions(transactions):
    addresses = set([trx["address_from"] for trx in transactions])
    addresses.update(set([trx["address_to"] for trx in transactions]))
    return addresses