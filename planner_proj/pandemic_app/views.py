from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from pandemic_app.forms import LoginForm, SignUpForm, CreateAssForm, CreateExamForm, CreateLectureForm, CreateClassForm
from pandemic_app.models import UserAccount

from datetime import datetime, timedelta, date
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe

from .models import *
from .utils import Calendar
from calendar import HTMLCalendar
import calendar
from .forms import EventForm


# Create your views here.
def index(request):
    username = "not logged in"
    if request.method == "POST":
        MyLoginForm = LoginForm(request.POST)
        if MyLoginForm.is_valid():
            username = MyLoginForm.cleaned_data['username']
    else:
        MyLoginForm = LoginForm()

    testingvar = "Testing string"
    template = loader.get_template('pandemic_app/index.html')
    context = {
        'username' : username,
        'testingvar' : testingvar,
    }
    return HttpResponse(template.render(context, request))

#need views for lecture, exam, and class now
#all of these might need a username field
def create_lec(request):
    class_name = "empty"
    date = "empty"
    summary = "empty"
    if request.method == "POST":
        MyLec = CreateLectureForm(request.POST)
        if MyLec.is_valid():
            date = MyLec.cleaned_date['due_date']
            class_name = MyLec.cleaned_data['class_name']
            summary = MyLec.cleaned_data['summary']
    else:
        MyLec = CreateLectureForm()
    
    template = loader.get_template('pandemic_app/content_manage.html')
    context = {
        'due_date' : date,
        'class_name' : class_name,
        'summary' : summary
    }

def create_assign(request):
    assign_name = "empty"
    class_name = "empty"
    due_date = "empty"
    date_assigned = "empty"
    if request.method == "POST":
        MyAssign = CreateAssForm(request.POST)
        if MyAssign.is_valid():
            assign_name = MyAssign.cleaned_data['assign_name']
            class_name = MyAssign.cleaned_data['class_name']
            due_date = MyAssign.cleaned_data['due_date']
            date_assigned = MyAssign.cleaned_data['date_assigned']
    else:
        MyAssign = CreateAssForm()
    
    template = loader.get_template('pandemic_app/content_manage.html')
    context = {
        'assign_name': assign_name,
        'class_name' : class_name,
        'due_date': due_date,
        'date_assigned': date_assigned,
    }
    return HttpResponse(template.render(context, request))


def add_entries(request):
    username = "not logged in"
    template = loader.get_template('pandemic_app/content_manage.html')
    context = {
        
    }
    return HttpResponse(template.render(context, request))

def create_account(request):
    username = "Not Entered"
    user_inst = None
    if request.method == "POST":
        MySignUp = SignUpForm(request.POST)
        if MySignUp.is_valid():
            username = MySignUp.cleaned_data['user']
            password = MySignUp.cleaned_data['password']
            email = MySignUp.cleaned_data['email']
            credit_hours = MySignUp.cleaned_data['credit_hours']
            user_inst = UserAccount(username=username, email=email, password=password, credit_hours=credit_hours)
            print("attributes:", username, password, email, credit_hours)
            #UserAccount.objects.raw("Insert Into pandemic_app_useraccount values (username, password, email, credit_hours);")
            user_inst.save()
    else: 
        MySignUp = SignUpForm()

    template = loader.get_template('pandemic_app/signup.html')
    context = {
        'filler' : 6,
        'user_inst' : user_inst,
    }
    return HttpResponse(template.render(context, request))


class CalendarView(generic.ListView):
    model = Event
    template_name = 'pandemic_app/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the month for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month    

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'pandemic_app/event.html', {'form': form})