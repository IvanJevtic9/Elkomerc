import json
import requests
from django.conf import settings

AUTH_ENDPOINT = "http://localhost:8000/api/auth/"
IMPORT_ENDPOINT = "http://localhost:8000/api/product/articles/import/"
FILE_PATH = "D:\source\DjangoRepos\Elkomerc\static\exel_files\importArt.xlsx"

auth_header = {
    "email": "ijevtic459@gmail.com",
    "password": "akudlola1412"
}

post_header = {
    'Content-Type': 'application/json'
}

response = requests.post(AUTH_ENDPOINT, data=json.dumps(auth_header), headers=post_header)
print(response.status_code)
token = response.json()['token']

print(token+"\n")

jwt_header = {
    "Authorization": "JWT " + token
}

file_import = {'file_import': open(FILE_PATH, 'rb')}

get_response = requests.post(IMPORT_ENDPOINT, data={} , files=file_import, headers=jwt_header)

print(get_response.text)
print(" "+str(get_response.status_code)
