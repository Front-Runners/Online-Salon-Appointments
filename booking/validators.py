from django.core.exceptions import ValidationError
from .models import Details
from django.utils import timezone
from django.db.models import F


def validate_availability(value):

    if value <= timezone.now():
        raise ValidationError(
            ("Please choose a future date and time."),
            params = {'value':value}
        ) 

    if Details.objects.filter(booking_date__lte = value, booking_date__gte = value - F('duration'), is_active = 1).exists():
        raise ValidationError(
            ("Date and time already booked. Please choose a different slot."),
            params = {'value':value}
        )