from django.core.exceptions import ValidationError
from .models import Details
from django.utils import timezone
from django.db.models import F
from datetime import timedelta


def validate_availability(value):
    None
'''
    if value <= timezone.now():
        raise ValidationError(
            ("Please choose a future date and time."),
            params = {'value':value}
        ) 

    booking_dates_dict={}
    booking_dates = Details.objects.values('booking_date','duration')

    for i in booking_dates:
        booking_dates_dict[i['booking_date']] = i['duration']

    for k,v in booking_dates_dict.items():
        if ((value >= k) and (value <= (k + timedelta(hours= v)))) or ((value >= k) and (value <= (k + timedelta(hours= v)))):
            raise ValidationError(
            ("Date and time already booked. Please choose a different slot."),
            params = {'value':value}
        )



    if Details.objects.filter(booking_date__lte = value, booking_date__gte = value - F('duration'), is_active = 1).exists():
        raise ValidationError(
            ("Date and time already booked. Please choose a different slot."),
            params = {'value':value}
        )


    '''