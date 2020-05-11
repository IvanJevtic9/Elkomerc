from django.conf import settings
from time import timezone
import datetime

expire_delta = settings.JWT_AUTH['JWT_EXPIRATION_DELTA']

def jwt_response_payload_handler(token, email=None, account_id=None):
    return {
        'token': token,
        'email': email,
        'local_id': account_id,
        'expires': datetime.datetime.now() + expire_delta
    }