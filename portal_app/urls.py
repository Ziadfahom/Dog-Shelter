from django.urls import path, include
from django.views.generic import RedirectView

from . import views

app_name = 'portal_app'

urlpatterns = [
    path('', RedirectView.as_view(url='owners/', permanent=False), name='portal'),

    path('owners/', views.owner_list_portal, name='list-owners'),
    path('owners/add/', views.add_owner_portal, name='add-owner'),
    path('owners/delete/<int:pk>/', views.delete_owner_portal, name='delete-owner'),
    path('owners/edit/<int:pk>/', views.edit_owner_portal, name='edit-owner'),

    path('cameras/', views.camera_list_portal, name='list-cameras'),
    path('cameras/add/', views.add_camera_portal, name='add-camera'),
    path('cameras/delete/<int:pk>/', views.delete_camera_portal, name='delete-camera'),
    path('cameras/edit/<int:pk>/', views.edit_camera_portal, name='edit-camera'),

    path('kennels/', views.kennel_list_portal, name='list-kennels'),
    path('kennels/add/', views.add_kennel_portal, name='add-kennel'),
    path('kennels/delete/<int:pk>/', views.delete_kennel_portal, name='delete-kennel'),
    path('kennels/edit/<int:pk>/', views.edit_kennel_portal, name='edit-kennel'),

    path('treatments/', views.treatment_list_portal, name='list-treatments'),
    path('treatments/add/', views.add_treatment_portal, name='add-treatment'),
    path('treatments/delete/<int:pk>/', views.delete_treatment_portal, name='delete-treatment'),
    path('treatments/edit/<int:pk>/', views.edit_treatment_portal, name='edit-treatment'),

    path('examinations/', views.examination_list_portal, name='list-examinations'),
    path('examinations/add/', views.add_examination_portal, name='add-examination'),
    path('examinations/delete/<int:pk>/', views.delete_examination_portal, name='delete-examination'),
    path('examinations/edit/<int:pk>/', views.edit_examination_portal, name='edit-examination'),

    path('placements/', views.placement_list_portal, name='list-placements'),
    path('placements/add/', views.add_placement_portal, name='add-placement'),
    path('placements/delete/<int:pk>/', views.delete_placement_portal, name='delete-placement'),
    path('placements/edit/<int:pk>/', views.edit_placement_portal, name='edit-placement'),

    path('sessions/', views.observes_list_portal, name='list-observes'),
    path('sessions/add/', views.add_observes_portal, name='add-observes'),
    path('sessions/delete/<int:pk>/', views.delete_observes_portal, name='delete-observes'),
    path('sessions/edit/<int:pk>/', views.edit_observes_portal, name='edit-observes'),

    path('observations/', views.observations_list_portal, name='list-observations'),
    path('observations/add/', views.add_observation_portal, name='add-observation'),
    path('observations/delete/<int:pk>/', views.delete_observation_portal, name='delete-observation'),
    path('observations/edit/<int:pk>/', views.edit_observation_portal, name='edit-observation'),

    path('stances/', views.stances_list_portal, name='list-stances'),
    path('stances/add/', views.add_stance_portal, name='add-stance'),
    path('stances/delete/<int:pk>/', views.delete_stance_portal, name='delete-stance'),
    path('stances/edit/<int:pk>/', views.edit_stance_portal, name='edit-stance'),

]
