from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:blogId>/', views.blog, name='blog'),
    path('new/', views.new, name='new'),
    path('updateBlogDatabase/<int:blogId>/', views.updateBlogDatabase, name='updateBlogDatabase'),
path('updateUserDatabase/', views.updateUserDatabase, name='updateUserDatabase'),

]