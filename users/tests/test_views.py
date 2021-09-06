from django.contrib.auth.models import User, Permission
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


class UserViewSetTest(APITestCase):

    def setUp(self):
        self.user_list_url = reverse('users-list')
        self.user_detail_url = reverse('users-detail', kwargs={'pk': 1})
        self.user_get_permissions_url = reverse('users-get_permissions', kwargs={'pk': 1})
        self.user_update_permissions_url = reverse('users-update_permissions', kwargs={'pk': 1})
        create_users(count_of_users=2)

        user = User.objects.first()
        location_permissions = get_content_type_permissions('location')
        user.user_permissions.set(location_permissions)

    def test_can_get_users(self):
        response = self.client.get(self.user_list_url)
        result = response.json()
        first_user = result[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(result, list)
        self.assertIsNotNone(first_user.get('id'))
        self.assertIsNotNone(first_user.get('username'))

    def test_can_get_user(self):
        response = self.client.get(self.user_detail_url)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(result, dict)
        self.assertIsNotNone(result.get('id'))
        self.assertIsNotNone(result.get('username'))

    def test_can_get_user_permissions(self):
        response = self.client.get(self.user_get_permissions_url)
        permissions = response.json()
        first_permission = permissions[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(permissions, list)
        self.assertIsNotNone(first_permission.get('id'))
        self.assertIsNotNone(first_permission.get('codename'))
        self.assertIsNotNone(first_permission.get('name'))

    def test_can_update_user_permission(self):
        permission = Permission.objects.all().first()
        response = self.client.post(self.user_update_permissions_url, {'permission': permission.id})
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result['permission'], permission.id)

    def test_cannot_update_user_permission_with_not_exist_user(self):
        user_update_permissions_url = reverse('users-update_permissions', kwargs={'pk': User.objects.last().id + 1})
        permission = Permission.objects.all().first()
        response = self.client.post(user_update_permissions_url, {'permission': permission.id})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_update_user_permission_with_not_exist_permission(self):
        user_update_permissions_url = reverse('users-update_permissions', kwargs={'pk': 1})
        permission = Permission.objects.order_by('id').last()
        response = self.client.post(user_update_permissions_url, {'permission': permission.id + 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_delete_user_permission(self):
        user = User.objects.get(id=1)
        user_permission = user.user_permissions.all()
        user_delete_permissions_url = reverse('users-delete_permissions',
                                              kwargs={'pk': 1, 'permission_id': f'{user_permission[0].id}'})
        response = self.client.delete(user_delete_permissions_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_delete_user_permission_with_not_exist_user(self):
        user = User.objects.get(id=1)
        user_permissions = user.user_permissions.all()
        user_delete_permissions_url = reverse('users-delete_permissions',
                                              kwargs={'pk': User.objects.last().id + 1,
                                                      'permission_id': f'{user_permissions[0].id}'})
        response = self.client.delete(user_delete_permissions_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_delete_user_permission_with_not_exist_permission(self):
        user = User.objects.get(id=1)
        user_permission = user.user_permissions.order_by('id').last()
        user_delete_permissions_url = reverse('users-delete_permissions',
                                              kwargs={'pk': User.objects.last().id + 1,
                                                      'permission_id': f'{user_permission.id + 1}'})
        response = self.client.delete(user_delete_permissions_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
