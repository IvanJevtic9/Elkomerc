from django.conf import settings
from time import timezone
import datetime

expire_delta = settings.JWT_AUTH['JWT_EXPIRATION_DELTA']

def jwt_response_payload_handler(token, email=None, account_id=None, is_stuff=None):
    return {
        'token': token,
        'email': email,
        'local_id': account_id,
        'is_stuff': is_stuff,
        'expires': datetime.datetime.now() + expire_delta
    }