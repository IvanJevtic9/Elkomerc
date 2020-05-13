import json
import requests
import os

AUTH_ENDPOINT = "http://localhost:8000/api/auth/"
WISHLIST_ENDPOINT = "http://localhost:8000/api/accounts/wishlist/"

auth_request = {
    'email': 'bok@gmail.com',
    'password': 'akudlola1412'
}
post_header = {
    'Content-Type': 'application/json'
}

jwt_response = requests.post(
    AUTH_ENDPOINT, data=json.dumps(auth_request), headers=post_header)

token = jwt_response.json()['token']

jwt_header = {
    "Authorization": "JWT " + token
}

response = requests.get(WISHLIST_ENDPOINT,data=json.dumps({}),headers=jwt_header)
print(response.text)