from django.db import migrations
from django.contrib.auth.models import Group, Permission


# This function is the main part of our migration
def create_group(apps, schema_editor):
    # We create (or get if it already exists) the 'Viewer' group
    Group.objects.get_or_create(name='Viewer')

    # We fetch the 'Viewer' group
    viewer_group = Group.objects.get(name='Viewer')

    # We fetch all the 'view' permissions for our 'dogs_app' app
    viewer_permissions = Permission.objects.filter(
        content_type__app_label='dogs_app',
        codename__startswith='view_'
    )

    # We set the 'view' permissions for the 'Viewer' group
    viewer_group.permissions.set(viewer_permissions)

    # We create (or get if it already exists) the 'Vet' group
    Group.objects.get_or_create(name='Vet')

    # We fetch the 'Vet' group
    vet_group = Group.objects.get(name='Vet')

    # We fetch the required permissions for the 'Vet' group for our 'dogs_app' app
    vet_permissions = Permission.objects.filter(
        content_type__app_label='dogs_app',
        codename__in=[
            'add_profile', 'change_profile', 'delete_profile', 'view_profile',
            'add_owner', 'change_owner', 'delete_owner', 'view_owner',
            'add_dog', 'change_dog', 'delete_dog', 'view_dog',
            'add_camera', 'change_camera', 'delete_camera', 'view_camera',
            'add_observes', 'change_observes', 'delete_observes', 'view_observes',
            'add_treatment', 'change_treatment', 'delete_treatment', 'view_treatment',
            'add_entranceexamination', 'change_entranceexamination', 'delete_entranceexamination', 'view_entranceexamination',
            'add_kennel', 'change_kennel', 'delete_kennel', 'view_kennel',
            'add_dogplacement', 'change_dogplacement', 'delete_dogplacement', 'view_dogplacement',
            'add_observation', 'change_observation', 'delete_observation', 'view_observation',
            'add_dogstance', 'change_dogstance', 'delete_dogstance', 'view_dogstance',
            'add_news', 'change_news', 'delete_news', 'view_news'
        ]
    )

    # We set the fetched permissions for the 'Vet' group
    vet_group.permissions.set(vet_permissions)


# This class is required for each migration file
class Migration(migrations.Migration):

    # We set the migration that this one depends on
    dependencies = [
        ('dogs_app', '0028_rename_ownerserialnum_dog_owner_and_more'),
    ]

    # We set the operations to be run for this migration
    operations = [
        # Run the 'create_group' function we defined above
        migrations.RunPython(create_group),
    ]
