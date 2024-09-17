from django.conf import settings
from django.urls import reverse
from django.core.signing import SignatureExpired, BadSignature, TimestampSigner
from django.core.mail import send_mail
from users.exceptions import InvalidTokenError

signer = TimestampSigner()


def send_verification_email(email, request):
    token = generate_email_verification_token(email)
    verification_url = (f"{settings.SERVER_PROTOCOL}://{settings.SERVER_DOMAIN}"
                        f"{reverse('verify_email', kwargs={'token': token})}")

    send_mail(
        'Email 인증',
        f'email을 인증하기 위해 해당 url을 클릭해주세요!: {verification_url}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )


def generate_email_verification_token(email: str) -> str:
    """
    사용자의 이메일을 토큰으로 변환.
    :param email: 사용자의 이메일
    :return: 서명된 이메일 토큰
    """
    return signer.sign(email)


def verify_email_verification_token(token: str, max_age: int = 3600) -> str | None:
    """
    토큰을 검증하고 이메일을 반환.
    :param token: 이메일 서명된 토큰
    :param max_age: 토큰의 유효 시간(초 단위)
    :return: 이메일이 유효하면 이메일을 반환, 그렇지 않으면 None
    """
    try:
        email = signer.unsign(token, max_age=max_age)
        return email
    except (SignatureExpired, BadSignature):
        raise InvalidTokenError
