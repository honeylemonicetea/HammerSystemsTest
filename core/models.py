from django.db import models



# Create your models here.
class UserProfile(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    own_invite_code = models.CharField(max_length=6, default="")
    friends_invite_code = models.CharField(max_length=6, default="")
    
    def __str__(self) -> str:
        return self.phone_number
    
    