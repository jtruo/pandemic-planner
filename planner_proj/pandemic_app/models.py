from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class UserAccount(models.Model):
    username = models.TextField()
    email = models.TextField()
    password = models.TextField()
    credit_hours = models.IntegerField()

class Class(models.Model):
    class_name = models.TextField()
    credits = models.IntegerField()
    students = ArrayField(models.TextField())
