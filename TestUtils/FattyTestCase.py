import json
from typing import Union
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

User = get_user_model()


class FattyTestBase(TestCase):
    url_prefix = f'/api/'

    def setUp(self):
        self.user_password = 'Test_password'
        self.user = User.objects.create_user(username='Test_user', password='Test_password', email='a@a.com')
        self.token = Token.objects.get(user=self.user)

    def get_response_and_check_status_code(self, url: str, expected_status_code: int = 200,
                                           authorized: bool = True) -> Union[dict, list]:
        client = APIClient()
        if authorized:
            client.force_authenticate(user=self.user)
        response = client.get(url)
        self.assertEqual(response.status_code, expected_status_code,
                         msg=f'Response status code for {url} is {response.status_code}, not {expected_status_code}')
        ret_json = {}
        try:
            ret_json = response.json()
        except TypeError:
            pass
        finally:
            return ret_json

    def post_response_and_check_status_code(self, url: str, data: Union[dict, list], expected_status_code: int = 201,
                                            authorized: bool = True, multipart: bool = False) -> Union[dict, list]:
        client = APIClient()
        if authorized:
            client.force_authenticate(user=self.user)
        if multipart:
            req_data = data
            req_kwargs = {}
        else:
            req_data = json.dumps(data)
            req_kwargs = {'content_type': 'application/json'}
        response = client.post(url, data=req_data, **req_kwargs)
        self.assertEqual(response.status_code, expected_status_code,
                         msg=f'Response status code for {url} is {response.status_code}, not {expected_status_code}')

        ret_json = {}
        try:
            ret_json = response.json()
        except TypeError:
            pass
        finally:
            return ret_json

    def patch_response_and_check_status_code(self, url: str, data: Union[dict, list], expected_status_code: int = 202,
                                             authorized: bool = True, multipart: bool = False) -> Union[dict, list]:
        client = APIClient()
        if authorized:
            client.force_authenticate(user=self.user)
        if multipart:
            req_data = data
            req_kwargs = {}
        else:
            req_data = json.dumps(data)
            req_kwargs = {'content_type': 'application/json'}
        response = client.patch(url, data=req_data, **req_kwargs)
        self.assertEqual(response.status_code, expected_status_code,
                         msg=f'Response status code for {url} is {response.status_code}, not {expected_status_code}')

        ret_json = {}
        try:
            ret_json = response.json()
        except TypeError:
            pass
        finally:
            return ret_json

    def delete_response_and_check_status_code(self, url: str, expected_status_code: int = 204,
                                              authorized: bool = True) -> Union[dict, list]:
        client = APIClient()
        if authorized:
            client.force_authenticate(user=self.user)
        response = client.delete(url)
        self.assertEqual(response.status_code, expected_status_code,
                         msg=f'Response status code for {url} is {response.status_code}, not {expected_status_code}')
        ret_json = {}
        try:
            ret_json = response.json()
        except TypeError:
            pass
        finally:
            return ret_json
