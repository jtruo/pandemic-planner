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
    students = ArrayField(models.TextField())

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'


#none of these are migrated yet
class Assignment(models.Model):
    #assignment_id = models.IntegerField() <- automatically added, can be modified more through the db
    due_date = models.DateField()
    date_assigned = models.DateField()
    class_id = models.IntegerField()

class Lecture(models.Model):
    class_id = models.IntegerField()
    day = models.TextField()
    summary = models.TextField()

class Exam(models.Model):
    class_id = models.IntegerField()
    exam_date = models.DateField() #maybe date and time field
    