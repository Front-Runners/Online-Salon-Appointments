from django import forms
from .models import Services
from .validators import validate_availability

class BookingForm(forms.Form):
    choices=[]
    services = Services.objects.values('service_id','service_name')

    for i in services:
        choices.append((str(i['service_id']),i['service_name']))

    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], label='Date & Time', validators = [validate_availability])
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)    
    services = forms.CharField(label='Please select the service',widget = forms.Select(choices=choices))

    field_order = ['date','first_name','last_name','services']

class BookingCancelForm(forms.Form):
    remarks = forms.CharField(widget=forms.Textarea())