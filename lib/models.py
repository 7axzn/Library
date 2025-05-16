from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Book_Details(models.Model):
    Name = models.CharField(max_length=120)
    Author = models.CharField(max_length=120)
    Category = models.CharField(max_length=120)
    Description = models.TextField()
    Date_Added = models.DateField()
    Availability = models.CharField( max_length=50)



class CustomUser(AbstractUser):
    USER_TYPES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    borrowed_books = models.ManyToManyField('Book_Details', blank=True) 
