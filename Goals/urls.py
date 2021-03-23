from django.conf.urls import url
from Goals import views


app_name = 'Goals'

urlpatterns = [
    url(r'^daily-eating-goals/$', views.DailyEatingGoalsView.as_view()),
]
