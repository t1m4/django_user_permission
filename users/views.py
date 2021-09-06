from django.contrib.auth.models import User, Permission
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from users.serializers import UserPermissionSerializer, UserSerializer, PermissionSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().prefetch_related('user_permissions')

    def get_serializer_class(self):
        if self.action == 'get_user_permissions':
            return PermissionSerializer
        elif self.action == 'update_user_permissions':
            return UserPermissionSerializer
        return super(UserViewSet, self).get_serializer_class()

    @action(detail=True, methods=['get'], url_path='get_permissions', url_name='get_permissions')
    def get_user_permissions(self, request, pk=None):
        user = self.get_object()
        permissions = user.user_permissions.all()
        serializer = self.get_serializer(permissions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='update_permissions', url_name='update_permissions')
    def update_user_permissions(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path="delete_permissions/(?P<permission_id>\d+?)",
            url_name='delete_permissions')
    def delete_user_permissions(self, request, pk=None, permission_id=None):
        user = self.get_object()
        user_permission = get_object_or_404(user.user_permissions, id=permission_id)
        user.user_permissions.remove(user_permission)
        return Response(status.HTTP_204_NO_CONTENT)


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
