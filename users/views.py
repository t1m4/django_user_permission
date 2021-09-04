from django.contrib.auth.models import User, Group
from rest_framework import generics
from rest_framework.generics import get_object_or_404

from users.serializers import PermissionSerializer, UserSerializer


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all().prefetch_related('user_permissions')


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "user_id"


class PermissionListView(generics.ListAPIView):
    serializer_class = PermissionSerializer

    def get_queryset(self):
        group = Group.objects.get(name='core_permissions')
        return group.permissions.all()


class UserPermissionsListView(generics.ListCreateAPIView):
    """
    Get all user permissions and create new one
    """
    serializer_class = PermissionSerializer
    lookup_url_kwarg = "user_id"

    def get_current_user(self):
        user_lookup_url_kwarg = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(User, id=user_lookup_url_kwarg)

    def get_queryset(self):
        user = self.get_current_user()
        return user.user_permissions.all()

    def perform_create(self, serializer):
        user = self.get_current_user()
        serializer.save(user=user)


class UserPermissionsDetailView(generics.RetrieveAPIView,
                                generics.DestroyAPIView):
    """
    Retrieve user permission and delete them
    """
    serializer_class = PermissionSerializer
    lookup_url_kwarg = "permission_id"
    user_lookup = "user_id"

    def get_current_user(self):
        user_lookup_url_kwarg = self.kwargs.get(self.user_lookup)
        return get_object_or_404(User, id=user_lookup_url_kwarg)

    def get_queryset(self):
        user = self.get_current_user()
        return user.user_permissions.all()

    def perform_destroy(self, permission):
        user = self.get_current_user()
        user.user_permissions.remove(permission)
