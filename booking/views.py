from django.shortcuts import render
from .models import Services, Availability, Details
from .forms import DateForm
from django.contrib.auth.decorators import login_required
from datetime import datetime

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
    current_date =  datetime.now()
    booking_details = Details.objects.filter(id=id,booking_date__gte=current_date)
    past_booking_details = Details.objects.filter(id=id,booking_date__lt=current_date)
    return render(request, 'booking_details.html',{'booking_details':booking_details,'past_booking_details':past_booking_details})