from rest_framework.serializers import ModelSerializer

from users.models import User


class SignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "name", "phone_number"]


class SignInSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
