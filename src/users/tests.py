from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from users.models import Token

User = get_user_model()


class AuthTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # API 엔드포인트 설정
        self.sign_up_url = reverse('sign_up')
        self.sign_in_url = reverse('sign_in')
        self.sign_out_url = reverse('sign_out')
        self.refresh_token_url = reverse('refresh_token')
        self.verify_email_url = reverse('verify_email', kwargs={'token': 'dummy_token'})  # 이메일 인증 토큰

        # 테스트 유저 정보
        self.email = 'testuser@example.com'
        self.password = 'securepassword123'
        self.name = 'Test User'
        self.phone_number = '010-1234-5678'

    def test_user_signup(self):
        """
        회원가입 테스트
        """
        data = {
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'phone_number': self.phone_number
        }
        response = self.client.post(self.sign_up_url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['email'], self.email)
        self.assertEqual(response.data['name'], self.name)

    def test_email_verification(self):
        """
        이메일 인증 테스트
        """
        # 회원가입 후, 이메일 인증을 위한 토큰 발급
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            name=self.name,
            phone_number=self.phone_number,
            is_active=False
        )
        token = Token.generate_token(user)
        email_verification_token = token.refresh

        # 이메일 인증 호출
        verification_url = reverse('verify_email', kwargs={'token': email_verification_token})
        response = self.client.get(verification_url)
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_user_login(self):
        """
        로그인 테스트
        """
        # 사용자 생성
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            name=self.name,
            phone_number=self.phone_number,
            is_active=True
        )

        data = {'email': self.email, 'password': self.password}
        response = self.client.post(self.sign_in_url, data)
        self.assertEqual(response.status_code, 200)

        # Access와 Refresh 쿠키가 응답에 포함되어 있는지 확인
        self.assertIn('access', response.cookies)
        self.assertIn('refresh', response.cookies)

    def test_user_logout(self):
        """
        로그아웃 테스트
        """
        # 로그인 후 쿠키에 토큰 저장
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            name=self.name,
            phone_number=self.phone_number,
            is_active=True
        )

        login_data = {'email': self.email, 'password': self.password}
        login_response = self.client.post(self.sign_in_url, login_data)
        self.assertEqual(login_response.status_code, 200)
        refresh_token = login_response.cookies['refresh'].value

        # 로그아웃 호출
        logout_response = self.client.post(self.sign_out_url)
        self.assertEqual(logout_response.status_code, 200)

        # 쿠키에서 토큰 삭제 확인
        self.assertNotIn('access', self.client.cookies)
        self.assertNotIn('refresh', self.client.cookies)

    def test_token_refresh(self):
        """
        토큰 재발급 테스트
        """
        # 로그인 후 쿠키에 access/refresh 토큰 저장
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            name=self.name,
            phone_number=self.phone_number,
            is_active=True
        )

        login_data = {'email': self.email, 'password': self.password}
        login_response = self.client.post(self.sign_in_url, login_data)
        self.assertEqual(login_response.status_code, 200)

        refresh_token = login_response.cookies['refresh'].value

        # refresh token을 사용해 access token 재발급
        refresh_response = self.client.post(self.refresh_token_url)
        self.assertEqual(refresh_response.status_code, 200)

        # 새로운 access 쿠키가 존재하는지 확인
        self.assertIn('access', refresh_response.cookies)
        self.assertIn('refresh', refresh_response.cookies)