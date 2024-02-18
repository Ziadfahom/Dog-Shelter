import re

from django.contrib.auth.models import User

from dogs_app.models import Observation, Observes, Dog


# Fetch the dog ID from the session ID
def get_dog_id_from_session_id(session_id):
    try:
        observes_obj = Observes.objects.get(id=session_id)
        dog_id = observes_obj.dog.dogID
        return dog_id
    except (Observation.DoesNotExist, AttributeError):
        return None

# Fetch the dog's name from the dog ID
def get_dog_name_from_dog_id(dog_id):
    try:
        dog_name = Dog.objects.get(dogID=dog_id).dogName
        return dog_name
    except (Dog.DoesNotExist, AttributeError):
        return None

def get_user_name_from_user_id(user_id):
    try:
        user_name = User.objects.get(id=user_id).username
        return user_name
    except (User.DoesNotExist, AttributeError):
        return None


def breadcrumb_processor(request):
    if not request.user.is_authenticated:
        return {'breadcrumbs': None}

    url_path = request.path_info
    breadcrumbs = [{"name": "Home", "url": "/"}]

    # Match and capture IDs from the URL
    session_id = re.search(r'/observations/(\d+)', url_path)

    if 'dogs/' in url_path:
        breadcrumbs.append({"name": "Dogs", "url": "/dogs/"})

    if re.search(r'/dog/(\d+)', url_path):
        dog_id = re.search(r'/dog/(\d+)', url_path).group(1)
        breadcrumbs.append({"name": "Dogs", "url": "/dogs/"})
        breadcrumbs.append({"name": get_dog_name_from_dog_id(dog_id), "url": f"/dog/{dog_id}"})

    if session_id:
        session_id = session_id.group(1)
        dog_id = get_dog_id_from_session_id(session_id)
        if dog_id:
            breadcrumbs.append({"name": "Dogs", "url": "/dogs/"})
            breadcrumbs.append({"name": get_dog_name_from_dog_id(dog_id), "url": f"/dog/{dog_id}"})
            breadcrumbs.append({"name": "Observations", "url": f"/observations/{session_id}"})

    if 'details/' in url_path:
        breadcrumbs.append({"name": "Details", "url": f"{url_path}"})
    if '/news/' in url_path:
        breadcrumbs.append({"name": "News", "url": f"{url_path}"})
    if 'add_dog/' in url_path:
        breadcrumbs.append({"name": "Dogs", "url": "/dogs/"})
        breadcrumbs.append({"name": "Add Dog", "url": f"{url_path}"})
    if 'update_dog/' in url_path:
        breadcrumbs.append({"name": "Dogs", "url": "/dogs/"})
        dog_id = re.search(r'/update_dog/(\d+)', url_path).group(1)
        breadcrumbs.append({"name": get_dog_name_from_dog_id(dog_id), "url": f"/dog/{dog_id}"})
        breadcrumbs.append({"name": "Update Dog", "url": f"{url_path}"})
    if 'delete_dog/' in url_path:
        breadcrumbs.append({"name": "Dogs", "url": "/dogs/"})
        dog_id = re.search(r'/delete_dog/(\d+)', url_path).group(1)
        breadcrumbs.append({"name": get_dog_name_from_dog_id(dog_id), "url": f"/dog/{dog_id}"})
        breadcrumbs.append({"name": "Delete Dog", "url": f"{url_path}"})
    if 'graphs/' in url_path:
        breadcrumbs.append({"name": "Graphs", "url": f"{url_path}"})
    if 'view_users/' in url_path:
        breadcrumbs.append({"name": "View Users", "url": f"{url_path}"})
    if 'add_news/' in url_path:
        breadcrumbs.append({"name": "News", "url": "/news/"})
        breadcrumbs.append({"name": "Add News", "url": f"{url_path}"})
    if 'update_news/' in url_path:
        breadcrumbs.append({"name": "News", "url": "/news/"})
        breadcrumbs.append({"name": "Update News", "url": f"{url_path}"})
    if 'delete_news/' in url_path:
        breadcrumbs.append({"name": "News", "url": "/news/"})
        breadcrumbs.append({"name": "Delete News", "url": f"{url_path}"})
    if 'update_user_self/' in url_path:
        breadcrumbs.append({"name": "Manage Details", "url": f"{url_path}"})
    if 'change_password/' in url_path:
        breadcrumbs.append({"name": "Change Password", "url": f"{url_path}"})
    if 'update_user/' in url_path:
        breadcrumbs.append({"name": "View Users", "url": "/view_users/"})
        user_id = re.search(r'/update_user/(\d+)', url_path).group(1)
        user_name = get_user_name_from_user_id(user_id)
        breadcrumbs.append({"name": f"Edit {user_name}", "url": f"{url_path}"})
    if 'delete_user/' in url_path:
        breadcrumbs.append({"name": "View Users", "url": "/view_users/"})
        user_id = re.search(r'/delete_user/(\d+)', url_path).group(1)
        user_name = get_user_name_from_user_id(user_id)
        breadcrumbs.append({"name": f"{user_name}", "url": f"/update_user/{user_id}"})
        breadcrumbs.append({"name": "Delete User", "url": f"{url_path}"})

    # Add more conditions later

    return {'breadcrumbs': breadcrumbs}
