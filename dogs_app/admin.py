from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Dog, Owner, Camera, Observes, Treatment, EntranceExamination,\
    Kennel, DogPlacement, Observation, DogStance, Profile, News, Branch


# Define an inline admin descriptor for the Profile model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Register your models
admin.site.register((Dog, Camera, Owner, Observes, Treatment,
                     EntranceExamination, Kennel, DogPlacement,
                     Observation, DogStance, News, Branch))
