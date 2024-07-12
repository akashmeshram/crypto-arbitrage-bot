from app.utils import coinswitch_api_call

def coinswitch_api_validator():
    endpoint = "/trade/api/v2/validate/keys"
    method = "GET"
    payload = {}

    response = coinswitch_api_call(endpoint, method, {}, payload)

    print(response)


def coinswitch_api_get_pairs():
    endpoint = "/trade/api/v2/24hr/all-pairs/ticker"
    method = "GET"
    params = { "exchange": "coinswitchx"}

    response = coinswitch_api_call(endpoint, method, params, {})

    print(response)