from django.urls import path, include, re_path

from . import views

# Used for a namespace to reverse a url
#app_name = 'pandemic_app'

urlpatterns = [

path('', views.index, name="index"),
path('signup', views.create_account, name = "create_account"),
path('calendar', views.CalendarView.as_view(), name='calendar'),
re_path(r'^event/new/$', views.event, name='event_new'),
re_path(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),

]