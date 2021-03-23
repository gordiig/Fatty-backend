from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from TestUtils.FattyTestCase import FattyTestBase

User = get_user_model()


class ProfileViewTestCase(FattyTestBase):
    """
    Тесты для profile/
    """
    def setUp(self):
        super().setUp()
        self.url = self.url_prefix + 'profile/'

    def testGet200_OK(self):
        response = self.get_response_and_check_status_code(self.url)
        self.assertEqual(self.user.username, response['username'], msg='Wrong username returned')


class SignUpViewTestCase(FattyTestBase):
    """
    Тесты для sign-up/
    """
    def setUp(self):
        super().setUp()
        self.url = self.url_prefix + 'sign-up/'
        self.data_201 = {
            'username': 'test',
            'password': 'pwd',
            'password_confirm': 'pwd',
        }
        self.data_400_exicting_username = {
            'username': self.user.username,
            'password': 'pwd',
            'password_confirm': 'pwd',
        }
        self.data_400_passwords_dont_match = {
            'username': 'test',
            'password': 'pwd',
            'password_confirm': 'dwp',
        }

    def testPost201_OK(self):
        response = self.post_response_and_check_status_code(self.url, data=self.data_201)
        try:
            token = Token.objects\
                .select_related('user')\
                .get(key=response['token'])
        except Token.DoesNotExist:
            self.assertTrue(False, msg='Token does not exist, so as new user')
        self.assertEqual(token.user.username, self.data_201['username'], msg='Wrong username')

    def testPost400_ExistingUsername(self):
        self.post_response_and_check_status_code(self.url, data=self.data_400_exicting_username, expected_status_code=400)

    def testPost400_PasswordsDontMatch(self):
        self.post_response_and_check_status_code(self.url, data=self.data_400_passwords_dont_match,
                                                 expected_status_code=400)


class ChangePasswordViewTestCase(FattyTestBase):
    """
    Тесты для profile/change-password/
    """
    def setUp(self):
        super().setUp()
        self.url = self.url_prefix + 'profile/change-password/'
        self.data_202 = {
            'old_password': self.user_password,
            'password': 'pwd',
            'password_confirm': 'pwd',
        }
        self.data_400_wrong_old = {
            'old_password': self.user_password + '1111111',
            'password': 'pwd',
            'password_confirm': 'pwd',
        }
        self.data_400_dont_match = {
            'old_password': self.user_password,
            'password': 'pwd',
            'password_confirm': 'dwp',
        }

    def testPatch202_OK(self):
        self.patch_response_and_check_status_code(self.url, data=self.data_202)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.data_202['password']), msg='Wrong new password')

    def testPatch400_WrongOldPwd(self):
        self.patch_response_and_check_status_code(self.url, data=self.data_400_wrong_old, expected_status_code=400)

    def testPatch400_PasswordsDontMatch(self):
        self.patch_response_and_check_status_code(self.url, data=self.data_400_dont_match, expected_status_code=400)

