from django.db.models import QuerySet, ObjectDoesNotExist
from rest_framework.serializers import Field, Serializer, ValidationError


class IdOnWriteSerializerOnReadField(Field):
    """
    Поле сериализатора, на добавление принимающее айди, а на чтение отдающее сериализированную сущность
    """
    def __init__(self, child_serializer: Serializer, queryset: QuerySet, message: str = 'Такого объекта не существует',
                 **kwargs):
        super().__init__(**kwargs)
        self.child_serializer = child_serializer
        self.queryset = queryset
        self.message = message

    def to_internal_value(self, data):
        try:
            return self.queryset.get(id=data)
        except ObjectDoesNotExist:
            raise ValidationError({'error': self.message})

    def to_representation(self, value):
        return self.child_serializer.to_representation(value)
