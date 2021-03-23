from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Exercise(models.Model):
    """
    Модель упражнения
    """
    MUSCLE_CHOICES = (
        ('Спина', 'Спина'),
        ('Бицепс', 'Бицепс'),
        ('Трицепс', 'Трицепс'),
        ('Предплечье', 'Предплечье'),
        ('Грудь', 'Грудь'),
        ('Пресс', 'Пресс'),
        ('Ноги', 'Ноги'),
        ('Кардио', 'Кардио'),
    )

    name = models.CharField(null=False, blank=False, max_length=128, help_text='Название упражнения', unique=True)
    muscle_type = models.CharField(choices=MUSCLE_CHOICES, max_length=64, help_text='Тип упражнения')

    def __str__(self):
        return f'{self.muscle_type}, {self.name}'


class ExerciseSet(models.Model):
    """
    Модель подхода
    """
    index_number = models.PositiveIntegerField(help_text='Номер подхода в тренировке')
    exercise = models.ForeignKey(Exercise, related_name='gym_sets', on_delete=models.CASCADE, help_text='Упражнение')
    reps = models.PositiveIntegerField(help_text='Повторения')
    training = models.ForeignKey('Training', on_delete=models.CASCADE, help_text='Тренировка')

    def __str__(self):
        return f'{self.training.date}, {self.exercise.name} ({self.index_number} подход) by {self.training.user.username}'


class Training(models.Model):
    """
    Модель тренировки
    """
    date = models.DateTimeField(auto_now_add=True, help_text='Дата тренировки')
    user = models.ForeignKey(User, related_name='trainings', on_delete=models.CASCADE, help_text='Кто занимался')

    def __str__(self):
        return f'{self.user.username} {self.date}'
