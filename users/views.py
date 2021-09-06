from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from users.serializers import PermissionSerializer, UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().prefetch_related('user_permissions')
    lookup_url_kwarg = 'user_id'

    def get_serializer_class(self):
        if self.action == 'create_permissions' or self.action == 'delete_permissions':
            return PermissionSerializer
        return self.serializer_class

    # @action(detail=True, methods=['get', 'post'], url_path='permissions', url_name="user_permissions-list")
    @action(detail=True, methods=['get', 'post'], url_path='permissions', url_name="permissions_list")
    def create_permissions(self, request, user_id=None):
        if request.method == "POST":
            user = get_object_or_404(User, id=user_id)
            serializer = self.get_serializer_class()(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        user = get_object_or_404(User, id=user_id)
        permissions = user.user_permissions.all()
        serializer = self.get_serializer_class()(permissions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], url_path="permissions/(?P<permission_id>\d+?)",
            url_name='permissions_detail')
    def delete_permissions(self, request, user_id=None, permission_id=None):
        user = get_object_or_404(User, id=user_id)
        print(user_id, permission_id)
        user_permission = get_object_or_404(user.user_permissions, id=permission_id)
        user.user_permissions.remove(user_permission)
        return Response(status.HTTP_204_NO_CONTENT)
