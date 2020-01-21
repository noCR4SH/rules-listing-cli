import http.client
import json
from dotenv import load_dotenv, find_dotenv
from os import environ as env

import constants

def get_token(client_id, client_secret, audience, domain):

    conn = http.client.HTTPSConnection(domain)

    payload = {'client_id': client_id, 'client_secret': client_secret, 'audience': audience, "grant_type": "client_credentials" }
    json_data = json.dumps(payload)

    headers = { 'content-type': "application/json" }

    conn.request("POST", "/oauth/token", json_data, headers)

    res = conn.getresponse()
    data = res.read()
    dict_res = json.loads(data)

    return dict_res

if __name__ == "__main__":

    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)

    AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
    AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
    AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
    AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)

    bearer_token = get_token(AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_AUDIENCE, AUTH0_DOMAIN)

    print(bearer_token)