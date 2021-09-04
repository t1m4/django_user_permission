from django.contrib.auth.models import Permission, User
from rest_framework import serializers


class PermissionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(min_value=1)

    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name', ]
        read_only_fields = ['codename', 'name']


class UserSerializer(serializers.ModelSerializer):
    user_permissions = PermissionSerializer(many=True, read_only=True)

    url = serializers.HyperlinkedIdentityField(
        view_name='core-user_detail',
        lookup_url_kwarg='user_id'
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'url', 'user_permissions']
