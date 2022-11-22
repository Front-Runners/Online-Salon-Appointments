from django.db import models
from django.urls import reverse
from datetime import datetime

# Create your models here.





class Services(models.Model):
    service_id = models.IntegerField(primary_key=True)
    service_name = models.CharField(max_length=150, help_text='Enter the service name')


    class Meta:
        ordering = ['service_name']

    
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.service_name


class Availability(models.Model):
    date = models.DateTimeField(null=True)
    is_available = models.SmallIntegerField(default=1)

    class Meta:
        ordering = ['date']

    
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.slot_start + " : " + self.slot_end


class Details(models.Model):
    booking_date = models.DateTimeField(null=True)
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150,null=False)
    last_name = models.CharField(max_length=150,null=False)
    location = models.CharField(max_length=150)
    services = models.CharField(max_length=500)
    is_active = models.IntegerField(default=1)


    class Meta:
        ordering = ['booking_date']

    
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.username + " : " + self.booking_date

    @property
    def is_past_due(self):
        return datetime.now() > self.booking_date