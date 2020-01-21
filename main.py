import requests
import re
import json
import csv
from dotenv import load_dotenv, find_dotenv
from os import environ as env

import constants

def get_token(client_id, client_secret, audience, domain):
    print("Requesting bearer token...")

    headers = { 'content-type': "application/json" }
    data = { 'client_id': client_id, 'client_secret': client_secret, 'audience': audience, "grant_type": "client_credentials" }
    
    response = requests.post("https://" + domain + "/oauth/token", json=data, headers=headers)
    
    json_response = response.json()

    return json_response

def get_rules(access_token, audience):
    print("Getting rules...")

    headers = { 'authorization': access_token["token_type"] + " " + access_token["access_token"] }

    response = requests.get(audience + "rules", headers=headers)

    json_response = response.json()
    return json_response

def find_client(rules):
    pattern = r"(context.+\')"

    for rule in rules:
        m = re.findall(pattern, rule['script'])
        if m:
            n = re.findall(r"'(.*?)'", m[0])
            rule['client_name'] = n[0]
        else:    
            rule['client_name'] = "none"
        try:
            del rule['script']
        except KeyError:
            print("Key not found")

    return rules    

def generate_csv(dict_data, filename):
    csv_columns = ['id', 'enabled', 'name', 'order', 'stage', 'client_name']

    print("Generating CSV file...")

    with open(filename, 'w') as f:
        w = csv.DictWriter(f, fieldnames=csv_columns)
        w.writeheader()
        for data in dict_data:
            w.writerow(data)

    print("Done!")

if __name__ == "__main__":

    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)

    AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
    AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
    AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
    AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)

    bearer_token = get_token(AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_AUDIENCE, AUTH0_DOMAIN)
    
    fetched_rules = get_rules(bearer_token, AUTH0_AUDIENCE)
    
    final_data = find_client(fetched_rules)
    
    csv_name = str(input("Provide name for the file: "))

    generate_csv(final_data, csv_name)