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


# class PermissionHyperlink(serializers.HyperlinkedIdentityField):
#     view_name = 'core-user_permission_detail'
#
#     def get_url(self, obj, view_name, request, format):
#         url_kwargs = self.context['view'].kwargs
#         return reverse(view_name, kwargs=url_kwargs, request=request, format=format)
#
# class UserPermissionsSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(min_value=1)
#
#     permission_url = PermissionHyperlink(view_name='core-user_permission_detail')
#     class Meta:
#         model = Permission
#         # fields = ['id', 'codename', 'name', ]
#         fields = ['id', 'codename', 'name', 'permission_url']
#         read_only_fields = ['codename', 'name', 'permission_url']
