from django import forms
from .models import Services
from .validators import validate_availability
from .models import Details, PractitionerDetails
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

class BookingForm(forms.Form):
    choices=[]
    
    services = Services.objects.values('service_id','service_name')
    practitioners = PractitionerDetails.objects.values('practitioner_name','service_id')
    for i in services:
        for j in practitioners:
            if i['service_id'] == j['service_id']:
                choices.append((str(i['service_id']) + ' - ' + j['practitioner_name'],i['service_name'] + ' - ' + j['practitioner_name']))

    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], label='Date & Time')
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)    
    services = forms.CharField(label='Please select the service',widget = forms.Select(choices=choices))

    field_order = ['date','first_name','last_name','services']

    def clean(self):
        cleaned_data = super(BookingForm, self).clean()
        booking_date = cleaned_data.get("date")
        service = cleaned_data.get("services")

        service_id = service.split(' - ')[0]
        
        duration = Services.objects.filter(service_id=service_id)[0].duration

        if booking_date <= timezone.now() - timedelta(hours= 5):
            raise forms.ValidationError(
            ("Please choose a future date and time.")
        )

        if int(booking_date.strftime("%H")) < 9 or int(booking_date.strftime("%H")) > 20:
            raise forms.ValidationError(
            ("Please choose a time between 9AM and 8PM")
        ) 

        booking_dates_dict={}
        booking_dates = Details.objects.values('booking_date','duration')

        for i in booking_dates:
            booking_dates_dict[i['booking_date']] = i['duration']

        for k,v in booking_dates_dict.items():
            if ((booking_date >= k) and (booking_date <= (k + timedelta(hours= v)))) or (((booking_date + timedelta(hours= duration)) >= k) and ((booking_date + timedelta(hours= duration)) <= (k + timedelta(hours= v)))):
                raise forms.ValidationError(
                ("Date and time already booked. Please choose a different slot.")
            )

        return cleaned_data

class BookingCancelForm(forms.Form):
    remarks = forms.CharField(widget=forms.Textarea())