from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from pandemic_app.forms import LoginForm, SignUpForm, CreateAssForm, CreateExamForm, CreateLectureForm, CreateClassForm
from pandemic_app.models import UserAccount, Class, Lecture, Assignment, Exam

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
#takes a class name and user_id and queries it to get the users class_id
def name_to_id(name, userid):
    c = Class.objects.all().filter(class_name=name, user_id = userid)
    if len(c) > 0:
        c = c[0]
    else:
        return -1
    return c.id


def info(request):
    template = loader.get_template('pandemic_app/info.html')
    userid = request.session['userid']
    username = ""
    if userid >= 0:
        #userid is okay
        username = request.session['username']
    else:
        userid = -1
    context = { #store all of the variables we use here
        'userid' : userid,
    }
    return HttpResponse(template.render(context, request))

# Create your views here.
def index(request):
    
    try:
        username = request.session['username']
    except KeyError:
        username = ""
    if len(username) > 0:
        print("username:", username)

    template = loader.get_template('pandemic_app/index.html')
    context = {
        'username' : username,
    }
    return HttpResponse(template.render(context, request))


def logout(request):
    try:
        del request.session['userid']
        del request.session['username']
        del request.session['email']
        del request.session['credit_hours']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('index'))
    
def login(request):
    
    try:
        username = request.session['username']
    except KeyError:
        username = ""
    if len(username) > 0:
        print("username:", username)

    if request.method == "POST":        
        MyLoginForm = LoginForm(request.POST)
        #if MyLoginForm.is_valid():
        username = MyLoginForm.data['username']
        pswrd = MyLoginForm.data['password']
        #user if one matched
        print("getting user for: ", username, pswrd, "\n")
        user = UserAccount.objects.all().filter(username=username)
        if len(user) >= 1:
            user = user[0]
        print("userid", user.id)
        request.session['userid'] = user.id #will be set based on user id paired with username in db
        request.session['username'] = user.username
        request.session['email'] = user.email
        request.session['credit_hours'] = user.credit_hours
        return HttpResponseRedirect(reverse('index'))
    else:
        MyLoginForm = LoginForm()

    testingvar = "Testing string"
    template = loader.get_template('pandemic_app/login.html')
    context = {
        'username' : username,
        'testingvar' : testingvar,
    }
    return HttpResponse(template.render(context, request))

def create(request):
    template = loader.get_template("pandemic_app/content_manage.html")
    return HttpResponse(template.render({}, request))

#need views for lecture, exam, and class now
#all of these might need a username field
def create_lec(request):
    class_name = "empty"
    date = "empty"
    summary = "empty"
    userid = request.session['userid']
    if userid >= 0:
        print('valid')
    else:
        return HttpResponse("not logged in, cannot create lec")
    if request.method == "POST":
        MyLec = CreateLectureForm(request.POST)
        date = MyLec.data['duedate']
        class_name = MyLec.data['classname']
        class_id = name_to_id(class_name, userid)#we will query db to get class_id via class name
        if class_id == -1:
            return HttpResponse("unable to retrive class id for class:", class_name)
        summary = MyLec.data['summary']
        c = Lecture(class_id=class_id, day=date, user_id=userid, summary=summary)
        c.save() #dont save it because we do not properly generate class id
    else:
        MyLec = CreateLectureForm()
    
    template = loader.get_template('pandemic_app/content_manage.html')
    context = {
        'due_date' : date,
        'class_name' : class_name,
        'summary' : summary
    }
    return HttpResponse(template.render(context, request))

#working!!
def create_class(request):
    class_name = "empty"
    userid = request.session['userid']
    if userid >= 0:
        print('user is logged in')
    else:
        return HttpResponse("Not Logged In, cannot create class")
    if request.method == "POST":
        MyClass = CreateClassForm(request.POST)
        name = MyClass.data['classname']
        cred = MyClass.data['credits']
        c = Class(class_name=name, credits=cred, user_id=userid)
        c.save()
    else:
        MyClass = CreateClassForm()
    template = loader.get_template('pandemic_app/content_manage.html')
    context = {}
    return HttpResponse(template.render(context, request))

def create_exam(request):
    userid = request.session['userid']
    if userid >= 0:
        print('user is logged in')
    else:
        return HttpResponse("User not logged in")
    if request.method == "POST":
        MyExam = CreateExamForm(request.POST)
        name = MyExam.data['classname']
        date = MyExam.data['date']
        class_id = name_to_id(name, userid)
        e = Exam(class_id=class_id, user_id=userid, exam_date=date)
        e.save()
    else:
        MyExam = CreateExamForm()
    template = loader.get_template('pandemic_app/content_manage.html')
    context = {}
    return HttpResponse(template.render(context, request))

def create_assign(request):
    assign_name = "empty"
    class_name = "empty"
    due_date = "empty"
    date_assigned = "empty"
    user_id = request.session['userid']
    if request.method == "POST":
        MyAssign = CreateAssForm(request.POST)
        assign_name = MyAssign.data['assname']
        class_name = MyAssign.data['classname']
        due_date = MyAssign.data['duedate']
        date_assigned = MyAssign.data['dateass']
        class_id = name_to_id(class_name, user_id)
        a = Assignment(due_date=due_date, date_assigned=date_assigned, user_id=user_id, class_id=class_id, ass_name=assign_name)
        a.save()
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
            #we should verify the username is not already in the UserAccounts table
            user = UserAccount.objects.all().filter(username=username)
            if len(user) == 0:
                user_inst = UserAccount(username=username, email=email, password=password, credit_hours=credit_hours)
                print("attributes:", username, password, email, credit_hours)
                #UserAccount.objects.raw("Insert Into pandemic_app_useraccount values (username, password, email, credit_hours);")
                user_inst.save()
            else:
                return HttpResponse("username already in use!")
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