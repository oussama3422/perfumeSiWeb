from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    product_favorites=models.ManyToManyField(Product)
    phoneNum=models.CharField(max_length=10)
    # fullname=models.CharField(max_length=20)


    def __str__(self) -> str:
        return self.user.username

