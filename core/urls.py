from django.urls import path

from . import views

urlpatterns = [
    path('', views.top, name='top'),
    path('search/', views.word_search, name='word_search'),
    path('register/', views.register_word, name='register_word'),
    path('list/', views.word_list, name='word_list'),
    path('create/', views.word_create, name='word_create'),
    path('flashcards/', views.flashcards, name='flashcards'),
    path('list/<int:pk>/edit/', views.word_edit, name='word_edit'),
    path('list/<int:pk>/delete/', views.word_delete, name='word_delete'),
]