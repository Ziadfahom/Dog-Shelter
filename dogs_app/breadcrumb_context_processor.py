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
    if '/poll/' in url_path:
        breadcrumbs.append({"name": "Poll", "url": f"{url_path}"})
    if 'add_poll/' in url_path:
        breadcrumbs.append({"name": "Poll", "url": "/poll/"})
        breadcrumbs.append({"name": "Add Poll", "url": f"{url_path}"})
    if 'update_poll/' in url_path:
        breadcrumbs.append({"name": "Poll", "url": "/poll/"})
        breadcrumbs.append({"name": "Update Poll", "url": f"{url_path}"})
    if 'delete_poll/' in url_path:
        breadcrumbs.append({"name": "Poll", "url": "/poll/"})
        breadcrumbs.append({"name": "Delete Poll", "url": f"{url_path}"})

    # Portal breadcrumbs
    if 'portal/' in url_path:
        breadcrumbs.append({"name": "Portal", "url": "/portal/"})
        if 'kennels/' in url_path:
            breadcrumbs.append({"name": "Kennels", "url": "/portal/kennels/"})
            if 'add/' in url_path:
                breadcrumbs.append({"name": "Add Kennel", "url": f"{url_path}"})
            elif 'edit/' in url_path:
                breadcrumbs.append({"name": "Edit Kennel", "url": f"{url_path}"})
        elif 'placements/' in url_path:
            breadcrumbs.append({"name": "Dog Placements", "url": "/portal/placements/"})
            if 'add/' in url_path:
                breadcrumbs.append({"name": "Add Placement", "url": f"{url_path}"})
            elif 'edit/' in url_path:
                breadcrumbs.append({"name": "Edit Placement", "url": f"{url_path}"})
        elif 'cameras/' in url_path:
            breadcrumbs.append({"name": "Cameras", "url": "/portal/cameras/"})
            if 'add/' in url_path:
                breadcrumbs.append({"name": "Add Camera", "url": f"{url_path}"})
            elif 'edit/' in url_path:
                breadcrumbs.append({"name": "Edit Camera", "url": f"{url_path}"})
        elif 'sessions/' in url_path:
            breadcrumbs.append({"name": "Camera Sessions", "url": "/portal/sessions/"})
            if 'add/' in url_path:
                breadcrumbs.append({"name": "Add Session", "url": f"{url_path}"})
            elif 'edit/' in url_path:
                breadcrumbs.append({"name": "Edit Session", "url": f"{url_path}"})
        elif 'observations/' in url_path:
            breadcrumbs.append({"name": "Observations", "url": "/portal/observations/"})
            if 'add/' in url_path:
                breadcrumbs.append({"name": "Add Observation", "url": f"{url_path}"})
            elif 'edit/' in url_path:
                breadcrumbs.append({"name": "Edit Observation", "url": f"{url_path}"})
        elif 'stances/' in url_path:
            breadcrumbs.append({"name": "Stances", "url": "/portal/stances/"})
            if 'add/' in url_path:
                breadcrumbs.append({"name": "Add Stance", "url": f"{url_path}"})
            elif 'edit/' in url_path:
                breadcrumbs.append({"name": "Edit Stance", "url": f"{url_path}"})
        elif 'treatments/' in url_path:
            breadcrumbs.append({"name": "Treatments", "url": "/portal/treatments/"})
            if 'add/' in url_path:
                breadcrumbs.append({"name": "Add Treatment", "url": f"{url_path}"})
            elif 'edit/' in url_path:
                breadcrumbs.append({"name": "Edit Treatment", "url": f"{url_path}"})
        elif 'examinations/' in url_path:
            breadcrumbs.append({"name": "Examinations", "url": "/portal/examinations/"})
            if 'add/' in url_path:
                breadcrumbs.append({"name": "Add Examination", "url": f"{url_path}"})
            elif 'edit/' in url_path:
                breadcrumbs.append({"name": "Edit Examination", "url": f"{url_path}"})
        elif 'owners/' in url_path:
            breadcrumbs.append({"name": "Dog Owners", "url": "/portal/owners/"})
            if 'add/' in url_path:
                breadcrumbs.append({"name": "Add Owner", "url": f"{url_path}"})
            elif 'edit/' in url_path:
                breadcrumbs.append({"name": "Edit Owner", "url": f"{url_path}"})

    # Add more conditions later

    return {'breadcrumbs': breadcrumbs}
