import requests
import json
from dotenv import load_dotenv, find_dotenv
from os import environ as env

import constants

def get_token(client_id, client_secret, audience, domain):

    headers = { 'content-type': "application/json" }
    data = { 'client_id': client_id, 'client_secret': client_secret, 'audience': audience, "grant_type": "client_credentials" }
    
    response = requests.post("https://" + domain + "/oauth/token", json=data, headers=headers)
    
    json_response = response.json()
    print(json_response)

    return json_response

def get_rules(access_token, audience):
    
    headers = { 'authorization': access_token["token_type"] + " " + access_token["access_token"] }

    response = requests.get(audience + "rules", headers=headers)

    json_response = response.json()
    print(json_response)

if __name__ == "__main__":

    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)

    AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
    AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
    AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
    AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)

    bearer_token = get_token(AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_AUDIENCE, AUTH0_DOMAIN)
    
    get_rules(bearer_token, AUTH0_AUDIENCE)