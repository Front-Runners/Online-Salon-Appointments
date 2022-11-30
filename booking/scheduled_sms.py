from .models import Details,PhoneDetails
from datetime import timedelta
from django.utils import timezone
from twilio.rest import Client

def send_reminder():
    current_date =  timezone.now()

    bookings=[]
    bookings_dict ={}
    booking_details = Details.objects.filter(booking_date__gte=current_date,is_active=1,is_reminder_sent=0).values('id','booking_date')

    for i in booking_details:
        bookings_dict ={}
        bookings_dict[i['id']]=i['booking_date']
        bookings.append(bookings_dict)

    for i in bookings: 
        for key,value in i.items():
            username = Details.objects.values('username').get(id=key)['username']
            phone = PhoneDetails.objects.values('phone').get(username=username)['phone']
            booking_date_str = value.strftime("%d-%b-%Y, %I:%M %p")
            
            sms_date = value - timedelta(days = 1)
            
            if current_date>=sms_date:
                account_sid = 'ACf763273bb4f4aa3a6a4a1992db020f70'
                auth_token = 'dc46ffb70c76a90b5265fe4d318b2aa8'
                client = Client(account_sid, auth_token)

    
                client.messages.create(
                                        body=f'Friendly reminder that you have an appointment scheduled for ' + booking_date_str,
                                        from_='+1 865 568 8278',
                                        to=str(phone)
                                    )   

                Details.objects.filter(id=key).update(is_reminder_sent=1)
