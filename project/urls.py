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
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from users import views as users_view

urlpatterns = [
    path('booking/', include('booking.urls')),
    path('booking/<int:id>/', include('booking.urls')),
    path('booking/reschedule/<int:id>/', include('booking.urls')),
    path('booking/cancel/<int:id>/', include('booking.urls')),
    path('booking/cancelled_bookings', include('booking.urls')),
    path('brochure/', include('brochure.urls')),
    path('api/', include('api.urls')),
    path('appointments/', users_view.appointments, name='appointments'),
    path('about/', include('about.urls')),
    path('login/', auth_views.LoginView.as_view(template_name = 'login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'logout.html'), name='logout'),
    path('register/', include('users.urls')),
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('verification/', include('verify_email.urls')),
]
