import json
import random
import requests
import string
from urllib.parse import urlparse, parse_qs

def linkedin_auth(credentials_filename="credentials.json"):
    def read_creds(filename):
        with open(filename) as f:
            return json.load(f)

    def save_token(filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def create_CSRF_token():
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(20))

    def open_url(url):
        import webbrowser
        print(url)
        webbrowser.open(url)

    def authorize(api_url, client_id, client_secret, redirect_uri):
        csrf_token = create_CSRF_token()
        params = {
            'response_type': 'code',
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'state': csrf_token,
            'scope': 'openid,profile,w_member_social,email'
        }

        response = requests.get(f'{api_url}/authorization', params=params)

        open_url(response.url)

        redirect_response = input('Paste the full redirect URL here:')
        url = urlparse(redirect_response)
        query = parse_qs(url.query)
        if 'code' in query:
            return query['code'][0]
        else:
            raise ValueError('Authorization code not found in the redirect URL.')

    def refresh_token(auth_code, client_id, client_secret, redirect_uri):
        access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'

        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        }

        response = requests.post(access_token_url, data=data, timeout=30)
        if response.ok:
            response_data = response.json()
            access_token = response_data.get('access_token')
            if access_token:
                return access_token
            else:
                raise ValueError('Access token not found in the response.')
        else:
            response.raise_for_status()

    creds = read_creds(credentials_filename)
    client_id, client_secret = creds['client_id'], creds['client_secret']
    redirect_uri = creds['redirect_uri']
    api_url = 'https://www.linkedin.com/oauth/v2'

    if 'access_token' not in creds:
        auth_code = authorize(api_url, client_id, client_secret, redirect_uri)
        access_token = refresh_token(auth_code, client_id, client_secret, redirect_uri)
        creds['access_token'] = access_token
        save_token(credentials_filename, creds)
    else:
        access_token = creds['access_token']
        print("Access Token found in credentials.json:", access_token)

    return access_token

if __name__ == '__main__':
    access_token = linkedin_auth()
