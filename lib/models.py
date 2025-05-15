from django.db import models

# Create your models here.
class Book_Details(models.Model):
    Name = models.CharField(max_length=120)
    Author = models.CharField(max_length=120)
    Category = models.CharField(max_length=120)
    Description = models.TextField()
    Date_Added = models.DateField()
    Availability = models.CharField(max_length=120)