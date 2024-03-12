from django import template
from django.contrib.auth.models import Group

# Used to determine (in HTML files) whether the User
# Has the permission to access a page

# -Admins have all privileges (Including viewing Users)
# -Vets have View\Update\Delete\Add privileges for all models
# -Viewers have only View privileges for all models

register = template.Library()


# Returns True if User has the queried group's privileges and ABOVE
@register.filter(name='has_group')
# Takes an input name of a User group
def has_group(user, group_name):
    # Disregard case sensitivity and pluralities ('Vets'='Vet', 'Viewers'='Viewer')
    group_name = group_name.title()
    if group_name.endswith('s'):
        group_name = group_name[:-1]

    # Always return True if User is Admin (has all privileges)
    if user.is_superuser:
        return True
    # Vet also has Viewer permissions
    elif group_name == "Viewer" and user.groups.filter(name="Vet").exists():
        return True
    # Return True if User is in the queried group
    elif group_name in ["Viewer", "Vet"] and user.groups.filter(name=group_name).exists():
        return True
    # Otherwise return False
    else:
        return False


# Returns True if User has the queried group's privileges and ONLY THAT
@register.filter(name='has_only_group')
# Takes an input name of a User group
def has_only_group(user, group_name):
    # Disregard case sensitivity and pluralities ('Vets'='Vet', 'Viewers'='Viewer')
    group_name = group_name.title()
    if group_name.endswith('s'):
        group_name = group_name[:-1]

    # Return True if query is for Admin and User is Admin
    if group_name == "Admin" and user.is_superuser:
        return True
    # Return True if query is for Viewer and User is Viewer (Regular Registered User)
    elif group_name == "Viewer" and user.groups.filter(name="Viewer").exists():
        return True
    # Return True if query is for Vet and User is Vet
    elif group_name == "Vet" and user.groups.filter(name="Vet").exists():
        return True
    # Otherwise return False
    else:
        return False

