from rest_framework.exceptions import APIException


class InvalidTokenError(APIException):
    status_code = 400
    default_detail = "유효하지 않거나 만료된 토큰입니다."
    default_code = "invalid_token"


class UserNotFoundError(APIException):
    status_code = 404
    default_detail = "해당 유저를 찾을 수 없습니다."
    default_code = "user_not_found"
