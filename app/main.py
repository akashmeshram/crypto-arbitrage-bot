from dotenv import load_dotenv
import os
from cryptography.hazmat.primitives.asymmetric import ed25519
from urllib.parse import urlparse, urlencode
import urllib
import json
import requests


def coinswitch_api_call(endpoint, method, params, payload):
    api_key = os.getenv('COINSWITCH_API_KEY')
    secret_key = os.getenv('COINSWITCH_API_SECRET')

    unquote_endpoint = endpoint
    if method == "GET" and len(params) != 0:
        endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)
        unquote_endpoint = urllib.parse.unquote_plus(endpoint)

    signature_msg = method + unquote_endpoint + json.dumps(payload, separators=(',', ':'), sort_keys=True)

    request_string = bytes(signature_msg, 'utf-8')
    secret_key_bytes = bytes.fromhex(secret_key)
    secret_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key_bytes)
    signature_bytes = secret_key.sign(request_string)
    signature = signature_bytes.hex()

    url = "https://coinswitch.co" + endpoint

    headers = {
    'Content-Type': 'application/json',
    'X-AUTH-SIGNATURE': signature,
    'X-AUTH-APIKEY': api_key
    }

    response = requests.request(method, url, headers=headers, json=payload)

    return response.json()


def coinswitch_api_validator():
    endpoint = "/trade/api/v2/validate/keys"
    method = "GET"
    payload = {}

    response = coinswitch_api_call(endpoint, method, {}, payload)

    print(response)

def main():
    # initialize the .env file
    load_dotenv()

    # call the coinswitch api validator
    coinswitch_api_validator()


if __name__ == '__main__':
    main()