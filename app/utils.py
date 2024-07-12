from dotenv import load_dotenv
import os
from cryptography.hazmat.primitives.asymmetric import ed25519
from urllib.parse import urlparse, urlencode
import urllib
import requests
import time

def coinswitch_api_call(endpoint, method, params, payload):
    # get the api key and secret key from the environment variables
    api_key = os.getenv('COINSWITCH_API_KEY')
    secret_key = os.getenv('COINSWITCH_API_SECRET')
    epoch_time = str(int(time.time() * 1000))

    # create the signature
    unquote_endpoint = endpoint
    if method == "GET" and len(params) != 0:
        endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)
        unquote_endpoint = urllib.parse.unquote_plus(endpoint)

    signature_msg = method + unquote_endpoint + epoch_time

    request_string = bytes(signature_msg, 'utf-8')
    secret_key_bytes = bytes.fromhex(secret_key)
    secret_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key_bytes)
    signature_bytes = secret_key.sign(request_string)
    signature = signature_bytes.hex()

    # make the request
    url = "https://coinswitch.co" + endpoint

    headers = {
    'Content-Type': 'application/json',
    'X-AUTH-SIGNATURE': signature,
    'X-AUTH-APIKEY': api_key,
    'X-AUTH-EPOCH': epoch_time
    }

    response = requests.request(method, url, headers=headers, json=payload)

    return response.json()

