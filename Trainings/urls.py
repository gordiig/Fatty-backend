from django.conf.urls import url
from Trainings import views


app_name = 'Trainings'

urlpatterns = [
    url(r'^muscle-types/$', views.MuscleTypesView.as_view()),
    url(r'^exercises/$', views.ExercisesView.as_view()),
    url(r'^exercise-sets/$', views.CreateExerciseSetView.as_view()),
    url(r'^exercise-sets/(?P<pk>\d+)/$', views.ExerciseSetView.as_view()),
    url(r'^trainings/$', views.TrainingsListView.as_view()),
    url(r'^trainings/(?P<pk>\d+)/$', views.TrainingView.as_view()),
]
