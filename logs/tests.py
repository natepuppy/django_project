from django.test import TestCase
from django.contrib.auth.models import User
from .models import Log
import json

class LogViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user for authentication
        cls.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        cls.log1 = Log.objects.create(
            user_id=1,
            platform_user_id=1,
            platform_id=1,
            session_id=1,
            contact_id=1,
            action_id=1,
            type='info',
            message='Session started successfully',
            code=None,
            code_path='logs/views.py:25'
        )
        cls.log2 = Log.objects.create(
            user_id=1,
            platform_user_id=1,
            platform_id=1,
            session_id=1,
            contact_id=2,
            action_id=2,
            type='error',
            message='Failed to send connection request',
            code='ERROR',
            code_path='actions/views.py:45'
        )

    def setUp(self):
        # Login the test user before each test
        self.client.login(username='testuser', password='testpass123')

    def test_index_get_successful(self):
        response = self.client.get('/logs/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Logs fetched successfully')
        self.assertEqual(len(data['data']), 2)

    def test_show_get_successful(self):
        response = self.client.get('/logs/1/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Log fetched successfully')
        self.assertEqual(data['data']['id'], 1)

    def test_show_get_not_found(self):
        response = self.client.get('/logs/999/')
        self.assertEqual(response.status_code, 404)

    def test_index_post_successful(self):
        response = self.client.post('/logs/', 
            data=json.dumps({
                'user_id': 1,
                'platform_user_id': 1,
                'platform_id': 1,
                'session_id': 1,
                'contact_id': 3,
                'action_id': 3,
                'type': 'warning',
                'message': 'Connection request pending for too long',
                'code': 'WARNING',
                'code_path': 'actions/views.py:67'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Log created successfully')
        self.assertEqual(Log.objects.count(), 3)

    def test_index_post_invalid_data(self):
        response = self.client.post('/logs/', 
            data=json.dumps({
                'user_id': 1,
                'platform_user_id': 1,
                'type': 'info',
                'message': '',  # Invalid empty message
                'code': None,
                'code_path': 'logs/views.py:25'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Log creation failed')
        self.assertEqual(Log.objects.count(), 2)

    def test_show_put_successful(self):
        response = self.client.put('/logs/2/', 
            data=json.dumps({
                'user_id': 1,
                'platform_user_id': 1,
                'platform_id': 1,
                'session_id': 1,
                'contact_id': 2,
                'action_id': 2,
                'type': 'error',
                'message': 'Failed to send connection request - retry successful',
                'code': 'ERROR',
                'code_path': 'actions/views.py:45'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Log updated successfully')
        self.assertEqual(Log.objects.count(), 2)

    def test_show_put_invalid_data(self):
        response = self.client.put('/logs/2/', 
            data=json.dumps({
                'user_id': 1,
                'platform_user_id': 1,
                'type': 'error',
                'message': '',  # Invalid empty message
                'code': 'ERROR',
                'code_path': 'actions/views.py:45'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Log update failed')
        self.assertEqual(Log.objects.count(), 2)

    def test_show_delete_successful(self):
        response = self.client.delete('/logs/1/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Log.objects.count(), 1)

    def test_show_delete_not_found(self):
        response = self.client.delete('/logs/999/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Log.objects.count(), 2)
