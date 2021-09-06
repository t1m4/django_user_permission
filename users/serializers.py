from django.contrib.auth.models import Permission, User
from rest_framework import serializers


class UserPermissionSerializer(serializers.ModelSerializer):
    permission = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all())

    class Meta:
        model = User
        fields = ['permission', ]

    def save(self, user):
        user.user_permissions.add(self.validated_data['permission'])


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name', ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', ]
