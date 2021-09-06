from django.contrib.auth.models import Permission, User, Group
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404


class PermissionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(min_value=1)

    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name', ]
        read_only_fields = ['codename', 'name']

    def save(self, user):
        permission = get_object_or_404(Permission, id=self.validated_data['id'])
        group = Group.objects.get(name='core_permissions')
        allowed_permissions = group.permissions.all()
        if permission in allowed_permissions:
            user = user
            user.user_permissions.add(permission)
        else:
            raise NotFound(detail="Not Found.")


class UserSerializer(serializers.ModelSerializer):
    user_permissions = PermissionSerializer(many=True, read_only=True)

    url = serializers.HyperlinkedIdentityField(
        view_name='users-detail',
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'url', 'user_permissions']
