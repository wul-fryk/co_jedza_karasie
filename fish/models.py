from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    topic_name = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.topic_name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room_name = models.CharField(max_length=250)
    room_topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    room_desription = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # participants = 

    def __str__(self):
        return self.room_name

    class Meta:
        ordering = ['-created', '-updated']



class Message(models.Model):
    room_messages = models.ForeignKey(Room, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body

    class Meta:
        ordering = ['-created']

