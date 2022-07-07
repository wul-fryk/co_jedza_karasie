from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Room

class User_form(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class Room_form(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'room_topic']