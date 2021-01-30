from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, account, timestamp):
        return (
            text_type(account.id) + text_type(timestamp) +
            text_type(account.is_active)
        )

account_activation_token = TokenGenerator()
account_change_password_token = TokenGenerator()