from django.db import models

# Create your models here.
class UserAccount(models.Model):
    username = models.TextField()
    email = models.TextField()
    password = models.TextField()
    credit_hours = models.IntegerField()

