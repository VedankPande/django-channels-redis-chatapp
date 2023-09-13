from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    online = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"User: {self.username}"
    
    def is_online(self):
        return self.online
    
    def set_user_offline(self):
        self.online = False
        self.save()
    
    def set_user_online(self):
        self.online = True
        self.save()

