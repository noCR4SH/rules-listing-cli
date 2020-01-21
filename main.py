import http.client
import json
from dotenv import load_dotenv, find_dotenv
from os import environ as env

import constants

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)

conn = http.client.HTTPSConnection(AUTH0_DOMAIN)

payload = {'client_id': AUTH0_CLIENT_ID, 'client_secret': AUTH0_CLIENT_SECRET, 'audience': AUTH0_AUDIENCE, "grant_type": "client_credentials" }
json_data = json.dumps(payload)

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", json_data, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))