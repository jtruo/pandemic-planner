from django.db import models

# Create your models here.
class Test(models.Model):

    name = models.TextField()
    
    attr = models.TextField()

class UserAccount(models.Model):
    username = models.TextField()
    email = models.TextField()
    password = models.TextField()
    credit_hours = models.IntegerField()

