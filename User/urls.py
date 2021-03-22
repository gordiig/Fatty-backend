from django.conf.urls import url
from User import views


app_name = 'User'

urlpatterns = [
    url(r'^profile/$', views.ProfileView.as_view()),
    url(r'^profile/change-password/$', views.ChangePasswordView.as_view()),
    url(r'^sign-up/$', views.SignUpView.as_view()),
]
