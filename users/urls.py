from django.urls import path, include
from rest_framework import routers

from users import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'permissions', views.PermissionViewSet, basename='permissions')

urlpatterns = [
    path('', include(router.urls)),
]
