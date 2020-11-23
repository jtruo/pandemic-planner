from django import forms

from django.forms import ModelForm, DateInput
from .models import Event

class LoginForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput())

class SignUpForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput())
    email = forms.EmailField()
    credit_hours = forms.IntegerField()

    def clean_user(self):
        data = self.cleaned_data['user']
        return data
    
    def clean_password(self):
        data = self.cleaned_data['password']
        return data
    
    def clean_email(self):
        data = self.cleaned_data['email']
        return data

    def clean_credit_hours(self):
        data = self.cleaned_data['credit_hours']
        return data


class EventForm(ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
        'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)