# El-KOMERC

# How to start
## Install virtaul python environment():
- py -m pip install --user virtualenv

## Create virtual enviroment
- py -m venv env

## Turn on Virtual enviroment
- ./env/Script/activate/
### if Activate.ps1 is disabled on the system run:
-- Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted

## Install django and rest-framework and other modules:
- pip install -r requirements.txt --no-index --find-links file:///tmp/packages (run this from root folder)

## Start server:
- python manage.py runserver - (run this from root folder)

# API 

## Authentification / Accounts:
- >base-url/auth/   - get token
- >base-url/auth/registration/ - account registration


