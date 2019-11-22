from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

from .models import Membership, UserMembership

# Create your tests here.

class UserMembershipTestCase(APITestCase):
    def setUp(self):
        user_obj = User(username='test_user', email='test@test.com')
        membership = Membership(slug='Free', membership_type='Professional', price=30.0)
        membership.save()
        # membership = Membership.objects.filter(membership_type='Professional').first()
        print(membership)
        user_obj.set_password("password")
        user_obj.save()
        user_membership = UserMembership.objects.create(user=user_obj, membership=membership)

    def test_user_membership(self):
        user_membership = UserMembership.objects.count()
        self.assertEqual(user_membership, 1)

    def test_get_list(self):
        data = {}
        url = api_reverse("subscription:user-membership-list")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    def test_update_user(self):
        user_membership = UserMembership.objects.first()
        url = user_membership.get_api_url()
        data = {"membership_type": "Free"}
        response = self.client.post(url, data, format='json')
        #self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        #response = self.client.put(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_with_user(self):
        user_membership = UserMembership.objects.first()
        url = user_membership.get_api_url()
        data = {"membership_type": "Free"}
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT' + token_rsp)  # JWT <token>
        response = self.client.put(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


