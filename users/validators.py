#validators.py
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from booking.models import PhoneDetails

def validate_email(value):
    if User.objects.filter(email = value).exists():
        raise ValidationError(
            ("Email already taken."),
            params = {'value':value}
        )


def validate_phone(value):
    if PhoneDetails.objects.filter(phone = value).exists():
        raise ValidationError(
            ("Phone number already taken."),
            params = {'value':value}
        )

def validate_verification(value):
    if User.objects.values('is_active').get(username=value)['is_active'] == 0:
        print('Success')
        raise ValidationError(
            ("Email not yet verified"),
            params = {'value':value}
        )