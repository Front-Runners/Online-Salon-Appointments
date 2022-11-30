from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from verify_email.email_handler import send_verification_email
from booking.models import Details, PhoneDetails
from datetime import datetime,timedelta
from .validators import validate_verification
from django.utils import timezone

from django import forms
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            phone = form.cleaned_data.get('phone')
            username = form.cleaned_data.get('username')
            PhoneDetails.objects.create(username=username,phone=phone)
            return redirect('login') 
    else:
        form = UserRegisterForm()
    return render(request,'register.html', {'form': form})    
    
@login_required
def appointments(request):
    current_user = request.user
    current_date =  timezone.now() - timedelta(hours= 5)
    booking_details = Details.objects.filter(username=current_user,is_active=1,booking_date__gte=current_date)
    past_booking_details = Details.objects.filter(username=current_user,is_active=1,booking_date__lt=current_date)
    cancelled_booking_details = Details.objects.filter(username=current_user,is_active=0)
    return render(request,'appointments.html', {'booking_details':booking_details,'past_booking_details':past_booking_details,'cancelled_booking_details':cancelled_booking_details})




class LoginForm(AuthenticationForm):
    username = forms.CharField(
        validators=[validate_verification],
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
    
