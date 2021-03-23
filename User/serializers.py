from django.db import IntegrityError
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя
    """
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
        ]


class SignUpSerializer(serializers.Serializer):
    """
    Сериализатор регистрации
    """
    username = serializers.CharField(max_length=128, allow_null=False, allow_blank=False)
    email = serializers.EmailField(allow_null=False, allow_blank=False, required=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password_confirm = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    def create(self, validated_data) -> User:
        if validated_data['password'] != validated_data['password_confirm']:
            raise serializers.ValidationError({'error': 'Пароли не совпадают'})
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                email=validated_data.get('email', ''),
            )
        except IntegrityError:
            raise serializers.ValidationError({'error': 'Юзер с переданными данными уже существует'})
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """
    Сериализатор смены пароля
    """
    old_password = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password_confirm = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    def update(self, instance: User, validated_data):
        if not instance.check_password(validated_data['old_password']):
            raise serializers.ValidationError({'error': 'Старый пароль введен неправильно'})
        if validated_data['password'] != validated_data['password_confirm']:
            raise serializers.ValidationError({'error': 'Пароли не совпадают'})
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
