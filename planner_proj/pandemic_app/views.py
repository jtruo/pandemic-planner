from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from pandemic_app.forms import LoginForm


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
