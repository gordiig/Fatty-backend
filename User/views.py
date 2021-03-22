from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView, Response, Request
from rest_framework.generics import RetrieveAPIView
from User.serializers import UserSerializer, SignUpSerializer, ChangePasswordSerializer

User = get_user_model()


class ProfileView(RetrieveAPIView):
    """
    Вьюха, возвращающая профиль
    """
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class SignUpView(APIView):
    """
    Вьюха регистрации
    """
    permission_classes = ()

    def post(self, request: Request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'token': user.auth_token.key}, status=status.HTTP_201_CREATED)


class ChangePasswordView(APIView):
    """
    Вьюха изменения пароля
    """
    def patch(self, request: Request):
        serializer = ChangePasswordSerializer(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_202_ACCEPTED)
