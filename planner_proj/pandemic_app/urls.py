from django.urls import path

from . import views

urlpatterns = [path('', views.index, name="index"),
path('signup', views.create_account, name = "create_account"),
path('calendar', views.CalendarView.as_view(), name='calendar')

]