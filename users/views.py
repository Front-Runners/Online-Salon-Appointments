from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from verify_email.email_handler import send_verification_email
from booking.models import Details

from django import forms
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            return redirect('login') 
    else:
        form = UserRegisterForm()
    return render(request,'register.html', {'form': form})    
    
@login_required
def appointments(request):
    current_user = request.user
    booking_details = Details.objects.filter(username=current_user,is_active=1)
    return render(request,'appointments.html', {'booking_details':booking_details})




class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='user',
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'username or email',
            }
        )
    )

    password = forms.CharField(
        label='', 
        widget=forms.PasswordInput(
            attrs = {
                'placeholder': 'password'
            }
        )
    )
    
