# Online-Salon-Appointments
Repository for code

## *The Project*
An online platform which facilitates the customers to plan and schedule hair salon services


## *About the team and the project*

![logo](https://user-images.githubusercontent.com/17834899/205514008-0b220eb7-7e0f-4b57-8c8c-5a1ef6fdc91d.png)

Team Front Runners is representing a project which will make the scheduling and planning of personal services easy and efficient.
The objective of this project is to develop a user-friendly website where customers can book their salon appointment for hair services.
Our system will schedule the appointment according to the availability of practitioners and will give timely notifications before their appointment.
Moreover, this system will allow the customers to manage their services.
If they have any personal engagement, they can reschedule or cancel their appointments by providing valid reasons.
This will be convenient and easy for the customers especially in their busy lives.



## *Work flow*
In this website, there are three types of login modes:
+ Customer
+ Practitioner
+ Admin


Customers and Practitioners can register their account through the Sign Up page. The email and mobile number should be unique. Passwords should meet minimum requirements as provided by the website.
>For admins, the account will be registered by our backend team at Front Runners and the credentials will be shared seperately
>Registered practitioners will be promoted as staff by our backend team at Front Runners

Post signup, the user will get a verification mail. He will be able to login only after successfull mail verification. 

Once logged in, customer will be automatically redirected to the Apppointments page, where he can vew upcoming bookings, past bookings and also book a new appointment.

In the Upcoming bookings, the customer can view his booking details page where he can either cancel or reschedule the appointment. Whenever a customer books an appointment, sms and mail will be triggered for both the customer as well as the practitioner. Mail and sms will be triggered for both cancellation and rescheduling.
A reminder sms will be sent to customers one day before the booking date.

> Customer will be allowed to cancel/rescheduled appointments scheduled within the next 12 hours upto 2 times only. Post which the account will get disabled.
> Once disabled both customer and the admin will get mail and sms regarding the account lock.



## *Code Organization*
In this web application project, the code is divided into different applications, each component like the home page, about page, booking page is an application here. All project conmfiguration details
are located in the file [./project/settings.py](../../project/settings.py) . Here we have mentioned the installed applications details, database connection details, SMTP server details etc. To run the server, [./manage.py](url) file is used.

Once the server starts, based on the URL provided in the browser, its matched with the URLs present in [./project/urls.py](url) . When the matched URL is found, the control will be given to the corresponding app's
_url.py_ file. Then the corresponding function in the _views.py_ file will be called which will then access the data through the defined models and calls the template to show the output to the User Interface


## *Commands to run the server and do migrations*

### Perform Migrations
```
python manage.py makemigrations
python manage.py migrate
```

### Run server
```
python manage.py runserver
```




## *Sample Screens*
### Welcome Screen
![image](https://user-images.githubusercontent.com/17834899/205507872-02c1d081-c529-4ab8-bae6-71cb0f505461.png)




### Brochure Page
![image](https://user-images.githubusercontent.com/17834899/205507893-7698bd70-41fa-4230-af76-7b28283630be.png)




### Signup Page
![image](https://user-images.githubusercontent.com/17834899/205507911-558dd1ab-f2de-432e-a30f-9cf642cc5267.png)




### Login Page
![image](https://user-images.githubusercontent.com/17834899/205507927-6310ef32-23c0-4d0b-b7aa-0c030ad1cca2.png)




### View Appointments Page (Customer View)
![image](https://user-images.githubusercontent.com/17834899/205507939-73fbb7e8-541c-4177-bd20-674622809fd7.png)




### View Appointment Details
![image](https://user-images.githubusercontent.com/17834899/205507943-38081d46-b0bc-4b97-a6be-ad8320f615a7.png)




### Cancellation Page
![image](https://user-images.githubusercontent.com/17834899/205507952-10503f5c-5f4f-4127-8e89-10e3be3792da.png)




### View Cancelled Appointments
![image](https://user-images.githubusercontent.com/17834899/205507956-fd6ff5b8-d4fb-40cb-bf14-9a1a5d1bdbf5.png)




### Book an Appointment (Date time picker)
![image](https://user-images.githubusercontent.com/17834899/205507964-05c49d7e-15fe-4f7b-af3e-88422eb5b2c6.png)




### Book an Appointment (Choose the service)
![image](https://user-images.githubusercontent.com/17834899/205507979-9a1f59bb-d57a-464d-8748-8b516d93972c.png)




### View Appointments Page (Practitioner View)
![image](https://user-images.githubusercontent.com/17834899/205508011-c99456c8-0da7-4b64-bf17-af60a8de577e.png)




### View Appointments Page (Admin View)
![image](https://user-images.githubusercontent.com/17834899/205508026-0a96bf14-e97d-4ede-aa7b-4210bf43f760.png)


### Customer Emails
![Screenshot 2022-12-04 154538](https://user-images.githubusercontent.com/17834899/205515002-696b474f-7d8f-443d-ac66-9a1e9618e786.png)

![Screenshot 2022-12-04 154339](https://user-images.githubusercontent.com/17834899/205515013-eb23bf56-cc67-4296-b51e-d80aae4d4a39.png)


### Customer SMS
![Screenshot_2022-12-04-15-51-22-53_0ce57feeccaa51fb7deed04b4dbda235](https://user-images.githubusercontent.com/17834899/205515049-59a94578-d4f8-497a-8515-4e3d3a7b0ec6.jpg)

![Screenshot_2022-12-04-15-52-21-21_0ce57feeccaa51fb7deed04b4dbda235](https://user-images.githubusercontent.com/17834899/205515055-5318dde2-6c0f-4d1f-8a8b-0aa3c9297f5f.jpg)



