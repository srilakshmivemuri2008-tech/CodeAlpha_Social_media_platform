from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('explore/', views.explore, name='explore'),

    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),

    path('u/<str:username>/', views.profile, name='profile'),
    path('u/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
