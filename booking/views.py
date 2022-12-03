from django.shortcuts import render
from .models import Services, Availability, Details, PhoneDetails, CancellationController, PractitionerDetails
from .forms import BookingCancelForm, BookingForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User
from twilio.rest import Client
from datetime import datetime, timedelta
from django.utils import timezone


# Create your views here
@login_required
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)        

        if form.is_valid():
            booking_date = form.cleaned_data.get('date')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            service = form.cleaned_data.get('services')
            current_user = request.user

            service_id = service.split(' - ')[0]
            practitioner_name = service.split(' - ')[1]
            service_name = Services.objects.filter(service_id=service_id)[0].service_name
            duration = Services.objects.filter(service_id=service_id)[0].duration
            practitioner_username = PractitionerDetails.objects.filter(practitioner_name=practitioner_name)[0].username

            Details.objects.create(username=current_user,booking_date=booking_date,first_name=first_name,last_name=last_name,services=service_name,duration=duration,
            location='1800 Shepperd Avenue E, Unit 5, North York, M2J 5A7',practitioner_name=practitioner_name)

            userdetails = User.objects.filter(username=current_user)
            phone = PhoneDetails.objects.values('phone').get(username=current_user)['phone']
            booking_date_str = booking_date.strftime("%d-%b-%Y, %I:%M %p")
            account_sid = 'ACf763273bb4f4aa3a6a4a1992db020f70'
            auth_token = 'dc46ffb70c76a90b5265fe4d318b2aa8'
            client = Client(account_sid, auth_token)

            for user in userdetails:
                customer_email = user.email

            send_mail(
                'Booking Confirmation',
                'Your appointment with ' + practitioner_name + ' is successfully booked for ' + booking_date_str,
                None,
                [customer_email],
                fail_silently=False,
            )         

            
            client.messages.create(
                                        body=f'Your appointment with {practitioner_name} is successfully booked for ' + booking_date_str,
                                        from_='+1 865 568 8278',
                                        to=str(phone))



            userdetails = User.objects.filter(username=practitioner_username)
            phone = PhoneDetails.objects.values('phone').get(username=practitioner_username)['phone']

            for user in userdetails:
                customer_email = user.email
                
            send_mail(
                'Upcoming Booking',
                'You have an upcoming appointment scheduled with ' + first_name + ' ' + last_name + ' on ' + booking_date_str + ' for ' + service_name,
                None,
                [customer_email],
                fail_silently=False,
            )         

            
            client.messages.create(
                                        body=f'You have an upcoming appointment scheduled with {first_name} {last_name} on {booking_date_str} for {service_name}',
                                        from_='+1 865 568 8278',
                                        to=str(phone))


            return render(request, 'booking_success.html',{})
    else:
        form = BookingForm()
    return render(request,'booking.html', {'form':form})



@login_required
def bookingdetails(request,id):
    current_date =  datetime.now()

    current_user = request.user

    admin_details = User.objects.filter(username=current_user,is_superuser=1)
    practitioner_details = User.objects.filter(username=current_user,is_staff=1)

    booking_details = Details.objects.filter(id=id,booking_date__gte=current_date)
    past_booking_details = Details.objects.filter(id=id,booking_date__lt=current_date)
    cancel_enabled = CancellationController.objects.filter(username=current_user,is_login_disabled=0)

    return render(request, 'booking_details.html',{'booking_details':booking_details,'past_booking_details':past_booking_details,'admin_details':admin_details,'practitioner_details':practitioner_details,'cancel_enabled':cancel_enabled})


@login_required
def cancelbooking(request,id):
    if request.method == 'POST':
        form = BookingCancelForm(request.POST)
        if form.is_valid():
            current_user = request.user
            cancel_remarks = form.cleaned_data.get('remarks')
            booking_date = Details.objects.values('booking_date').get(id=id)['booking_date']
            booking_date_str = booking_date.strftime("%d-%b-%Y, %I:%M %p")

            admin_username = User.objects.values('username').get(is_superuser=1)['username']

            controller_id = CancellationController.objects.values('id').get(username=current_user)['id']
            no_of_cancels = CancellationController.objects.values('no_of_cancels').get(username=current_user)['no_of_cancels']
            is_login_disabled = CancellationController.objects.values('is_login_disabled').get(username=current_user)['is_login_disabled']

            current_date =  timezone.now()

            print()
            
            if no_of_cancels == 2 and ((booking_date - current_date) <= timedelta(hours=12)):
                no_of_cancels = no_of_cancels + 1
                is_login_disabled = 1    
                user_id = User.objects.values('id').get(username=current_user)['id']
                User.objects.filter(id=user_id).update(is_active=0)
                Details.objects.filter(id=id).update(is_active=0,cancel_remarks='Cancelled - Maximum no. of attempts exceeded')

                userdetails = User.objects.filter(username=current_user)
                phone = PhoneDetails.objects.values('phone').get(username=current_user)['phone']
                account_sid = 'ACf763273bb4f4aa3a6a4a1992db020f70'
                auth_token = 'dc46ffb70c76a90b5265fe4d318b2aa8'
                client = Client(account_sid, auth_token)

                for user in userdetails:
                    customer_email = user.email
                
                send_mail(
                    'Account Disabled',
                    'Your account is disabled since you have made more than 2 last moment cancellation/reschedule requests. Please contact the Salon for further details',
                    None,
                    [customer_email],
                    fail_silently=False,
                )

                client.messages.create(
                                        body=f'Your account is disabled since you have made more than 2 last moment cancellation/reschedule requests. Please contact the Salon for further details',
                                        from_='+1 865 568 8278',
                                        to=str(phone))       


                userdetails = User.objects.filter(username=admin_username)
                phone = PhoneDetails.objects.values('phone').get(username=admin_username)['phone']


                for user in userdetails:
                    admin_email = user.email

                send_mail(
                    'Account disabled for user '+ str(current_user),
                    'Account is disabled for user '+ str(current_user) +' since the user have made more than 2 last moment cancellation/reschedule requests.',
                    None,
                    [admin_email],
                    fail_silently=False,
                )

                client.messages.create(
                                        body=f'Account is disabled for user {str(current_user)} since user have made more than 2 last moment cancellation/reschedule requests.',
                                        from_='+1 865 568 8278',
                                        to=str(phone))   

            else:
                if (booking_date - current_date) <= timedelta(hours=12):
                    no_of_cancels = no_of_cancels + 1
                    is_login_disabled = 0
                
                Details.objects.filter(id=id).update(is_active=0,cancel_remarks=cancel_remarks)

                userdetails = User.objects.filter(username=current_user)
                phone = PhoneDetails.objects.values('phone').get(username=current_user)['phone']
                account_sid = 'ACf763273bb4f4aa3a6a4a1992db020f70'
                auth_token = 'dc46ffb70c76a90b5265fe4d318b2aa8'
                client = Client(account_sid, auth_token)
                practitioner_name = Details.objects.values('practitioner_name').get(id=id)['practitioner_name']
                practitioner_username = PractitionerDetails.objects.filter(practitioner_name=practitioner_name)[0].username

                for user in userdetails:
                    customer_email = user.email
                
                send_mail(
                    'Cancellation Confirmation',
                    'Your booking for '+ booking_date_str +' has been successfully cancelled',
                    None,
                    [customer_email],
                    fail_silently=False,
                )

                client.messages.create(
                                        body=f'Your booking for {booking_date_str} been successfully cancelled',
                                        from_='+1 865 568 8278',
                                        to=str(phone)) 

                
                userdetails = User.objects.filter(username=practitioner_username)
                phone = PhoneDetails.objects.values('phone').get(username=practitioner_username)['phone']

                for user in userdetails:
                    customer_email = user.email
                
                send_mail(
                    'Booking Cancelled',
                    'Your booking for '+ booking_date_str +' has been cancelled by the customer',
                    None,
                    [customer_email],
                    fail_silently=False,
                )

                client.messages.create(
                                        body=f'Your booking for {booking_date_str} has been cancelled by the customer',
                                        from_='+1 865 568 8278',
                                        to=str(phone))
            
            CancellationController.objects.filter(id=controller_id).update(no_of_cancels=no_of_cancels,is_login_disabled=is_login_disabled)

            cancelled_booking_details = Details.objects.filter(id=id)
                        
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
            service = form.cleaned_data.get('services')
            current_user = request.user

            service_id = service.split(' - ')[0]
            practitioner_name = service.split(' - ')[1]
            service_name = Services.objects.filter(service_id=service_id)[0].service_name
            duration = Services.objects.filter(service_id=service_id)[0].duration
            admin_username = User.objects.values('username').get(is_superuser=1)['username']
            new_practitioner_username = PractitionerDetails.objects.filter(practitioner_name=practitioner_name)[0].username

            old_practitioner_name = Details.objects.values('practitioner_name').get(id=id)['practitioner_name']
            old_practitioner_username = PractitionerDetails.objects.filter(practitioner_name=old_practitioner_name)[0].username

            booking_date_str = booking_date.strftime("%d-%b-%Y, %I:%M %p")

            controller_id = CancellationController.objects.values('id').get(username=current_user)['id']
            no_of_cancels = CancellationController.objects.values('no_of_cancels').get(username=current_user)['no_of_cancels']
            is_login_disabled = CancellationController.objects.values('is_login_disabled').get(username=current_user)['is_login_disabled']

            old_booking_date = Details.objects.values('booking_date').get(id=id)['booking_date']
            old_booking_date_str = old_booking_date.strftime("%d-%b-%Y, %I:%M %p")

            current_date =  timezone.now()

            if no_of_cancels == 2 and ((old_booking_date - current_date) <= timedelta(hours=12)):
                no_of_cancels = no_of_cancels + 1
                is_login_disabled = 1
                Details.objects.filter(id=id).update(is_active=0,cancel_remarks='Cancelled - Maximum no. of attempts exceeded')

                user_id = User.objects.values('id').get(username=current_user)['id']
                User.objects.filter(id=user_id).update(is_active=0)
                CancellationController.objects.filter(id=controller_id).update(no_of_cancels=no_of_cancels,is_login_disabled=is_login_disabled)

                userdetails = User.objects.filter(username=current_user)
                phone = PhoneDetails.objects.values('phone').get(username=current_user)['phone']
                account_sid = 'ACf763273bb4f4aa3a6a4a1992db020f70'
                auth_token = 'dc46ffb70c76a90b5265fe4d318b2aa8'
                client = Client(account_sid, auth_token)

                for user in userdetails:
                    customer_email = user.email
                
                send_mail(
                    'Account Disabled',
                    'Your account is disabled since you have made more than 2 last moment cancellation/reschedule requests. Please contact the Salon for further details',
                    None,
                    [customer_email],
                    fail_silently=False,
                )

                client.messages.create(
                                        body=f'Your account is disabled since you have made more than 2 last moment cancellation/reschedule requests. Please contact the Salon for further details',
                                        from_='+1 865 568 8278',
                                        to=str(phone))


                userdetails = User.objects.filter(username=admin_username)
                phone = PhoneDetails.objects.values('phone').get(username=admin_username)['phone']


                for user in userdetails:
                    admin_email = user.email

                send_mail(
                    'Account disabled for user '+ str(current_user),
                    'Account is disabled for user '+ str(current_user) +' since the user have made more than 2 last moment cancellation/reschedule requests.',
                    None,
                    [admin_email],
                    fail_silently=False,
                )

                client.messages.create(
                                        body=f'Account is disabled for user {str(current_user)} since user have made more than 2 last moment cancellation/reschedule requests.',
                                        from_='+1 865 568 8278',
                                        to=str(phone)) 
                
                return render(request, 'booking_failed.html',{})                
            else:
                if (old_booking_date - current_date) <= timedelta(hours=12):
                    no_of_cancels = no_of_cancels + 1
                    is_login_disabled = 0
                Details.objects.filter(id=id).update(is_active=0,cancel_remarks='Rescheduled')
                CancellationController.objects.filter(id=controller_id).update(no_of_cancels=no_of_cancels,is_login_disabled=is_login_disabled)

                userdetails = User.objects.filter(username=current_user)
                phone = PhoneDetails.objects.values('phone').get(username=current_user)['phone']
                account_sid = 'ACf763273bb4f4aa3a6a4a1992db020f70'
                auth_token = 'dc46ffb70c76a90b5265fe4d318b2aa8'
                client = Client(account_sid, auth_token)

                for user in userdetails:
                    customer_email = user.email
                    
                send_mail(
                    'Booking Confirmation',
                    'Your appointment is successfully rescheduled for ' + booking_date_str,
                    None,
                    [customer_email],
                    fail_silently=False,
                )

                client.messages.create(
                                        body=f'Your appointment is successfully rescheduled for ' + booking_date_str,
                                        from_='+1 865 568 8278',
                                        to=str(phone))

                
                
                userdetails = User.objects.filter(username=old_practitioner_username)
                phone = PhoneDetails.objects.values('phone').get(username=old_practitioner_username)['phone']

                for user in userdetails:
                    customer_email = user.email
                
                send_mail(
                    'Booking Cancelled',
                    'Your booking for '+ old_booking_date_str +' has been cancelled by the customer',
                    None,
                    [customer_email],
                    fail_silently=False,
                )

                client.messages.create(
                                        body=f'Your booking for {old_booking_date_str} has been cancelled by the customer',
                                        from_='+1 865 568 8278',
                                        to=str(phone))


                
                userdetails = User.objects.filter(username=new_practitioner_username)
                phone = PhoneDetails.objects.values('phone').get(username=new_practitioner_username)['phone']

                for user in userdetails:
                    customer_email = user.email
                
                send_mail(
                    'Upcoming Booking',
                    'You have an upcoming appointment scheduled with ' + first_name + ' ' + last_name + ' on ' + booking_date_str + ' for ' + service_name,
                    None,
                    [customer_email],
                    fail_silently=False,
                )

                client.messages.create(
                                        body=f'You have an upcoming appointment scheduled with {first_name} {last_name} on {booking_date_str} for {service_name}',
                                        from_='+1 865 568 8278',
                                        to=str(phone))
                
            

            Details.objects.create(username=current_user,booking_date=booking_date,first_name=first_name,last_name=last_name,services=service_name,duration=duration,
            location='1800 Shepperd Avenue E, Unit 5, North York, M2J 5A7',practitioner_name=practitioner_name)

            return render(request, 'booking_success.html',{})
    else:
        form = BookingForm()
    return render(request,'booking.html', {'form':form})


@login_required
def cancelledbookings(request):
    current_user = request.user
    is_admin = User.objects.values('is_superuser').get(username=current_user)['is_superuser']
    is_practitioner = User.objects.values('is_staff').get(username=current_user)['is_staff']

    if is_admin == 1:
        cancelled_booking_details = Details.objects.filter(is_active=0)

    elif is_practitioner == 1:
        practitioner_name = PractitionerDetails.objects.filter(username=current_user)[0].practitioner_name
        cancelled_booking_details = Details.objects.filter(is_active=0,practitioner_name=practitioner_name)

    else:
        cancelled_booking_details = Details.objects.filter(is_active=0,username=current_user)

    return render(request,'cancelled_bookings.html', {'cancelled_booking_details':cancelled_booking_details})
