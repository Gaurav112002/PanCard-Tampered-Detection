from django.db import models
from datetime import datetime

# Create your models here.
class Insert(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name
    