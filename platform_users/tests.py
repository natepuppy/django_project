from django.test import TestCase
from django.contrib.auth.models import User
from .models import PlatformUser
import json

class PlatformUserViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user for authentication
        cls.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        cls.platform_user1 = PlatformUser.objects.create(
            user_id=1,
            platform_id=1,
            username='john_doe',
            email='john@example.com',
            encrypted_password='encrypted_password_123',
            status='active',
            daily_connection_request=50,
            weekly_connection_request_limit=200,
            daily_connection_request_count=0,
            weekly_connection_request_count=0
        )
        cls.platform_user2 = PlatformUser.objects.create(
            user_id=2,
            platform_id=1,
            username='jane_smith',
            email='jane@example.com',
            encrypted_password='encrypted_password_456',
            status='active',
            daily_connection_request=30,
            weekly_connection_request_limit=150,
            daily_connection_request_count=0,
            weekly_connection_request_count=0
        )

    def setUp(self):
        # Login the test user before each test
        self.client.login(username='testuser', password='testpass123')

    def test_index_get_successful(self):
        response = self.client.get('/platform_users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Platform users fetched successfully')
        self.assertEqual(len(data['data']), 2)

    def test_show_get_successful(self):
        response = self.client.get('/platform_users/1/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Platform user fetched successfully')
        self.assertEqual(data['data']['id'], 1)

    def test_show_get_not_found(self):
        response = self.client.get('/platform_users/999/')
        self.assertEqual(response.status_code, 404)

    def test_index_post_successful(self):
        response = self.client.post('/platform_users/', 
            data=json.dumps({
                'user_id': 3,
                'platform_id': 1,
                'username': 'test_user',
                'email': 'test@example.com',
                'encrypted_password': 'encrypted_password_789',
                'status': 'active',
                'daily_connection_request': 25,
                'weekly_connection_request_limit': 100,
                'daily_connection_request_count': 0,
                'weekly_connection_request_count': 0
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Platform user created successfully')
        self.assertEqual(PlatformUser.objects.count(), 3)

    def test_index_post_invalid_data(self):
        response = self.client.post('/platform_users/', 
            data=json.dumps({
                'user_id': 4,
                'platform_id': 1,
                'username': '',  # Invalid empty username
                'email': 'invalid@example.com',
                'encrypted_password': 'encrypted_password_999',
                'status': 'active',
                'daily_connection_request': 25,
                'weekly_connection_request_limit': 100,
                'daily_connection_request_count': 0,
                'weekly_connection_request_count': 0
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Platform user creation failed')
        self.assertEqual(PlatformUser.objects.count(), 2)

    def test_show_put_successful(self):
        response = self.client.put('/platform_users/2/', 
            data=json.dumps({
                'user_id': 2,
                'platform_id': 1,
                'username': 'jane_updated',
                'email': 'jane.updated@example.com',
                'encrypted_password': 'encrypted_password_456',
                'status': 'inactive',
                'daily_connection_request': 40,
                'weekly_connection_request_limit': 180,
                'daily_connection_request_count': 5,
                'weekly_connection_request_count': 20
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Platform user updated successfully')
        self.assertEqual(PlatformUser.objects.count(), 2)

    def test_show_put_invalid_data(self):
        response = self.client.put('/platform_users/2/', 
            data=json.dumps({
                'user_id': 2,
                'platform_id': 1,
                'username': '',  # Invalid empty username
                'email': 'jane.updated@example.com',
                'encrypted_password': 'encrypted_password_456',
                'status': 'inactive',
                'daily_connection_request': 40,
                'weekly_connection_request_limit': 180,
                'daily_connection_request_count': 5,
                'weekly_connection_request_count': 20
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Platform user update failed')
        self.assertEqual(PlatformUser.objects.count(), 2)

    def test_show_delete_successful(self):
        response = self.client.delete('/platform_users/1/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(PlatformUser.objects.count(), 1)

    def test_show_delete_not_found(self):
        response = self.client.delete('/platform_users/999/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(PlatformUser.objects.count(), 2)
