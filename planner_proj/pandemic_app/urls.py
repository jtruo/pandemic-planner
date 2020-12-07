from django.urls import path, include, re_path

from . import views

# Used for a namespace to reverse a url
#app_name = 'pandemic_app'

urlpatterns = [

path('', views.index, name="index"),
path('reports', views.info, name = "info"),
path('login', views.login, name = "login"),
path('logout', views.logout, name = "logout"),
path('create', views.create, name="create"),
path('create_lec', views.create_lec, name="create_lec"),
path('create_assign', views.create_assign, name = "create_assign"),
path('signup', views.create_account, name = "signup"),
path('calendar', views.CalendarView.as_view(), name='calendar'),
path('create_class', views.create_class, name="create_class"),
path('create_exam', views.create_exam, name="create_exam"),

]