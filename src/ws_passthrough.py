'''import requests
from src.config.config import env

# Cloudflare API endpoint and headers
endpoint = "https://api.cloudflare.com/client/v4/zones"
headers = {
    "X-Auth-Email": env.CF_EMAIL,
    "X-Auth-Key": env.CF_API_KEY,
    "Content-Type": "application/json",
}

# Domain name and WebSocket Passthrough setting
domain_name = "smartpro.solutions"
ws_passthrough = {"value": "on"}

# Get domain ID
response = requests.get(endpoint, headers=headers, params={"name": domain_name})
zone_id = response.json()["result"][0]["id"]

# Enable WebSocket Passthrough
endpoint = f"{endpoint}/{zone_id}/settings/websockets"
response = requests.patch(endpoint, headers=headers, json=ws_passthrough)

if response.ok:
    print("WebSocket Passthrough enabled.")
else:
    print(f"Failed to enable WebSocket Passthrough. Error: {response.text}")
'''

import json
from src.handlers.fetch import fetch
from src.config.config import env

headers = {
    "X-Auth-Email": env.CF_EMAIL,
    "X-Auth-Key": env.CF_API_KEY,
    "Content-Type": "application/json",
}

payload = {
        "name": None,
        ""