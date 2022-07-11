from django.contrib import admin
from .models import Topic, Room, Message, User_activity
# Register your models here.

admin.site.register(Topic)
admin.site.register(User_activity)
admin.site.register(Room)
admin.site.register(Message)