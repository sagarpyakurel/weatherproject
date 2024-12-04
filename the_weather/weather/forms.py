from django.forms import ModelForm, TextInput  # Import necessary form classes
from .models import City  # Import the City model

class CityForm(ModelForm):
    class Meta:
        model = City  # Specify the model to use
        fields = ['name']  # Include only the 'name' field
        widgets = {'name': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'})}  # Customize the 'name' field