from django.shortcuts import render

# Create your views here.
def brochure(request):
    return render(request, 'brochure.html', {})