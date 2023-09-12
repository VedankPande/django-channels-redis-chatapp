from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.



class Message(models.Model):
    
    sender = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='sent_messages')
    receiver = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='received_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.sender.username} sent message: '{self.message}' to {self.receiver.username}"