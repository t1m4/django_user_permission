from django.urls import path
from core import views

urlpatterns = [
    path('permissions/', views.PermissionListView.as_view(), name='core-permission_list'),
    path('users/', views.UserListView.as_view(), name='core-user_list'),
    path('users/<int:user_id>/', views.UserDetailView.as_view(), name='core-user_detail'),
    path('users/<int:user_id>/permissions/', views.UserPermissionsListView.as_view(), name='core-user_permissions_list'),
]