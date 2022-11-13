from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from verify_email.email_handler import send_verification_email

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
    return render(request,'appointments.html', {})
    
