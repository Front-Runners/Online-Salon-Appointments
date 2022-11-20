from django.shortcuts import render
from booking.models import Services

# Create your views here.
def brochure(request):
    services = Services.objects.all()

    context = {
        'services': services,
        }

    return render(request, 'brochure.html', context)