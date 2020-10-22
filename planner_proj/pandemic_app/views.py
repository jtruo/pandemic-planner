from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from pandemic_app.forms import LoginForm, SignUpForm
from pandemic_app.models import UserAccount


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

