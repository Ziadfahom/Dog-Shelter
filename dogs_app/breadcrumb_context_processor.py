import re
from dogs_app.models import Observation, Observes


# Fetch the dog ID from the session ID
def get_dog_id_from_session_id(session_id):
    try:
        observes_obj = Observes.objects.get(id=session_id)
        dog_id = observes_obj.dog.dogID
        return dog_id
    except (Observation.DoesNotExist, AttributeError):
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
        breadcrumbs.append({"name": "Dog", "url": f"/dog/{dog_id}"})

    if session_id:
        session_id = session_id.group(1)
        dog_id = get_dog_id_from_session_id(session_id)
        if dog_id:
            breadcrumbs.append({"name": "Dogs", "url": "/dogs/"})
            breadcrumbs.append({"name": "Dog", "url": f"/dog/{dog_id}"})
            breadcrumbs.append({"name": "Observations", "url": f"/observations/{session_id}"})

    if 'details/' in url_path:
        breadcrumbs.append({"name": "Details", "url": f"{url_path}"})
    if 'add_dog/' in url_path:
        breadcrumbs.append({"name": "New Dog", "url": f"{url_path}"})
    if 'graphs/' in url_path:
        breadcrumbs.append({"name": "Graphs", "url": f"{url_path}"})
    if 'view_users/' in url_path:
        breadcrumbs.append({"name": "View Users", "url": f"{url_path}"})
    if 'add_news/' in url_path:
        breadcrumbs.append({"name": "Add News", "url": f"{url_path}"})
    if 'update_user_self/' in url_path:
        breadcrumbs.append({"name": "Manage Details", "url": f"{url_path}"})
    if 'change_password/' in url_path:
        breadcrumbs.append({"name": "Change Password", "url": f"{url_path}"})

    # Add more conditions later

    return {'breadcrumbs': breadcrumbs}
