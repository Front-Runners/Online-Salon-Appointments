"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking, name='booking'),
    path('<int:id>/', views.bookingdetails, name='bookingdetails'),
    path('reschedule/<int:id>/', views.reschedulebooking, name='reschedulebooking'),
    path('cancel/<int:id>/', views.cancelbooking, name='cancelbooking'),
    path('cancelled_bookings/', views.cancelledbookings, name='cancelledbookings')
]
