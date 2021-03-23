from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class DailyEatingGoals(models.Model):
    """
    Модель ежедневных целей для питания
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='daly_eating_goals', help_text='Чья цель')
    kcal = models.PositiveIntegerField(help_text='Дневной калораж', default=0)
    carbs = models.PositiveIntegerField(help_text='Углеводы', default=0)
    proteins = models.PositiveIntegerField(help_text='Белки', default=0)
    fats = models.PositiveIntegerField(help_text='Жиры', default=0)

    def __str__(self):
        return self.user.username
