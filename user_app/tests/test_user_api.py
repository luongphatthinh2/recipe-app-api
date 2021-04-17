from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

#import module of django rest framework
from  rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user_app:create')
TOKEN_URL = reverse('user_app:token')

def craete_user(**params): # helper function
    return get_user_model().objects.create_user(**params)

class PublicUserAPITests(TestCase): # for unauthenticated user
    """
    Test the user API ( public) for unauthenticated user 
    """
    def setUp(self) :
        self.client = APIClient()
    
    def test_create_valid_user_successfully(self):
        """Test creating user with valid payload successfully"""
        payload = {
            'email':'thinh@gmail.com',
            'password': '123456789',
            'name': 'Thinh luong 2109'
        }
        response = self.client.post(CREATE_USER_URL,payload) # response is a Response object in django
        
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        user  = get_user_model().objects.get(**response.data) # **response.data == payload

        self.assertTrue(user.check_password(payload['password'])) 

        self.assertNotIn('password',response.data)

    def test_user_exists(self):
        """Test creating  a user that already exists fails"""
        payload = {
            'email':'thinh@gmail.com',
            'password': '123456789',
            'name': 'Thinh luong 2109'
        }
        craete_user(**payload)

        response = self.client.post(CREATE_USER_URL,payload)# response is a Response object in django
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ Test that the password must be more than 5 characters"""
        payload = {
            'email':'thinh@gmail.com',
            'password': '1234',
            'name': 'Thinh luong 2109'
        }   
        response = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

        user_exits = get_user_model().objects.filter(
            email = payload['email'],
        ).exists()

        self.assertFalse(user_exits)

    def test_create_token_for_user(self):
        """Test that a token is created for user"""
        payload = {
            'email':'thinh@gmail.com',
            'password' : '122456789'
        }
        craete_user(**payload)
        response = self.client.post(TOKEN_URL,payload)

        self.assertIn('token',response.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """  Test that token is not created if invalid credentials are given"""
        craete_user(email = 'thinh@gmail.com',password='123456789')
        payload = {
            'email':'thinh@gmail.com',
            'password': 'wrong',
        }
        response = self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',response.data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test  that token is not  created  if user does not exist"""
        payload = {
            'email':'thinh@gmail.com',
            'password': 'wrong',
        }
        response = self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',response.data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_password(self):
        """ Test that email and password are required"""
        response = self.client.post(TOKEN_URL,{'email':'thinh@gmail.com','password':''})
        self.assertNotIn('token',response.data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)