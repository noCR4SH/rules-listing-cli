# rules-listing-cli
Simple tool for generating CSV report with rules and assigned applications

#### Installation

1. Download or clone the repository
2. Install all the dependencies
`pip install -r requirements.txt`
3. Create .env file for storing sensitive content. Template:
  ```markdown
AUTH0_CLIENT_ID=<client_id of you M2M application>
AUTH0_DOMAIN=<tenant name>.auth0.com
AUTH0_CLIENT_SECRET=<secret key for client_id>
AUTH0_AUDIENCE=https://<tenant name>.com/api/v2/
```
4. Run the script:
`python main.py`
