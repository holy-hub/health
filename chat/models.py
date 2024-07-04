from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    name       = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class GroupMessage(models.Model): # Dans un groupe de personnes
    room       = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}, createur du groupe de message {self.room.name}."

class PrivateMessage(models.Model):
    sender   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content  = models.TextField()
    sent_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} envoie du message a {self.receiver.username}."
