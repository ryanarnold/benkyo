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
    path('register/', views.register, name='register'),
    path('register-success/', views.register_success, name='register-success'),

    path('decks/', views.decks, name='decks'),
    path('decks/create/', views.decks_create, name='decks-create'),
    
    path('decks/<int:deck_id>/delete/confirm/', views.decks_delete_confirm, name='decks-delete-confirm'),
    path('decks/<int:deck_id>/delete/', views.decks_delete, name='decks-delete'),

    path('decks/<int:deck_id>/edit/', views.decks_edit, name='decks-edit'),

    path('decks/<int:deck_id>/cards/add/', views.cards_add, name='cards-add'),
    path('decks/<int:deck_id>/cards/<int:card_id>/edit/', views.cards_edit, name='cards-edit'),
    path('decks/<int:deck_id>/cards/<int:card_id>/delete/', views.cards_delete, name='cards-delete'),
    path('decks/<int:deck_id>/cards/delete/all/', views.cards_delete_all, name='cards-delete-all'),

    path('decks/<int:deck_id>/cards/import/', views.cards_import, name='cards-import'),

    path('decks/<int:deck_id>/review/start/', views.review_start, name='review-start'),
    path('decks/<int:deck_id>/review/', views.review, name='review'),
    path('decks/<int:deck_id>/review/assessment/', views.review_assessment, name='review-assessment'),
    path('decks/<int:deck_id>/review/end/', views.review_end, name='review-end'),
]
