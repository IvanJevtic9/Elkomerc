import json
import requests
import os

AUTH_ENDPOINT = "http://localhost:8000/api/auth/"

auth_request = {
    'email': 'ijevtic459@gmail.com',
    'password': 'akudlola1412'
}
post_header = {
    'Content-Type': 'application/json'
}

jwt_response = requests.post(AUTH_ENDPOINT, data=json.dumps(auth_request),headers=post_header)
token = jwt_response.json()['token']
print("Token: "+str(token))

data = {
    'email': 'sinisa.djokic17@gmail.com',
    'password': 'akudlola1412',
    'password2': 'akudlola1412',
    'address': 'BB',
    'city': 'Pozega',
    'phone_number': '0642502565',
    'account_type': 'USR',
    'first_name': 'Sinisa',
    'last_name': 'Djokic',
    'date_of_birth': '2001-08-17'
}

get_response = requests.post(AUTH_ENDPOINT+'register/', data=json.dumps(data),headers=post_header)
print('\n'+str(get_response.text))
print(get_response.status_code)
