from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        """
        이 코드에서 **request.resolver_match**를 사용해 권한 클래스를 확인하므로,
        모든 뷰가 DRF에서 제공하는 클래스 기반 뷰(CBV)일 때만 정상적으로 작동합니다.
        함수형 뷰나 다른 인증 로직을 사용할 때는 예외 처리가 필요할 수 있습니다.
        """

        if request.resolver_match and AllowAny in request.resolver_match.func.view_class.permission_classes:
            return None  # 인증이 필요 없는 API에서는 None을 반환

        # 쿠키에서 access_token 가져오기
        access_token = request.COOKIES.get('access')

        if not access_token:
            return None  # 토큰이 없으면 None 반환

        # 토큰 검증
        try:
            validated_token = self.get_validated_token(access_token)
        except AuthenticationFailed:
            return None

        # 유저 객체와 검증된 토큰 반환
        return self.get_user(validated_token), validated_token
