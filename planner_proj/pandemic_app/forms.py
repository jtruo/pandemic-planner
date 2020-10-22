from django import forms

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