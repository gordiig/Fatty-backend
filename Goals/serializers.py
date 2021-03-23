from rest_framework import serializers
from Goals.models import DailyEatingGoals


class DailyEatingGoalsSerializer(serializers.ModelSerializer):
    """
    Сериализатор дневного кбжу
    """
    class Meta:
        model = DailyEatingGoals
        fields = [
            'kcal',
            'carbs',
            'proteins',
            'fats',
        ]
