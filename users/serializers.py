from django.contrib.auth.models import Permission, User
from rest_framework import serializers
from rest_framework.generics import get_object_or_404


class UserPermissionSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)

    def save(self, user):
        permission = get_object_or_404(Permission, id=self.validated_data['id'])
        user.user_permissions.add(permission)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name', ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', ]
