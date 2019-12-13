from django.test import TestCase
from .models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

def create_pre_user(number):
    name  = 'test' + str(number)
    user = User.objects.create(username=name, email=name+'@test.com',date_of_birth='2000-12-12')
    user.set_password('pass1234')
    user.save()
    Token.objects.get_or_create(user=user)
    return user

class login_TestCase(TestCase):
    client = APIClient()
    test_url = '/account/auth/'

    def setUp(self):
        create_pre_user(1)

    def test_response_success(self):
        user = User.objects.get(username='test1')
        res = self.client.post(self.test_url, {'email':user.email,'password':'pass1234'} ,format='json')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.data['token'],user.auth_token.key)
        self.assertEqual(res.data['outcome'],'success')

class get_user_and_profile_with_content(TestCase):
    client = APIClient()
    test_url = '/account/auth/'

    def setUp(self):
        create_pre_user(1)
        create_pre_user(2)

    def test_response_success(self):
        user = User.objects.get(username='test1')
        user2 = User.objects.get(username='test2')
        user.profile.following.add(user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
        res = self.client.post(self.test_url+'/test2', {} ,format='json')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.data['outcome'],'success')
