from django.urls import path

from . import views

urlpatterns = [
    path('<str:username>/', views.index, name='index'),
    path('settings/social/', views.social, name='social'),
]
