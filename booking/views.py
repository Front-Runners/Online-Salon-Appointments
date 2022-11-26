from django.shortcuts import render
from .models import Services, Availability, Details, PhoneDetails
from .forms import BookingCancelForm, BookingForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User
from twilio.rest import Client
from datetime import datetime, timedelta


# Create your views here
@login_required
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)        

        if form.is_valid():
            booking_date = form.cleaned_data.get('date')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            service_id = form.cleaned_data.get('services')
            current_user = request.user

            service_name = Services.objects.filter(service_id=service_id)[0].service_name
            duration = Services.objects.filter(service_id=service_id)[0].duration

            Details.objects.create(username=current_user,booking_date=booking_date,first_name=first_name,last_name=last_name,services=service_name,duration=duration,
            location='1800 Shepperd Avenue E, Unit 5, North York, M2J 5A7')

            userdetails = User.objects.filter(username=current_user)
            phone = PhoneDetails.objects.values('phone').get(username=current_user)['phone']
            booking_date_str = booking_date.strftime("%d-%b-%Y, %I:%M %p")

            for user in userdetails:
                customer_email = user.email
            send_mail(
                'Booking Confirmation',
                'Your appointment is successfully booked for ' + booking_date_str,
                None,
                [customer_email],
                fail_silently=False,
            )

            account_sid = 'ACf763273bb4f4aa3a6a4a1992db020f70'
            auth_token = 'dc46ffb70c76a90b5265fe4d318b2aa8'
            client = Client(account_sid, auth_token)

            #reminder_date = datetime.strptime('26-Nov-2022, 01:25 AM','%d-%b-%Y, %I:%M %p')
            #print(reminder_date.isoformat())
            
            client.messages.create(
                                        body=f'Your appointment is successfully booked for ' + booking_date_str,
                                        from_='+1 865 568 8278',
                                        to=str(phone)
                                    )

            '''
            client.messages.create(
                                        body=f'Friendly reminder that you have an appointment scheduled for ' + booking_date_str,
                                        from_='+1 865 568 8278',
                                        to=str(phone),
                                        schedule_type='fixed',
                                        send_at='2022-11-26T01:30:00Z',
                                        messaging_service_sid='MG6d49dc7c69e422813b0c37553b8acc7a'
                                    )

            '''

            return render(request, 'booking_success.html',{})
    else:
        form = BookingForm()
    return render(request,'booking.html', {'form':form})



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
            phone = PhoneDetails.objects.values('phone').get(username=current_user)['phone']
            for user in userdetails:
                customer_email = user.email
            send_mail(
                'Cancellation Confirmation',
                'Your booking has been successfully cancelled',
                None,
                [customer_email],
                fail_silently=False,
            )

            account_sid = 'ACf763273bb4f4aa3a6a4a1992db020f70'
            auth_token = 'dc46ffb70c76a90b5265fe4d318b2aa8'
            client = Client(account_sid, auth_token)

            client.messages.create(
                                        body=f'Your booking has been successfully cancelled',
                                        from_='+1 865 568 8278',
                                        to=str(phone)
                                    )


            return render(request, 'booking_details.html',{'booking_details':cancelled_booking_details})
    else:
        form = BookingCancelForm()
    return render(request,'booking_cancel.html', {'form': form})


@login_required
def reschedulebooking(request,id):
    if request.method == 'POST':
        form = BookingForm(request.POST)        

        if form.is_valid():
            booking_date = form.cleaned_data.get('date')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            service_id = form.cleaned_data.get('services')
            current_user = request.user

            service_name = Services.objects.filter(service_id=service_id)[0].service_name
            duration = Services.objects.filter(service_id=service_id)[0].duration

            Details.objects.filter(id=id).update(is_active=0,cancel_remarks='Rescheduled')

            Details.objects.create(username=current_user,booking_date=booking_date,first_name=first_name,last_name=last_name,services=service_name,duration=duration,
            location='1800 Shepperd Avenue E, Unit 5, North York, M2J 5A7')

            userdetails = User.objects.filter(username=current_user)
            phone = PhoneDetails.objects.values('phone').get(username=current_user)['phone']
            booking_date = booking_date.strftime("%d-%b-%Y, %I:%M %p")

            for user in userdetails:
                customer_email = user.email
            send_mail(
                'Booking Confirmation',
                'Your appointment is successfully rescheduled for ' + booking_date,
                None,
                [customer_email],
                fail_silently=False,
            )

            account_sid = 'ACf763273bb4f4aa3a6a4a1992db020f70'
            auth_token = 'dc46ffb70c76a90b5265fe4d318b2aa8'
            client = Client(account_sid, auth_token)
            
            client.messages.create(
                                        body=f'Your appointment is successfully rescheduled for ' + booking_date,
                                        from_='+1 865 568 8278',
                                        to=str(phone)
                                    )


            return render(request, 'booking_success.html',{})
    else:
        form = BookingForm()
    return render(request,'booking.html', {'form':form})


@login_required
def cancelledbookings(request):
    current_user = request.user
    cancelled_booking_details = Details.objects.filter(username=current_user,is_active=0)
    return render(request,'cancelled_bookings.html', {'cancelled_booking_details':cancelled_booking_details})
