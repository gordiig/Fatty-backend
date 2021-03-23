from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView, Response, Request
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView
from Trainings.models import Exercise, ExerciseSet, Training
from Trainings.serializers import ExerciseSerializer, ExerciseSetSerializer, TrainingSerializer, TrainingListSerializer

User = get_user_model()


class MuscleTypesView(APIView):
    """
    Вьюха с типами мышц
    """
    pagination_class = None

    def get(self, request: Request):
        types = [x[0] for x in Exercise.MUSCLE_CHOICES]
        return Response({'muscleTypes': types}, status=status.HTTP_200_OK)


class ExercisesView(ListCreateAPIView):
    """
    Вьюха с упражнениями
    """
    pagination_class = None
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        return Exercise.objects.all()


class ExerciseSetView(RetrieveUpdateDestroyAPIView):
    """
    Вьюха с инфой по подходу
    """
    serializer_class = ExerciseSetSerializer

    def get_queryset(self):
        return ExerciseSet.objects.select_related('exercise')


class TrainingsListView(ListCreateAPIView):
    """
    Вьюха списка тренировок
    """
    serializer_class = TrainingListSerializer

    def get_queryset(self):
        return Training.objects\
            .filter(user=self.request.user)\
            .select_related('user')


class TrainingView(RetrieveDestroyAPIView):
    """
    Вьюха тренировки
    """
    serializer_class = TrainingSerializer

    def get_queryset(self):
        return Training.objects\
            .filter(user=self.request.user)\
            .prefetch_related('exerciseset_set', 'exerciseset_set__exercise')\
            .select_related('user')
