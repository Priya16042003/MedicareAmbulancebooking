from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
import razorpay
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib import messages
from .models import AmbulanceBooking,Ambulance
from django.shortcuts import render, redirect
from geopy.geocoders import Nominatim  # Import the geocoding library
from geopy.distance import geodesic


from .models import UserProfile,AmbulanceBooking


def process_payment(request):
    if request.method == 'POST':
        amount_str = request.POST.get['amount']
        amount=int(amount_str)
        
        print(amount)

        # Initialize the Razorpay client
        client = razorpay.Client(auth=("rzp_test_27ICZnfVBzKJlI", "QIhAaluLjojyMQwitkXmiwfi"))

        # Create an order
        payment = client.order.create({'amount':amount*100000, 'currency': 'INR',
                                       'payment_capture': '1'})
          
        return render(request, 'success.html',{'payment': payment,'amount': amount})
      
    return render(request, 'bookingdetails.html')
   
        # Handle GET requests by rendering
    
def members(request):
     template = loader.get_template('Home.html')
     return HttpResponse(template.render())
def details(request,  id):
    ambulance_booking = AmbulanceBooking.objects.get(id=id)
    # booking = Booking.objects.get(id=booking_id)

    return render(request, 'bookingdetails.html', {
        'AmbulanceBooking': ambulance_booking,
    #     'booking': booking
    })

# def login(request):
#      template = loader.get_template('login.html')
#      return HttpResponse(template.render())
def aboutus(request):
     template = loader.get_template('abtusnew.html')
     return HttpResponse(template.render())
def services(request):
     template = loader.get_template('service.html')
     return HttpResponse(template.render())


def book(request):
  if request.method == 'POST':
        your_name = request.POST.get('name')
        phone_number = request.POST.get('phone')
        pickup_location = request.POST.get('location')
        date = request.POST.get('date')
        time = request.POST.get('time')
        ambulance_type = request.POST.get('ambulanceType')
        additional_comments = request.POST.get('comments')
        geolocator = Nominatim(user_agent="myapp")  # Replace "myapp" with your user agent
        try:
            location = geolocator.geocode(pickup_location)
            user_latitude = location.latitude if location else None
            user_longitude = location.longitude if location else None
        except:
            user_latitude = None
            user_longitude = None

        # Find the nearest ambulance location (example logic)
        user_location = (user_latitude, user_longitude)  # Coordinates of the user's pickup location

        # Query the database to get a list of ambulance locations
        ambulance_locations = Ambulance.objects.all()

        # Find the nearest ambulance location using the Haversine formula
        nearest_ambulance = min(ambulance_locations, key=lambda ambulance: geodesic(user_location, (ambulance.current_location_latitude, ambulance.current_location_longitude)).miles)

        # Calculate the distance from the user's location to the nearest ambulance
        distance = geodesic(user_location, (nearest_ambulance.current_location_latitude, nearest_ambulance.current_location_longitude)).miles
        print(distance)

        # Calculate the total amount based on distance and ambulance type (example logic)
        base_fee = 100  # Base fee
        distance_fee = distance * 2  # Example: $2 per mile
        ambulance_type_fee = {
            'Basic Ambulance': 50,
            'Advanced Ambulance': 75,
            'Intensive Care Unit (ICU) Ambulance': 100,
            'Specialized Ambulance': 90,
        }.get(ambulance_type, 0)  # Default to 0 if type not found

        total_amount = base_fee + distance_fee + ambulance_type_fee

        # Create the AmbulanceBooking instance
        booking = AmbulanceBooking(
            your_name=your_name,
            phone_number=phone_number,
            pickup_location=pickup_location,
            date=date,
            time=time,
            ambulance_type=ambulance_type,
            additional_comments=additional_comments,
            total_amount=total_amount,
        )
        booking.save()

        # You can perform additional actions here, such as sending confirmation emails.

        messages.success(request, 'Booking successfully saved.')

        # Redirect to a thank you page or any other appropriate page
        return HttpResponseRedirect(reverse('details', args=[booking.id]))

    # Handle GET requests or render the booking form
  return render(request, 'book.html') # Change 'booking_form.html' to your actual template name

def plan(request):
     template = loader.get_template('plan.html')
     return HttpResponse(template.render())

@csrf_protect
def login(request):
    if request.method == 'POST':
          
          user = request.POST['user']
          email = request.POST['email']
          password = request.POST['password']


            # You may want to perform additional actions, such as sending a welcome email.

            # Redirect to the user's profile page or home page
          new_user=UserProfile(user=user,email=email,password=password)
          new_user.save() # You need to define a 'home' URL pattern.
          messages.success(request, 'Successfully registered. Please sign in.')
          return HttpResponseRedirect(reverse('members'))


  
    return render(request, 'login.html', {})
