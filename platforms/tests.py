from django.test import TestCase
from .models import Platform
import json

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

    def test_index_get_successful(self):
        response = self.client.get('/platforms/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Platforms fetched successfully')
        self.assertEqual(len(data['data']), 2)

    def test_show_get_successful(self):
        response = self.client.get('/platforms/1/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Platform fetched successfully')
        self.assertEqual(data['data']['id'], 1)

    def test_show_get_not_found(self):
        response = self.client.get('/platforms/999/')
        self.assertEqual(response.status_code, 404)

    def test_index_post_successful(self):
        response = self.client.post('/platforms/', 
            data=json.dumps({
                'name': 'Test Platform',
                'base_url': 'https://test.com',
                'login_url': 'https://test.com/login',
                'has_captcha': False,
                'is_active': True
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Platform created successfully')
        self.assertEqual(Platform.objects.count(), 3)

    def test_index_post_invalid_data(self):
        response = self.client.post('/platforms/', 
            data=json.dumps({
                'name': '',  # Invalid empty name
                'base_url': 'https://test.com',
                'login_url': 'https://test.com/login',
                'has_captcha': False,
                'is_active': True
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Platform creation failed')
        self.assertEqual(Platform.objects.count(), 2)

    def test_show_put_successful(self):
        response = self.client.put('/platforms/1/', 
            data=json.dumps({
                'name': 'LinkedIn Updated',
                'base_url': 'https://www.linkedin.com',
                'login_url': 'https://www.linkedin.com/login',
                'has_captcha': True,
                'is_active': False
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Platform updated successfully')
        self.assertEqual(Platform.objects.count(), 2)

    def test_show_put_invalid_data(self):
        response = self.client.put('/platforms/1/', 
            data=json.dumps({
                'name': '',  # Invalid empty name
                'base_url': 'https://www.linkedin.com',
                'login_url': 'https://www.linkedin.com/login',
                'has_captcha': True,
                'is_active': False
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Platform update failed')
        self.assertEqual(Platform.objects.count(), 2)

    def test_show_delete_successful(self):
        response = self.client.delete('/platforms/1/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Platform.objects.count(), 1)

    def test_show_delete_not_found(self):
        response = self.client.delete('/platforms/999/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Platform.objects.count(), 2)
