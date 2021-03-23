from django.contrib.auth import get_user_model
from django.db.models import Max, IntegerField, Value
from django.db.models.functions import Coalesce
from rest_framework import serializers, validators
from fatty_shared.serializers import IdOnWriteSerializerOnReadField
from User.serializers import UserSerializer
from Trainings.models import Exercise, ExerciseSet, Training

User = get_user_model()


class ExerciseSerializer(serializers.ModelSerializer):
    """
    Сериализатор упражнения
    """
    muscle_type = serializers.ChoiceField(choices=Exercise.MUSCLE_CHOICES)
    name = serializers.CharField(
        validators=validators.UniqueValidator(
            queryset=Exercise.objects.all(),
            message='Такое упражнение уже есть в базе, алло',
            lookup='iexact'
        )
    )

    class Meta:
        model = Exercise
        fields = [
            'name',
            'muscle_type'
        ]


class ExerciseSetSerializer(serializers.ModelSerializer):
    """
    Сериализатор подхода
    """
    index_number = serializers.IntegerField(min_value=0, required=False)
    exercise = IdOnWriteSerializerOnReadField(
        child_serializer=ExerciseSerializer(),
        queryset=Exercise.objects.all(),
        message='Переданного упражнения нет в базе'
    )
    reps = serializers.IntegerField(min_value=0)
    training = serializers.PrimaryKeyRelatedField(queryset=Training.objects.all())

    class Meta:
        model = ExerciseSet
        fields = [
            'index_number',
            'exercise',
            'reps',
            'training',
        ]

    def create(self, validated_data):
        if 'index_number' not in validated_data:
            index_number = ExerciseSet.objects \
                .filter(training=validated_data['training']) \
                .aggregate(max_idx_num=Coalesce(Max('index_number', output_field=IntegerField()), Value(0)))
            validated_data['index_number'] = index_number['max_idx_num'] + 1
        return super().create(validated_data)

    def update(self, instance: ExerciseSet, validated_data):
        if 'training' in validated_data:
            del validated_data['training']
        return super().update(instance, validated_data)


class TrainingListSerializer(serializers.ModelSerializer):
    """
    Списковый сериализатор тренировок
    """
    user = IdOnWriteSerializerOnReadField(
        child_serializer=UserSerializer(),
        queryset=User.objects.all(),
        message='Данного пользователя не существует',
    )

    class Meta:
        model = Training
        fields = [
            'date',
            'user',
        ]


class TrainingSerializer(TrainingListSerializer):
    """
    Сериализатор тренировки
    """
    sets = serializers.SerializerMethodField()

    class Meta(TrainingListSerializer.Meta):
        fields = TrainingListSerializer.Meta.fields + [
            'sets'
        ]

    def get_sets(self, instance: Training):
        sets = instance.exerciseset_set \
            .select_related('exercise') \
            .order_by('index_number')
        return ExerciseSetSerializer(instance=sets, many=True).data
