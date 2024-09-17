from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    """
    이메일을 사용한 인증 백엔드
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # username 대신 email 필드를 사용
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):  # 비밀번호 확인
            return user
        return None
