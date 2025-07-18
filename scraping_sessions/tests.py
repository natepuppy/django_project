from django.test import TestCase
from django.contrib.auth.models import User
from .models import Session
import json

class SessionViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user for authentication
        cls.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        cls.session1 = Session.objects.create(
            platform_user_id=1,
            type='scraping',
            status='running',
            errors_count=0,
            parameters_json={'target': 'linkedin.com'},
            ip_address='192.168.1.100',
            port=8080,
            session_cookies_json={'session_id': 'abc123'}
        )
        cls.session2 = Session.objects.create(
            platform_user_id=2,
            type='automation',
            status='completed',
            errors_count=2,
            parameters_json={'target': 'facebook.com'},
            ip_address='192.168.1.101',
            port=8081,
            session_cookies_json={'session_id': 'def456'}
        )

    def setUp(self):
        # Login the test user before each test
        self.client.login(username='testuser', password='testpass123')

    def test_index_get_successful(self):
        response = self.client.get('/sessions/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Sessions fetched successfully')
        self.assertEqual(len(data['data']), 2)

    def test_show_get_successful(self):
        response = self.client.get('/sessions/1/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Session fetched successfully')
        self.assertEqual(data['data']['id'], 1)

    def test_show_get_not_found(self):
        response = self.client.get('/sessions/999/')
        self.assertEqual(response.status_code, 404)

    def test_index_post_successful(self):
        response = self.client.post('/sessions/', 
            data=json.dumps({
                'platform_user_id': 3,
                'type': 'monitoring',
                'status': 'pending',
                'errors_count': 0,
                'parameters_json': {'target': 'twitter.com'},
                'ip_address': '192.168.1.102',
                'port': 8082,
                'session_cookies_json': {'session_id': 'ghi789'}
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Session created successfully')
        self.assertEqual(Session.objects.count(), 3)

    def test_index_post_invalid_data(self):
        response = self.client.post('/sessions/', 
            data=json.dumps({
                'platform_user_id': 4,
                'type': 'scraping',
                'status': 'pending',
                'errors_count': -1,  # Invalid negative errors count
                'parameters_json': {'target': 'invalid.com'},
                'ip_address': '192.168.1.103',
                'port': 8083,
                'session_cookies_json': {'session_id': 'jkl012'}
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Session creation failed')
        self.assertEqual(Session.objects.count(), 2)

    def test_show_put_successful(self):
        response = self.client.put('/sessions/2/', 
            data=json.dumps({
                'platform_user_id': 2,
                'type': 'automation',
                'status': 'failed',
                'errors_count': 5,
                'parameters_json': {'target': 'facebook.com', 'retry': True},
                'ip_address': '192.168.1.101',
                'port': 8081,
                'session_cookies_json': {'session_id': 'def456', 'retry_count': 1}
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Session updated successfully')
        self.assertEqual(Session.objects.count(), 2)

    def test_show_put_invalid_data(self):
        response = self.client.put('/sessions/2/', 
            data=json.dumps({
                'platform_user_id': 2,
                'type': 'automation',
                'status': 'failed',
                'errors_count': -5,  # Invalid negative errors count
                'parameters_json': {'target': 'facebook.com'},
                'ip_address': '192.168.1.101',
                'port': 8081,
                'session_cookies_json': {'session_id': 'def456'}
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Session update failed')
        self.assertEqual(Session.objects.count(), 2)

    def test_show_delete_successful(self):
        response = self.client.delete('/sessions/1/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Session.objects.count(), 1)

    def test_show_delete_not_found(self):
        response = self.client.delete('/sessions/999/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Session.objects.count(), 2)
