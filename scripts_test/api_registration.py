import json
import requests
import os

AUTH_ENDPOINT = "http://localhost:8000/api/auth/"

auth_request = {
    'email': 'jecajevtic2005.com',
    'password': 'akudlola1412'
}
post_header = {
    'Content-Type': 'application/json'
}

data = {
    'email': 'jecajevtic2005@gmail.com',
    'password': 'Kakao123!',
    'password2': 'Kakao123!',
    'address': 'Volgina 20a',
    'city': 'Beograd Zvezdara',
    'zip_code': "11050",
    'phone_number': '0658058009',
    'account_type': 'USR',
    "data": {
        'first_name': 'Jelena',
        'last_name': 'Jevtic',
        'date_of_birth': '1995-10-16'
    }
}

# -------------------------------------------------------------------------------------------


def get_auth_url():
    return AUTH_ENDPOINT


def get_token(method="post", auth_request={}, headers={}):
    if method == "post":
        jwt_response = requests.post(
            get_auth_url(), data=json.dumps(auth_request), headers=post_header)
        print("Token: "+str(jwt_response.json()['token']))

        return jwt_response.json()['token']

    return None

# For registration we do not need auth token


def registration(method='post', data={}, headers={}):

    if method == "post":
        get_response = requests.post(
            get_auth_url()+'register/', data=json.dumps(data), headers=post_header)
        print('\n'+str(get_response.text))
        print(get_response.status_code)


# ----------------------------------------------------------------------------------------------

registration(data=data, headers=post_header)
