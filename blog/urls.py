from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('r/<slug:category_slug>/', views.home, name='category'),
    path('categories/new/', views.category_create, name='category_create'),
    path('categories/<slug:slug>/verify/', views.category_verify, name='category_verify'),
    path('categories/<slug:slug>/unverify/', views.category_unverify, name='category_unverify'),
    path('categories/<slug:slug>/delete/', views.category_delete, name='category_delete'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/vote/<str:action>/', views.vote, name='vote'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('u/<str:username>/', views.user_profile, name='profile'),
    path('settings/profile/', views.profile_settings, name='profile_settings'),
]
