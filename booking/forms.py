from django import forms

class DateForm(forms.Form):
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])


class BookingCancelForm(forms.Form):
    remarks = forms.CharField(widget=forms.Textarea())