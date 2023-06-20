from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('logout/', views.logout_user_view, name='logout'),
    path('register/', views.register_user_view, name='register'),
    path('dog/<int:pk>', views.dog_record_view, name='dog_record'),
    path('delete_dog/<int:pk>', views.delete_dog_view, name='delete_dog'),
    path('add_dog/', views.add_dog_view, name='add_dog'),
    path('update_dog/<int:pk>', views.update_dog_view, name='update_dog'),
    path('view_users/', views.view_users, name='view_users'),
    path('delete_user/<int:pk>', views.delete_user_view, name='delete_user'),
    path('update_user/<int:pk>', views.update_user_view, name='update_user'),
    path('update_user_self/', views.update_user_self_view, name='update_user_self'),
    path('add_news/', views.add_news, name='add_news'),
    path('update_news/<int:news_id>/', views.update_news, name='update_news'),
    path('delete_news/<int:news_id>/', views.delete_news, name='delete_news'),
]
