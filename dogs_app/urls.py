from django.urls import path, include
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('toggle_branch/', views.toggle_branch, name='toggle_branch'),          # Toggle branch
    path('italy/', views.set_italy_branch, name='set_italy_branch'),            # Set Italy branch
    path('israel/', views.set_israel_branch, name='set_israel_branch'),         # Set Israel branch
    path('logout/', views.logout_user_view, name='logout'),
    path('accounts/login/', views.login_user_view, name='login'),
    path('register/', views.register_user_view, name='register'),
    path('dog/<int:pk>', views.dog_record_view, name='dog_record'),
    path('observations/<int:session_id>/', views.view_observations, name='view_observations'),
    path('delete_observation/', views.delete_observation, name='delete_observation'),
    path('edit_observation/<int:observation_id>/', views.edit_observation, name='edit_observation'),
    path('delete_stance/', views.delete_stance, name='delete_stance'),
    path('edit_dog_stance/<int:stance_id>/', views.edit_dog_stance, name='edit_dog_stance'),
    path('delete_dog/<int:pk>', views.delete_dog_view, name='delete_dog'),
    path('add_dog/', views.add_dog_view, name='add_dog'),
    path('update_dog/<int:pk>', views.update_dog_view, name='update_dog'),
    path('edit_owner/<int:owner_id>/', views.edit_owner, name='edit_owner'),
    path('delete_treatment/<int:treatment_id>/', views.delete_treatment, name='delete_treatment'),
    path('delete_examination/<int:examination_id>/', views.delete_examination, name='delete_examination'),
    path('delete_placement/<int:placement_id>/', views.delete_placement, name='delete_placement'),
    path('delete_session/<int:session_id>/', views.delete_session, name='delete_session'),
    path('edit_treatment/<int:treatment_id>/', views.edit_treatment, name='edit_treatment'),
    path('edit_examination/<int:examination_id>/', views.edit_examination, name='edit_examination'),
    path('edit_placement/<int:placement_id>/', views.edit_placement, name='edit_placement'),
    path('edit_session/<int:session_id>/', views.edit_session, name='edit_session'),
    path('view_users/', views.view_users, name='view_users'),
    path('delete_user/<int:pk>', views.delete_user_view, name='delete_user'),
    path('update_user/<int:pk>', views.update_user_view, name='update_user'),
    path('update_user_self/', views.update_user_self_view, name='update_user_self'),
    path('add_news/', views.add_news, name='add_news'),
    path('update_news/<int:news_id>/', views.update_news, name='update_news'),
    path('delete_news/<int:news_id>/', views.delete_news, name='delete_news'),
    path('change_password/', views.change_password, name='change_password'),
    path('graphs/', views.graphs, name='graphs'),
    path('chart_data/', views.chart_data, name='chart_data'),
    path('news/', views.view_news, name='view_news'),
    path('dogs/', views.view_dogs, name='view_dogs'),
    path('filter/', views.filter_dogs, name='filter_dogs'),
    path('export_dogs_json/', views.export_dogs_json, name='export_dogs_json'),
    path('get_filtered_dog_ids/', views.get_filtered_dog_ids, name='get_filtered_dog_ids'),
    path('export_dogs_excel/', views.export_dogs_excel, name='export_dogs_excel'),
    path('import_dogs_excel/', views.import_dogs_excel, name='import_dogs_excel'),
    path('import_dogs_json/', views.import_dogs_json, name='import_dogs_json'),

]
