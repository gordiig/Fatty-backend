from rest_framework.generics import RetrieveUpdateAPIView
from Goals.models import DailyEatingGoals
from Goals.serializers import DailyEatingGoalsSerializer


class DailyEatingGoalsView(RetrieveUpdateAPIView):
    """
    Вьюха для получения дневных целей кбжу
    """
    serializer_class = DailyEatingGoalsSerializer

    def get_object(self):
        return DailyEatingGoals.objects.get(user=self.request.user)
