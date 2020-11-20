from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from pandemic_app.forms import LoginForm, SignUpForm
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