from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    # URL for the OpenWeatherMap API with placeholders for city name and API key
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=340fb9ddc6c457b9fe7e06ecb544a77a'

    # Initialize error message, general message, and message class
    err_msg = ''
    message = ''
    message_class = ''

    
    if request.method == "POST":
        form = CityForm(request.POST)  # Initialize the form with submitted data

        if form.is_valid():  # Validate the form data
            new_city = form.cleaned_data['name']  # Get the cleaned city name from the form
            existing_city_count = City.objects.filter(name=new_city).count()  # Check if the city already exists in the database

            if existing_city_count == 0:  # If the city does not exist in the database
                r = requests.get(url.format(new_city)).json()  # Make a request to the API with the new city name
                if r['cod'] == 200:  # Check if the API response is successful
                    form.save()  # Save the new city to the database
                else:
                    err_msg = 'City does not exist on this planet!!'  # Set error message if city is not found
            else:
                err_msg = 'City already added to database!!'  # Set error message if city already exists

        if err_msg:  # If there is an error message
            message = err_msg  # Set the general message to the error message
            message_class = "is-danger"  # Set the message class to indicate an error
        else:
            message = "City added successfully!!"  # Set success message
            message_class = "is-success"  # Set the message class to indicate success

        print(err_msg)  # Print the error message (for debugging purposes)

    form = CityForm()  # Initialize an empty form

    cities = City.objects.all()  # Retrieve all cities from the database

    weather_data = []  # Initialize an empty list to hold weather data
    for city in cities:
        r = requests.get(url.format(city)).json()  # Make a request to the API for each city

        # Extract relevant weather data from the API response
        city_weather = {
            "city": city.name,
            "temperature": r['main']['temp'],
            "description": r['weather'][0]['description'],
            "icon": r['weather'][0]['icon'],
            "rain": r['weather'][0]['main'],
        }
        weather_data.append(city_weather)  # Add the weather data to the list

    # Create a context dictionary to pass data to the template
    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class,
    }
    return render(request, 'index.html', context)  # Render the template with the context data

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()  # Delete the city from the database
    return redirect('weather_home')  # Redirect to the home page
