import json
import requests
import os

ACCOUNT_ENDPOINT = "http://localhost:8000/api/account/"
AUTH_ENDPOINT = "http://localhost:8000/api/auth/"

auth_request = {
    'email': 'sinisa9@gmail.com',
    'password': 'sicapica1412'
}
post_header = {
    'Content-Type': 'application/json'
}

jwt_response = requests.post(AUTH_ENDPOINT, data=json.dumps(auth_request),headers=post_header)
token = jwt_response.json()['token']
print("Token: "+str(token))

jwt_header = {
    'Content-Type': 'application/json',
    "Authorization": "JWT " + token
}

data = {
    'email': 'sinisa9@gmail.com',
    'address': 'Volgina 20a',
    'city': 'Vranjani',
    'phone_number': '0642502565',
    'account_type': 'USR',
    'first_name': 'Sinisa',
    'last_name': 'Djokic',
    'date_of_birth': '2001-08-18'
}
get_response = requests.put(ACCOUNT_ENDPOINT+'9/', data=json.dumps(data),headers=jwt_header)
print('\n'+str(get_response.text))
print(get_response.status_code)

data = {
    'old_password': 'sicapica1412',
    'new_password': 'Krneki123!',
    'new_password2': 'Krneki123!'
}
get_response = requests.put(ACCOUNT_ENDPOINT+'change-password/9/', data=json.dumps(data),headers=jwt_header)
print('\n'+str(get_response.text))
print(get_response.status_code)