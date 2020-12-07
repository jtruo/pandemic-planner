from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.urls import reverse

# Create your models here.
class UserAccount(models.Model):
    username = models.TextField()
    email = models.TextField()
    password = models.TextField()
    credit_hours = models.IntegerField()

class Class(models.Model):
    class_name = models.TextField()
    credits = models.IntegerField()
    user_id = models.IntegerField()

# Currently unused
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

class Assignment(models.Model):
    #assignment_id = models.IntegerField() <- automatically added, can be modified more through the db
    due_date = models.DateField()
    date_assigned = models.DateField()
    class_id = models.IntegerField()
    ass_name = models.TextField()
    user_id = models.IntegerField()

class Lecture(models.Model):
    class_id = models.IntegerField()
    day = models.DateField()
    summary = models.TextField()
    user_id = models.IntegerField()

class Exam(models.Model):
    class_id = models.IntegerField()
    exam_date = models.DateField() 
    user_id = models.IntegerField()    