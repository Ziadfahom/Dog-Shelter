from django import template
from django.contrib.auth.models import Group

# Used to determine (in HTML files) whether the User
# Has the permission to access a page

# -Admins have all privileges (Including viewing Users)
# -Vets have View\Update\Delete\Add privileges for all models
# -Regulars have only View privileges for all models

register = template.Library()


@register.filter(name='has_group')
# Takes an input name of a User group
def has_group(user, group_name):
    # Disregard case sensitivity and pluralities ('Vets'='Vet', 'Regulars'='Regular')
    group_name = group_name.title()
    if group_name.endswith('s'):
        group_name = group_name[:-1]

    # Always return True if User is Admin (has all privileges)
    if user.is_superuser:
        return True
    # Vet also has Regular permissions
    elif group_name == "Regular" and user.groups.filter(name="Vet").exists():
        return True
    # Return True if User is in the queried group
    elif group_name in ["Regular", "Vet"] and user.groups.filter(name=group_name).exists():
        return True
    # Otherwise return False
    else:
        return False


