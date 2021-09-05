from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404

from users.serializers import PermissionSerializer, UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().prefetch_related('user_permissions')
    lookup_url_kwarg = 'user_id'


class UserPermissionViewSet(mixins.RetrieveModelMixin,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = PermissionSerializer
    lookup_url_kwarg = 'permission_id'
    user_lookup_field = 'user_id'

    def get_current_user(self):
        user_lookup_url_kwarg = self.kwargs.get(self.user_lookup_field)
        return get_object_or_404(User, id=user_lookup_url_kwarg)

    def get_queryset(self):
        user = self.get_current_user()
        return user.user_permissions.all()

    def perform_create(self, serializer):
        user = self.get_current_user()
        serializer.save(user=user)

    def perform_destroy(self, permission):
        user = self.get_current_user()
        user.user_permissions.remove(permission)
