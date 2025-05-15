from django.db import models

# Create your models here.
class Book_Details(models.Model):
    Name = models.CharField(max_length=120)
    Author = models.CharField(max_length=120)
    Category = models.CharField(max_length=120)
    Description = models.TextField()
    Date_Added = models.DateField()
    Availability = models.BooleanField(default=True)




    from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='user')
