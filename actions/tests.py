from django.test import TestCase
from django.contrib.auth.models import User
from .models import Action
import json

class ActionViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user for authentication
        cls.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        cls.action1 = Action.objects.create(
            platform_user_id=1,
            contact_id=1,
            session_id=1,
            type='message',
            status='pending',
            message_text='Hi John, I would like to connect with you!',
            retry_count=0
        )
        cls.action2 = Action.objects.create(
            platform_user_id=1,
            contact_id=2,
            session_id=1,
            type='connection_request',
            status='accepted',
            retry_count=0
        )

    def setUp(self):
        # Login the test user before each test
        self.client.login(username='testuser', password='testpass123')

    def test_index_get_successful(self):
        response = self.client.get('/actions/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Actions fetched successfully')
        self.assertEqual(len(data['data']), 2)

    def test_show_get_successful(self):
        response = self.client.get('/actions/1/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Action fetched successfully')
        self.assertEqual(data['data']['id'], 1)

    def test_show_get_not_found(self):
        response = self.client.get('/actions/999/')
        self.assertEqual(response.status_code, 404)

    def test_index_post_successful(self):
        response = self.client.post('/actions/', 
            data=json.dumps({
                'platform_user_id': 1,
                'contact_id': 3,
                'session_id': 1,
                'type': 'message',
                'status': 'pending',
                'message_text': 'Hi Jane, I would like to connect with you!',
                'retry_count': 0
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Action created successfully')
        self.assertEqual(Action.objects.count(), 3)

    def test_index_post_invalid_data(self):
        response = self.client.post('/actions/', 
            data=json.dumps({
                'platform_user_id': 1,
                'contact_id': 4,
                'session_id': 1,
                'type': 'message',
                'status': 'pending',
                'retry_count': -1  # Invalid negative retry count
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Action creation failed')
        self.assertEqual(Action.objects.count(), 2)

    def test_show_put_successful(self):
        response = self.client.put('/actions/2/', 
            data=json.dumps({
                'platform_user_id': 1,
                'contact_id': 2,
                'session_id': 1,
                'type': 'connection_request',
                'status': 'rejected',
                'error_message': 'User rejected the connection request',
                'retry_count': 1
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Action updated successfully')
        self.assertEqual(Action.objects.count(), 2)

    def test_show_put_invalid_data(self):
        response = self.client.put('/actions/2/', 
            data=json.dumps({
                'platform_user_id': 1,
                'contact_id': 2,
                'session_id': 1,
                'type': 'message',
                'status': 'pending',
                'retry_count': -5  # Invalid negative retry count
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Action update failed')
        self.assertEqual(Action.objects.count(), 2)

    def test_show_delete_successful(self):
        response = self.client.delete('/actions/1/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Action.objects.count(), 1)

    def test_show_delete_not_found(self):
        response = self.client.delete('/actions/999/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Action.objects.count(), 2)
