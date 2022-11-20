from django.shortcuts import render
from .models import Services, Availability, Details
from .forms import DateForm
from django.contrib.auth.decorators import login_required

# Create your views here
@login_required
def booking(request):
    services = Services.objects.all()
    availability = Availability.objects.all()
    form = DateForm()

    context = {
        'services': services,
        'availability': availability,
        'form': form
        }


    return render(request, 'booking.html',context)

@login_required
def bookingdetails(request,id):
    booking_details = Details.objects.filter(id=id)
    return render(request, 'booking_details.html',{'booking_details':booking_details})