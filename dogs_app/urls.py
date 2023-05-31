from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('logout/', views.logout_user_view, name='logout'),
    path('register/', views.register_user_view, name='register'),

]
