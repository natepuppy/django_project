from django.test import TestCase
from django.contrib.auth.models import User
from .models import Contact
import json

class ContactViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user for authentication
        cls.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        cls.contact1 = Contact.objects.create(
            platform_user_id=1,
            session_id=1,
            external_id='linkedin_123',
            profile_url='https://www.linkedin.com/in/john-doe',
            first_name='John',
            last_name='Doe',
            name='John Doe',
            email='john.doe@example.com',
            phone='+1234567890',
            tags=['developer', 'python'],
            notes='Great developer, worked at Google',
            profile_type='person',
            headline='Senior Software Engineer',
            industry='Technology',
            location='San Francisco, CA',
            about='Passionate about building great software',
            connections_count=500,
            followers_count=1000,
            metadata={'company': 'Google', 'experience': '10 years'},
            is_connection=True
        )
        cls.contact2 = Contact.objects.create(
            platform_user_id=1,
            session_id=1,
            external_id='linkedin_456',
            profile_url='https://www.linkedin.com/in/jane-smith',
            first_name='Jane',
            last_name='Smith',
            name='Jane Smith',
            email='jane.smith@example.com',
            phone='+1234567891',
            tags=['designer', 'ui'],
            notes='Excellent UI/UX designer',
            profile_type='person',
            headline='Senior UI/UX Designer',
            industry='Design',
            location='New York, NY',
            about='Creating beautiful user experiences',
            connections_count=300,
            followers_count=800,
            metadata={'company': 'Apple', 'experience': '8 years'},
            is_connection=False
        )

    def setUp(self):
        # Login the test user before each test
        self.client.login(username='testuser', password='testpass123')

    def test_index_get_successful(self):
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Contacts fetched successfully')
        self.assertEqual(len(data['data']), 2)

    def test_show_get_successful(self):
        response = self.client.get('/contacts/1/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Contact fetched successfully')
        self.assertEqual(data['data']['id'], 1)

    def test_show_get_not_found(self):
        response = self.client.get('/contacts/999/')
        self.assertEqual(response.status_code, 404)

    def test_index_post_successful(self):
        response = self.client.post('/contacts/', 
            data=json.dumps({
                'platform_user_id': 1,
                'session_id': 1,
                'external_id': 'linkedin_789',
                'profile_url': 'https://www.linkedin.com/in/test-user',
                'first_name': 'Test',
                'last_name': 'User',
                'name': 'Test User',
                'email': 'test.user@example.com',
                'phone': '+1234567892',
                'tags': ['manager', 'product'],
                'notes': 'Product manager at startup',
                'profile_type': 'person',
                'headline': 'Product Manager',
                'industry': 'Technology',
                'location': 'Austin, TX',
                'about': 'Building great products',
                'connections_count': 200,
                'followers_count': 500,
                'metadata': {'company': 'Startup', 'experience': '5 years'},
                'is_connection': True
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Contact created successfully')
        self.assertEqual(Contact.objects.count(), 3)

    def test_index_post_invalid_data(self):
        response = self.client.post('/contacts/', 
            data=json.dumps({
                'platform_user_id': 1,
                'session_id': 1,
                'connections_count': -1,  # Invalid negative connections count
                'profile_type': 'person',
                'is_connection': True
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Contact creation failed')
        self.assertEqual(Contact.objects.count(), 2)

    def test_show_put_successful(self):
        response = self.client.put('/contacts/2/', 
            data=json.dumps({
                'platform_user_id': 1,
                'session_id': 1,
                'first_name': 'Jane',
                'last_name': 'Smith Updated',
                'name': 'Jane Smith Updated',
                'email': 'jane.updated@example.com',
                'headline': 'Senior UI/UX Designer & Manager',
                'connections_count': 400,
                'followers_count': 900,
                'is_connection': True,
                'notes': 'Excellent UI/UX designer, now a manager'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Contact updated successfully')
        self.assertEqual(Contact.objects.count(), 2)

    def test_show_put_invalid_data(self):
        response = self.client.put('/contacts/2/', 
            data=json.dumps({
                'platform_user_id': 1,
                'session_id': 1,
                'followers_count': -100,  # Invalid negative followers count
                'profile_type': 'person',
                'is_connection': True
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Contact update failed')
        self.assertEqual(Contact.objects.count(), 2)

    def test_show_delete_successful(self):
        response = self.client.delete('/contacts/1/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Contact.objects.count(), 1)

    def test_show_delete_not_found(self):
        response = self.client.delete('/contacts/999/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Contact.objects.count(), 2)
