from django import forms
from .models import Services


choices=[]
services = Services.objects.values('service_id','service_name')

for i in services:
    choices.append((str(i['service_id']),i['service_name']))

print(choices)

class BookingForm(forms.Form):
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], label='Date & Time')
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)    
    services = forms.CharField(label='Please select the service',widget = forms.Select(choices=choices))



class BookingCancelForm(forms.Form):
    remarks = forms.CharField(widget=forms.Textarea())