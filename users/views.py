from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .forms import PostForm
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
def profile(request):
    form = PostForm(request.POST)
    if form.is_valid():
        form.save()
        form = PostForm()
    return render(request,'profile.html', {'form': form})
    
