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

    for rule in json_response:
        cleaned_script = re.sub(r"[^\w]", " ",  rule['script']).split()
        rule['cleaned_script'] = cleaned_script

    return json_response

def get_clients(access_token, audience):
    print("Gettings clients....")

    headers = { 'authorization': access_token["token_type"] + " " + access_token["access_token"] }

    response = requests.get(audience + "clients?fields=client_id%2Cname&include_fields=true", headers=headers)

    json_response = response.json()
    return json_response

def find_client(rules, clients):

    for client in clients:
        for rule in rules:
            if client['name'] in rule['cleaned_script'] or client['client_id'] in rule['cleaned_script']:
                rule['client_name'] = client['name']
                rule['client_id'] = client['client_id']
            else:
                rule['client_name'] = "none"
                rule['client_id'] = "none"

    for i in rules:
        try:
            del i['script']
            del i['cleaned_script']
        except KeyError:
            print("Key not found")

    return rules

def generate_csv(dict_data, filename):
    csv_columns = ['id', 'enabled', 'name', 'order', 'stage', 'client_name', 'client_id']

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
    clients_data = get_clients(bearer_token, AUTH0_AUDIENCE)
    final_data = find_client(fetched_rules, clients_data)

    csv_name = str(input("Provide name for the file: "))

    generate_csv(final_data, csv_name)