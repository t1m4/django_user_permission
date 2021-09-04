from django.urls import path
from users import views

urlpatterns = [
    path('permissions/', views.PermissionListView.as_view(), name='users-permission_list'),
    path('users/', views.UserListView.as_view(), name='users-user_list'),
    path('users/<int:user_id>/', views.UserDetailView.as_view(), name='users-user_detail'),
    path('users/<int:user_id>/permissions/', views.UserPermissionsListView.as_view(), name='users-user_permissions_list'),
    path('users/<int:user_id>/permissions/<int:permission_id>/', views.UserPermissionsDetailView.as_view(), name='users-user_permission_detail'),
]