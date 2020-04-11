import json
import requests
import os

AUTH_ENDPOINT = "http://localhost:8000/api/auth/"
ACCOUNT_ENDPOINT = "http://localhost:8000/api/account/"

auth_request = {
    'email': 'sinisa9@gmail.com',
    'password': 'sicapica1412'
}
post_header = {
    'Content-Type': 'application/json'
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

pass_data = {
    'old_password': 'sicapica1412',
    'new_password': 'Krneki123!',
    'new_password2': 'Krneki123!'
}

img_path = os.path.join(os.getcwd(), "Screenshot_1.png")

#-----------------------------------------------------------------
def get_token(method="post", request={}, headers={}):
    if method == "post":
        jwt_response = requests.post(AUTH_ENDPOINT , data=json.dumps(request), headers=post_header)
        print("Token: "+str(jwt_response.json()['token']))

        return jwt_response.json()['token']

    return None

def update_account(data={},request= {},headers={}, img_path=None):
    token = get_token(request=request,headers=headers)

    jwt_header = {
        "Authorization": "JWT " + token
    }

    if img_path is None:
        get_response = requests.put(ACCOUNT_ENDPOINT+'9/', data=json.dumps(data),headers=jwt_header)
        print('\n'+str(get_response.text))
        print(get_response.status_code)
    else:
        file = {'profile_image': open(img_path, 'rb')}

        get_response = requests.put(ACCOUNT_ENDPOINT+'9/', data=data, files=file, headers=jwt_header)
        print('\n'+str(get_response.text))
        print(get_response.status_code)

def change_password(data={},request={}, headers={}):
    token = get_token(request=request,headers=headers)

    jwt_header = {
        'Content-Type': 'application/json',
        "Authorization": "JWT " + token
    }

    get_response = requests.put(ACCOUNT_ENDPOINT+'change-password/9/', data=json.dumps(data), headers=jwt_header)
    print('\n'+str(get_response.text))
    print(get_response.status_code)

#-----------------------------------------------------------------
update_account(data=data, request=auth_request, headers=post_header, img_path=img_path)
