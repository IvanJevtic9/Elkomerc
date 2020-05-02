from django.core.validators import RegexValidator

password_validator1 = RegexValidator(regex=r'^.*[0-9].*$', message="MUST_CONTAIN_DIGIT")
password_validator2 = RegexValidator(regex=r'.*[A-Z].*$', message="MUST_CONTAIN_UPARCASE")
password_validator3 = RegexValidator(regex=r'.*[a-z].*$', message="MUST_CONTAIN_LOWERCASE")
password_validator4 = RegexValidator(regex=r'^(.*){6,}$', message="MUST_CONTAIN_AT_LAST_SIX_CHARACTERS")