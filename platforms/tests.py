from django.test import TestCase
from .models import Platform
import json
import pdb

class PlatformViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.platform1 = Platform.objects.create(
            name='LinkedIn',
            base_url='https://www.linkedin.com',
            login_url='https://www.linkedin.com/login',
            has_captcha=False,
            is_active=True
        )
        cls.platform2 = Platform.objects.create(
            name='Facebook',
            base_url='https://www.facebook.com',
            login_url='https://www.facebook.com/login',
            has_captcha=False,
            is_active=True
        )

    def test_index_valid_id(self):
        response = self.client.get('/platforms/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Platforms fetched successfully')
        self.assertEqual(len(data['data']), 2)

    def test_show_valid_id(self):
        response = self.client.get(f'/platforms/show/{self.platform1.id}/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Platform fetched successfully')
        self.assertEqual(data['data']['id'], 1)

    def test_show_invalid_id(self):
        response = self.client.get('/platforms/show/1234567890/')
        self.assertEqual(response.status_code, 404)
        content = response.content.decode('utf-8')
        self.assertIn("The requested resource was not found on this server.", content)
        self.assertEqual(Platform.objects.count(), 2)

    def test_create_valid_params(self):
        payload = {
            'name': 'Test Platform',
            'base_url': 'https://test.com',
            'login_url': 'https://test.com/login',
            'has_captcha': False,
            'is_active': True
        }

        response = self.client.post('/platforms/create/',
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Platform created successfully')
        self.assertEqual(Platform.objects.count(), 3)

    def test_create_invalid_params(self):
        payload = {
            'name': '',
            'base_url': 'https://test.com',
            'login_url': 'https://test.com/login',
            'has_captcha': False,
            'is_active': True
        }

        response = self.client.post('/platforms/create/',
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Platform creation failed')
        self.assertEqual(Platform.objects.count(), 2)

    def test_update_valid_params(self):
        payload = {
            'name': 'Test Platform',
            'base_url': 'https://test.com',
            'login_url': 'https://test.com/login',
            'has_captcha': False,
            'is_active': True
        }

        response = self.client.put(
            f'/platforms/update/{self.platform1.id}/',
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Platform updated successfully')
        self.assertEqual(Platform.objects.count(), 2)

    def test_update_invalid_params(self):
        payload = {
            'name': '',
            'base_url': 'https://test.com',
            'login_url': 'https://test.com/login',
            'has_captcha': False,
            'is_active': True
        }

        response = self.client.put(
            f'/platforms/update/{self.platform1.id}/',
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Platform update failed')
        self.assertEqual(Platform.objects.count(), 2)

    def test_destroy_valid_id(self):
        response = self.client.delete(f'/platforms/delete/{self.platform1.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Platform.objects.count(), 1)

    def test_destroy_invalid_id(self):
        response = self.client.delete('/platforms/delete/1234567890/')
        self.assertEqual(response.status_code, 404)
        content = response.content.decode('utf-8')
        self.assertIn("The requested resource was not found on this server.", content)
        self.assertEqual(Platform.objects.count(), 2)
