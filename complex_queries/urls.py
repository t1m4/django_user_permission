from django.urls import path

from complex_queries import views

urlpatterns = [
    path('test/', views.TestView.as_view())
]
