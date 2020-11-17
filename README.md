# El-KOMERC

# How to start
## Install virtaul python environment():
- py -m pip install --user virtualenv

## Create virtual enviroment
- py -m venv env

## Turn on Virtual enviroment
- ./env/Script/activate/

## Install django and rest-framework and other modules:
- pip install -r requirements.txt --no-index --find-links file:///tmp/packages (run this from root folder)

## Start server:
- python manage.py runserver - (run this from root folder)

# API 

## Authentification / Accounts:
- >base-url/auth/   - get token
- >base-url/auth/registration/ - account registration


