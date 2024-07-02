import requests
from datetime import datetime
import json

with open('config.json', 'r') as f:
    config = json.load(f)

api_endpoint = "https://api.api-ninjas.com/v1/cryptoprice"
api_key = config['api_key']
headers = {
    'X-Api-Key': api_key
}
params = {
    'symbol': 'BTCUSDC'
}

response = requests.get(api_endpoint, headers=headers, params=params).json()
response['timestamp'] = datetime.fromtimestamp(response['timestamp'])


