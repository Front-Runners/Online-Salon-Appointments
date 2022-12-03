from django.shortcuts import render, redirect
from .forms import UserRegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from verify_email.email_handler import send_verification_email
from booking.models import Details, PhoneDetails, PractitionerDetails, CancellationController
from datetime import datetime,timedelta
from django.utils import timezone
from django.contrib.auth.models import User



# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            phone = form.cleaned_data.get('phone')
            username = form.cleaned_data.get('username')
            PhoneDetails.objects.create(username=username,phone=phone)
            CancellationController.objects.create(username=username, no_of_cancels=0,is_login_disabled=0)
            return redirect('login') 
    else:
        form = UserRegisterForm()
    return render(request,'register.html', {'form': form})    
    
@login_required
def appointments(request):
    current_user = request.user

    is_admin = User.objects.values('is_superuser').get(username=current_user)['is_superuser']
    is_practitioner = User.objects.values('is_staff').get(username=current_user)['is_staff']
    current_date =  timezone.now()
    admin_details = User.objects.filter(username=current_user,is_superuser=1)
    practitioner_details = User.objects.filter(username=current_user,is_staff=1)

    if ((is_admin == 0) and (is_practitioner == 0)):
        booking_details = Details.objects.filter(username=current_user,is_active=1,booking_date__gte=current_date)
        past_booking_details = Details.objects.filter(username=current_user,is_active=1,booking_date__lt=current_date)
        cancelled_booking_details = Details.objects.filter(username=current_user,is_active=0)
    elif ((is_admin == 1) and (is_practitioner == 0)):
        booking_details = Details.objects.filter(is_active=1,booking_date__gte=current_date)
        past_booking_details = Details.objects.filter(is_active=1,booking_date__lt=current_date)
        cancelled_booking_details = Details.objects.filter(is_active=0)
    elif ((is_admin == 0) and (is_practitioner == 1)):
        practitioner_name = PractitionerDetails.objects.filter(username=current_user)[0].practitioner_name
        booking_details = Details.objects.filter(is_active=1,booking_date__gte=current_date,practitioner_name=practitioner_name)
        past_booking_details = Details.objects.filter(is_active=1,booking_date__lt=current_date,practitioner_name=practitioner_name)
        cancelled_booking_details = Details.objects.filter(is_active=0,practitioner_name=practitioner_name)
    
    return render(request,'appointments.html', {'booking_details':booking_details,'past_booking_details':past_booking_details,'cancelled_booking_details':cancelled_booking_details, 'admin_details':admin_details, 'practitioner_details':practitioner_details})



def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return redirect('appointments')
    else:
        form = LoginForm()
    return render(request,'register.html', {'form': form})   


    
