from itertools import chain

from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


def create_users(count_of_users):
    user_data = {
        'email': 'test1@mail.ru',
        'username': 'test',
        'password': 'alksdfjs',
    }
    for index in range(count_of_users):
        user_data = user_data.copy()
        user_data['email'] += str(index)
        user_data['username'] += str(index)
        user_data['password'] += str(index)
        User.objects.create(**user_data)


def get_content_type_permissions(model):
    content_type = ContentType.objects.get(model=model)
    return Permission.objects.filter(content_type=content_type)


class UserListViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_list_url = reverse('users-list')

    def setUp(self):
        create_users(count_of_users=2)

    def test_can_get_users(self):
        response = self.client.get(self.user_list_url)
        result = response.json()
        first_user = result[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(result, list)
        self.assertIsNotNone(first_user.get('id'))
        self.assertIsNotNone(first_user.get('username'))
        self.assertIsNotNone(first_user.get('url'))
        self.assertIsNotNone(first_user.get('user_permissions'))


def create_group():
    location_permissions = get_content_type_permissions('location')
    module_permissions = get_content_type_permissions('module')
    total_permissions = list(chain(location_permissions, module_permissions))
    group = Group.objects.create(name='core_permissions')
    group.permissions.set(total_permissions)


class UserPermissionsListViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.permissions_list_url = reverse('user_permissions-list', kwargs={"user_id": 1})
        cls.invalid_permissions_list_url = reverse('user_permissions-list', kwargs={"user_id": 100})

    def setUp(self):
        create_users(count_of_users=2)

        user = User.objects.first()
        location_permissions = get_content_type_permissions('location')
        user.user_permissions.set(location_permissions)

        create_group()

    def test_can_get_user_permissions(self):
        response = self.client.get(self.permissions_list_url)
        permissions = response.json()
        first_permission = permissions[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(permissions, list)
        self.assertIsNotNone(first_permission.get('id'))
        self.assertIsNotNone(first_permission.get('codename'))
        self.assertIsNotNone(first_permission.get('name'))

    def test_can_add_new_permission(self):
        content_type = ContentType.objects.get(model='module')
        permissions = Permission.objects.filter(content_type=content_type)
        id = permissions[0].id
        response = self.client.post(self.permissions_list_url, {'id': id})
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result['id'], id)

    def test_cannot_add_not_existing_permission(self):
        response = self.client.post(self.permissions_list_url, {'id': 100})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_add_permission_to_not_existing_user(self):
        content_type = ContentType.objects.get(model='module')
        permissions = Permission.objects.filter(content_type=content_type)
        id = permissions[0].id
        response = self.client.post(self.invalid_permissions_list_url, {'id': id})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserPermissionsDetailViewTest(APITestCase):

    def setUp(self):
        create_users(count_of_users=2)

        user = User.objects.first()
        location_permissions = get_content_type_permissions('location')
        user.user_permissions.set(location_permissions)

        create_group()

    def test_can_delete_user_permission(self):
        content_type = ContentType.objects.get(model='location')
        permissions = Permission.objects.filter(content_type=content_type)
        id = permissions.get(codename='view_location').id
        permissions_detail_url = reverse('user_permissions-detail', kwargs={"user_id": 1, "permission_id": id})
        response = self.client.delete(permissions_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_add_not_existing_permission(self):
        permissions_detail_url = reverse('user_permissions-detail', kwargs={"user_id": 1, "permission_id": 100})
        response = self.client.delete(permissions_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_add_permission_to_not_existing_user(self):
        permissions_detail_url = reverse('user_permissions-detail', kwargs={"user_id": 100, "permission_id": 1})
        response = self.client.delete(permissions_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
