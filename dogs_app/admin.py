from django.contrib import admin
from .models import Dog, Owner, Camera, Observes, Treatment, EntranceExamination, Kennel, DogPlacement, Observation, DogStance

# Register your models here.
admin.site.register((Dog, Camera, Owner, Observes, Treatment,
                     EntranceExamination, Kennel, DogPlacement,
                     Observation, DogStance))
