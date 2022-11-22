from django.shortcuts import render
from .models import Services, Availability, Details
from .forms import DateForm,BookingCancelForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User
from twilio.rest import Client

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


@login_required
def cancelbooking(request,id):
    if request.method == 'POST':
        form = BookingCancelForm(request.POST)
        if form.is_valid():
            cancel_remarks = form.cleaned_data.get('remarks')
            Details.objects.filter(id=id).update(is_active=0,cancel_remarks=cancel_remarks)
            cancelled_booking_details = Details.objects.filter(id=id)
            
            current_user = request.user
            userdetails = User.objects.filter(username=current_user)
            for user in userdetails:
                customer_email = user.email
            send_mail(
                'Cancellation Confirmation',
                'Your booking has been successfully Cancelled',
                None,
                [customer_email],
                fail_silently=False,
            )

            account_sid = 'ACf763273bb4f4aa3a6a4a1992db020f70'
            auth_token = 'dc46ffb70c76a90b5265fe4d318b2aa8'
            client = Client(account_sid, auth_token)

            client.messages.create(
                                        body=f'Your booking has been successfully Cancelled',
                                        from_='+1 865 568 8278',
                                        to='+1 647 862 6197' 
                                    )


            return render(request, 'booking_details.html',{'booking_details':cancelled_booking_details})
    else:
        form = BookingCancelForm()
    return render(request,'booking_cancel.html', {'form': form})


@login_required
def reschedulebooking(request,id):
    None