import unittest
from requests import get, post


class TestApp(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api'

    def test_ping(self):
        url = self.base_url + '/ping'
        self.assertEqual(get(url).status_code, 200)

    def test_all_countries(self):
        url = self.base_url + '/countries'
        self.assertEqual(get(url).status_code, 200)

    def test_all_countries_with_region(self):
        url = self.base_url + '/countries?region=Europe&region=Africa'
        self.assertEqual(get(url).status_code, 200)

    def test_countries_by_alpha2(self):
        url = self.base_url + '/countries/RU'
        self.assertEqual(get(url).status_code, 200)

    def test_countries_by_wrong_alpha2(self):
        url = self.base_url + '/countries/QWE'
        self.assertEqual(get(url).status_code, 400)

    def test_registration_without_login(self):
        url = self.base_url + '/auth/register'
        user = {
            'login': '',
            'email': 'general.mayorov@gmail.com',
            'password': '!123456789aA',
            'countryCode': 'RU',
            'isPublic': True,
            'phone': '+79166623069'

        }
        self.assertEqual(post(url, json=user).status_code, 400)

    def test_registration_without_email(self):
        url = self.base_url + '/auth/register'
        user = {
            'login': 'kasad36',
            'email': '',
            'password': '!123456789aA',
            'countryCode': 'RU',
            'isPublic': True,
            'phone': '+79166623069'

        }
        self.assertEqual(post(url, json=user).status_code, 400)

    def test_registration_without_password(self):
        url = self.base_url + '/auth/register'
        user = {
            'login': 'kasad36',
            'email': 'general.mayorov@gmail.com',
            'password': '',
            'countryCode': 'RU',
            'isPublic': True,
            'phone': '+79166623069'

        }
        self.assertEqual(post(url, json=user).status_code, 400)

    def test_registration_without_countrycode(self):
        url = self.base_url + '/auth/register'
        user = {
            'login': 'kasad36',
            'email': 'general.mayorov@gmail.com',
            'password': '!123456789aA',
            'countryCode': '',
            'isPublic': True,
            'phone': '+79166623069'

        }
        self.assertEqual(post(url, json=user).status_code, 400)

    def test_registration_wrong_countrycode(self):
        url = self.base_url + '/auth/register'
        user = {
            'login': 'kasad36',
            'email': 'general.mayorov@gmail.com',
            'password': '!123456789aA',
            'countryCode': 'QWE',
            'isPublic': True,
            'phone': '+79166623069'

        }
        self.assertEqual(post(url, json=user).status_code, 400)

    def test_registration_wrong_phone(self):
        url = self.base_url + '/auth/register'
        user = {
            'login': 'kasad36',
            'email': 'general.mayorov@gmail.com',
            'password': '!123456789aA',
            'countryCode': 'RU',
            'isPublic': True,
            'phone': '89166623069'

        }
        self.assertEqual(post(url, json=user).status_code, 400)


    def test_registration_wrong_image(self):
        url = self.base_url + '/auth/register'
        user = {
            'login': 'kasad36',
            'email': 'general.mayorov@gmail.com',
            'password': '!123456789aA',
            'countryCode': 'RU',
            'isPublic': True,
            'phone': '+79166623069',
            'image': 'a' * 300

        }
        self.assertEqual(post(url, json=user).status_code, 400)

    def test_registration_short_password(self):
        url = self.base_url + '/auth/register'
        user = {
            'login': 'kasad36',
            'email': 'general.mayorov@gmail.com',
            'password': '!123456',
            'countryCode': 'RU',
            'isPublic': True,
            'phone': '+79166623069',

        }
        self.assertEqual(post(url, json=user).status_code, 400)

    def test_registration_bad_password(self):
        url = self.base_url + '/auth/register'
        user = {
            'login': 'kasad36',
            'email': 'general.mayorov@gmail.com',
            'password': '12345678',
            'countryCode': 'RU',
            'isPublic': True,
            'phone': '+79166623069'

        }
        self.assertEqual(post(url, json=user).status_code, 400)

    def test_registration(self):
        url = self.base_url + '/auth/register'
        user = {
            'login': 'kasad36',
            'email': 'general.mayorov@gmail.com',
            'password': '!123456789aA',
            'countryCode': 'RU',
            'isPublic': True,
            'phone': '+79166623069'

        }
        self.assertEqual(post(url, json=user).status_code, 200)
