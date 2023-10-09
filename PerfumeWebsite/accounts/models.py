from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    phoneNum=models.CharField(max_length=10)
    # fullname=models.CharField(max_length=20)


    def __str__(self) -> str:
        return self.user.username

