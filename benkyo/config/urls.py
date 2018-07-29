"""benkyo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from benkyo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/?(?P<password_mismatch>\d+)?/?', views.register, name='register'),
    path('register/', views.register, name='register'),
    path('authenticate-user/', views.authenticate_user, name='authenticate-user'),
    path('create-user/', views.create_user, name='create-user'),
    path('register-success/', views.register_success, name='register-success'),

    path('decks/', views.decks, name='decks'),
    path('decks/create/', views.decks_create, name='decks-create'),
    path('decks/create/successful/', views.decks_create_successful, name='decks-create-successful'),
    
    path('decks/<int:deck_id>/delete/confirm/', views.decks_delete_confirm, name='decks-delete-confirm'),
    path('decks/<int:deck_id>/delete/', views.decks_delete_confirm, name='decks-delete'),
    path('decks/delete/success', views.decks_delete_confirm, name='decks-delete-success'),
]
