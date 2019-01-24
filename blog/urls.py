from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:blogId>/', views.blog, name='blog'),
    path('new/', views.new, name='new'),
    path('updateBlogDatabase1357/<int:blogId>/', views.updateBlogDatabase1357, name='updateBlogDatabase1357'),
    path('updateUserDatabase1357/', views.updateUserDatabase1357, name='updateUserDatabase1357'),

]