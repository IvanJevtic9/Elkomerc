# El-KOMERC

# How to start
## Install virtaul python environment():
- py -m pip install --user virtualenv

## Create virtual enviroment
- py -m venv env

## Turn on Virtual enviroment
- .\env\Scripts\activate
### if Activate.ps1 is disabled on the system run:
-- Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted

## Install django and rest-framework and other modules:
- pip install -r requirements.txt
- If you have problem with run server command after running this command, you will need to maually install each lib you got problem with. 

## Start django server:
- python manage.py runserver - (run this from root folder)
## Start redis server (You have to download redis first):
- Navigate to the redis folder and run command - redis-server

## Starting celary (scheduler):
- celery -A Elkomerc beat -l info
- celery -A Elkomerc worker -l info -P solo
- monitoring: celery flower -A Elkomerc --port=5555 

# API 

## Authentification / Accounts:
- >base-url/auth/   - get token
- >base-url/auth/registration/ - account registration


