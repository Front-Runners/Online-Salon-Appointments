from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.
def home(request):
    return render(request, 'home_page.html', {})