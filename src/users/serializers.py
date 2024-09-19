from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User
from utils.validators import validate_create_user


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ["email", "password", "login_type",
                  "name", "nickname", "phone_number",
                  "is_active"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValueError("이미 사용 중인 이메일입니다.")

        return value

    def validate(self, data):
        validate_create_user(**data)
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SignInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # authenticate 함수로 유저 인증
        user = authenticate(username=email, password=password)

        # 인증 실패 시 (None 반환)
        if not user:
            raise ValidationError("비밀번호 혹은 이메일이 일치하지 않습니다.")

        # 인증 성공, 하지만 계정이 비활성화된 경우
        if not user.is_active:
            raise ValidationError("해당 계정은 비활성화 상태입니다. 회원가입 시 받은 이메일로 인증을 수행해주시기 바랍니다.")

        # 유저 인증 및 활성화 상태 확인 성공
        data["user"] = user
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'nickname', 'phone_number']
        read_only_fields = ['id', 'email']