from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.validators import validate_email,validate_phone
from phonenumber_field.formfields import PhoneNumberField

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(validators = [validate_email])
    phone = PhoneNumberField(validators = [validate_phone])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

