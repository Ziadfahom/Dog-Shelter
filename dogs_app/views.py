from django.db.models import Value
from django.db.models.functions import Concat, Trim
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse
from .filters import DogFilter
from .forms import SignUpForm, AddDogForm, UpdateUserForm, ProfileUpdateForm
from .models import *
from django.conf import settings
import os
from django.core import serializers
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from datetime import date, timedelta

import logging
from pytz import timezone


# Location of the default User profile picture if they don't have a picture
DEFAULT_IMAGE_SOURCE = '/profile_pictures/default.jpg'

# CONSTANTS
# Number of Dogs/Users/Table Entries we want displayed in a single page across all Paginators
ENTRIES_PER_PAGE = 10


# Main Page view for displaying either dog records if  user is logged in,
# or a login page if user is logged out
def home_view(request):
    # Get all the dog records in the database
    all_dogs = Dog.objects.all().order_by('-dateOfArrival')

    # Get the total number of dogs
    total_dogs = Dog.objects.count()

    # Get the number of dogs that have received toy treatments
    toy_treatment_dogs = Dog.objects.filter(observers__observation__isKong='Y').distinct().count()

    # Get all the website News to display them in descending order
    news_items = News.objects.all().order_by('-created_at')

    # Checking if user is logged in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        users = get_user_model()

        # Check if username exists
        if users.objects.filter(username=username).exists():

            try:
                # Authenticate
                user = authenticate(request, username=username, password=password)

                # If correct username+password combination
                if user is not None:
                    login(request, user=user)
                    messages.success(request, message='You have successfully logged in!')
                    return redirect('dogs_app:home')
                else:
                    # Username exists but password was incorrect
                    messages.error(request, message='The password is incorrect. Please try again...')
                    return redirect('dogs_app:home')
            except Exception as e:
                messages.error(request, message=f'An error occurred during login: {e}')
                return redirect('dogs_app:home')
        else:
            # Username does not exist
            messages.error(request, message='The username does not exist. Please try again...')
            return redirect('dogs_app:home')
    else:
        # User is not logged in, redirect them to login page (home)

        # Attach user roles to the home page display
        role = get_user_role(request.user) if request.user.is_authenticated else ""

        context = {
            'dogs': all_dogs,
            'total_dogs': total_dogs,
            'toy_treatment_dogs': toy_treatment_dogs,
            'news_items': news_items,
            'role': role
        }
        return render(request, 'home.html', context=context)


# Logout Users view for displaying a user-logout option if they're already logged in
def logout_user_view(request):
    logout(request)
    messages.success(request, message='You have been logged out..')
    return redirect('dogs_app:home')


# User Registration view for new users
def register_user_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            # Add User to the Viewers Group
            viewers_group = Group.objects.get(name="Viewer")
            user.groups.add(viewers_group)

            # Check if a profile already exists for the user
            profile = Profile.objects.filter(user=user).first()
            if not profile:
                profile = Profile.objects.create(user=user)

            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            profile_form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)

            messages.success(request, f"Welcome, {username} and thank you for signing up! "
                                      "You're now a member of our Dogs Shelter community.")
            return redirect('dogs_app:home')
    else:
        form = SignUpForm()
        profile_form = ProfileUpdateForm()

    return render(request, 'register.html', {'form': form, 'profile_form': profile_form})


# User password reset view
def change_password(request):
    # User trying to submit the form
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        # The details are valid
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important! Re-logins the user after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dogs_app:home')
        # Issues with the filled details
        else:
            messages.error(request, 'Please correct the error below')
    # User is trying to open the change password page
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form,
    })


# View for adding website news to the homepage
# Only logged-in admins permitted
@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_news(request):
    if request.method == 'POST':
        news_title = request.POST.get('title')
        news_content = request.POST.get('content')
        News.objects.create(title=news_title, content=news_content)
        return redirect('dogs_app:home')
    return render(request, 'add_news.html')


# Dog record page, displays the details for a single dog
# Takes in the dog's PK
def dog_record_view(request, pk):
    # Check if the user is logged in
    if request.user.is_authenticated:
        # Look up and save the dog's record and all relevant data of that dog
        dog_record = Dog.objects.select_related('owner').prefetch_related(
            'treatment_set',
            'entranceexamination_set',
            'observers__observation_set',
            'dogplacement_set__kennel',  # For Cameras related to DogPlacement's kennel
            'observers__observation_set__dogstance_set',  # For DogStances related to Observations
        ).get(dogID=pk)

        context = {
            'dog_record': dog_record,
            'treatments': Treatment.objects.filter(dog=dog_record).order_by('-treatmentDate'),
            'examinations': EntranceExamination.objects.filter(dog=dog_record).order_by('-examinationDate'),
            'observations': Observation.objects.filter(observes__dog=dog_record).order_by('-obsDateTime'),
            'placements': DogPlacement.objects.filter(dog=dog_record).order_by('-entranceDate'),
        }

        return render(request, 'dog_record.html', context=context)

    # User is NOT logged in --> send them to login page
    else:
        messages.error(request, message='You Must Be Logged In To View That Page...')
        return redirect('dogs_app:home')


# Deleting a dog record
def delete_dog_view(request, pk):
    # Check if the user is logged in
    if request.user.is_authenticated:
        # Check if the user has the right permissions
        if not request.user.has_perm('dogs_app.delete_dog'):
            raise PermissionDenied
        # Grab the dog to delete
        delete_dog = get_object_or_404(Dog, dogID=pk)

        if request.method == 'POST':
            dog_name = delete_dog.dogName
            delete_dog.delete()
            messages.success(request, f'{dog_name} Has Been Deleted Successfully...')
            return redirect('dogs_app:view_dogs')
        # User clicked "Delete" button to confirm deletion
        return render(request, 'delete_dog.html', {'dog': delete_dog})
    # User not logged in, must login first
    else:
        messages.error(request, 'You must be logged in to do that...')
        return redirect('dogs_app:home')


def add_dog_view(request):
    # Check if user is logged in
    if request.user.is_authenticated:
        # Check if the user has the right permissions
        if not request.user.has_perm('dogs_app.add_dog'):
            raise PermissionDenied

        # If form is submitted (i.e., User has filled the form)
        if request.method == 'POST':
            # Initialize the form
            form = AddDogForm(request.POST, request.FILES)
            # Validate the form inputs
            if form.is_valid():
                # Save new dog details to database + display success message
                form.save()
                messages.success(request, f"{form.cleaned_data['dogName']} Has Been Added Successfully...")
                return redirect('dogs_app:view_dogs')
            # If form is not valid, render errors
            else:
                return render(request, 'add_dog.html', {"form": form})
        # If request is not POST (i.e., GET), just render the form
        else:
            form = AddDogForm()
            return render(request, 'add_dog.html', {"form": form})
    # If user is not logged in/authenticated, show an error message and redirect to home.
    else:
        messages.error(request, "You Must Be Logged In To Add New Dogs...")
        return redirect('dogs_app:home')


# Updating a Dog record
def update_dog_view(request, pk):
    # Check if user is logged in
    if request.user.is_authenticated:
        # Check if the user has the right permissions to edit dogs
        if not request.user.has_perm('dogs_app.change_dog'):
            raise PermissionDenied

        # Grab the Dog record
        current_dog = Dog.objects.get(dogID=pk)
        form = AddDogForm(request.POST or None, request.FILES or None, instance=current_dog)

        # Check if the "deleteImage" button was clicked
        if 'deleteImage' in request.POST:
            # Delete the dog's image if it is not the default images
            if current_dog.dogImage and current_dog.dogImage.name:
                os.remove(os.path.join(settings.MEDIA_ROOT, current_dog.dogImage.name))

            current_dog.dogImage = None
            current_dog.save()
            messages.success(request, f"{current_dog.dogName}'s Picture Has Been Removed Successfully!")
            # Refresh the current page
            return HttpResponseRedirect(request.path_info)

        # Check if form is submitted
        if form.is_valid():
            form.save()
            messages.success(request, f"{current_dog.dogName}'s Details Have Been Updated Successfully!")
            return redirect('dogs_app:dog_record', pk=current_dog.dogID)
        return render(request, 'update_dog.html', {'form': form, 'current_dogID': current_dog.dogID})

    # User is not logged in, redirect them to login
    else:
        messages.error(request, "You must be logged in to do that...")
        return redirect('dogs_app:home')


# Display all users for the admins only in view_users.html
# Check user is logged in
@login_required
# Check user is Admin
@user_passes_test(lambda u: u.is_superuser)
def view_users(request):
    # Retrieve sorting criteria from request
    order_by = request.GET.get('order_by', 'username') # Default sort field
    direction = request.GET.get('direction', 'asc') # Default sort direction

    # Retrieve all the users in the system, prefetch their groups, and select their profiles
    users = User.objects.all().prefetch_related('groups').select_related('profile')

    # Use a Role Filter for filtering Users based on their Role
    role_filter = request.GET.get('role', 'all')

    page = request.GET.get('page')

    # Apply role filter
    if role_filter and role_filter != "all":
        if role_filter == "Admin":
            users = users.filter(is_superuser=True)
        else:
            users = users.filter(groups__name=role_filter)

    # Search Query
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(Q(username__icontains=search_query) | Q(email__icontains=search_query) | Q(
            first_name__icontains=search_query) | Q(last_name__icontains=search_query))

    # Apply sorting
    if order_by == 'full_name':
        users = users.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
    elif order_by in ['phone_number', 'address']:
        order_by = 'profile__' + order_by

    if order_by == 'role':
        users_page, paginator = sort_users_by_role(users, direction, page)
    else:
        if direction == 'desc':
            sort_order = '-' + order_by
        else:
            sort_order = order_by
        users = users.order_by(sort_order)

        # Create a Paginator object with the users and the number of users per page
        paginator = Paginator(users, ENTRIES_PER_PAGE, allow_empty_first_page=True)

        # Get the current page number from the request's GET parameters
        page = request.GET.get('page')

        # Get the Page object for the current page
        users_page = paginator.get_page(page)

    # Calculate pagination range
    pagination_start = max(users_page.number - 3, 1)
    pagination_end = min(users_page.number + 3, paginator.num_pages)

    # Fetch each user's Status (E.g: "Admin", "Vet" or "Viewer")
    for user in users_page:
        user.role = get_user_role(user)

    context = {
        'users': users_page,
        'pagination_start': pagination_start,
        'pagination_end': pagination_end,
        'role_filter': role_filter,
        'order_by': order_by,
        'direction': direction,
        'search_query': search_query,
    }

    # pass all users on to viewers_users.html
    return render(request, 'view_users.html', context=context)


# Takes in a User, returns their ranking.
# Used in view_users and update_user to determine User Status
def get_user_role(user):
    if user.is_superuser:
        return "Admin"
    elif user.groups.filter(name="Vet").exists():
        return "Vet"
    elif user.groups.filter(name="Viewer").exists():
        return "Viewer"
    else:
        return ""


# Custom sorting function for view_users
# Custom sorting function for view_users
def sort_users_by_role(users, direction='asc', page_number=1):
    # Mapping roles to sort order
    ROLE_SORT_ORDER = {'Admin': 0, 'Vet': 1, 'Viewer': 2}

    # Use the existing get_user_role function to extract the role's sort order
    def get_role_order(user):
        role = get_user_role(user)
        return ROLE_SORT_ORDER.get(role, -1)

    # Sort users based on the role order and username
    sorted_users = sorted(users, key=lambda user: (get_role_order(user), user.username))

    # If the direction is descending, reverse the sorted list
    if direction == 'desc':
        sorted_users.reverse()

    # Create a Paginator object with the sorted_users and the number of users per page
    paginator = Paginator(sorted_users, ENTRIES_PER_PAGE, allow_empty_first_page=True)

    # Get the Page object for the current page
    users_page = paginator.get_page(page_number)

    return users_page, paginator


# Only logged-in users permitted
@login_required
# Check user is Admin
@user_passes_test(lambda u: u.is_superuser)
# Delete a user in the Admin user-view page
def delete_user_view(request, pk):
    # Check if the user is logged in
    if request.user.is_authenticated:
        # Check if the user has the right permissions
        if not request.user.has_perm('dogs_app.delete_user'):
            raise PermissionDenied
        # Grab the user to delete
        delete_user = get_object_or_404(User, pk=pk)
        # User trying to display the delete page
        if request.method == 'POST':
            user_name = delete_user.username
            delete_user.delete()
            messages.success(request, f'{user_name} Has Been Deleted Successfully...')
            return redirect('dogs_app:view_users')
        # User clicked "Delete" button to confirm deletion
        return render(request, 'delete_user.html', {'delete_user': delete_user})
    # User not logged in, must login first
    else:
        messages.error(request, message='You must be logged in to do that...')
        return redirect('dogs_app:home')


# View for updating user details
# Check user is Admin
@user_passes_test(lambda u: u.is_superuser)
def update_user_view(request, pk):
    # Check if user is logged in
    if request.user.is_authenticated:
        user_to_update = User.objects.get(pk=pk)
        initial = {'role': get_user_role(user_to_update)}
        # Main User Form
        user_form = UpdateUserForm(request.POST or None,
                                   instance=user_to_update,
                                   initial=initial,
                                   request_user=request.user)
        # Addition User Details Form (phone, address, image)
        profile_form = ProfileUpdateForm(request.POST or None,
                                         request.FILES or None,
                                         instance=user_to_update.profile)

        # Check if the "deleteImage" button was clicked
        if 'deleteImage' in request.POST:
            # Delete the user's profile image if it is not the default image
            if user_to_update.profile.image and 'default.jpg' not in user_to_update.profile.image.name:
                os.remove(os.path.join(settings.MEDIA_ROOT, user_to_update.profile.image.name))

            user_to_update.profile.image = DEFAULT_IMAGE_SOURCE
            user_to_update.profile.save()
            messages.success(request, f"{user_to_update.first_name} {user_to_update.last_name}'s"
                                      f" Picture Has Been Removed Successfully!")
            # Refresh the current page
            return HttpResponseRedirect(request.path_info)

        if user_form.is_valid() and profile_form.is_valid():
            # Save form without committing (we'll modify the user before saving)
            user = user_form.save(commit=False)
            role = user_form.cleaned_data['role']
            # If the group name is not empty
            if role:
                # If group name is Admin, update is_superuser status and clear other groups
                if role == 'Admin':
                    user.is_superuser = True
                    user.is_staff = True
                    user_to_update.groups.clear()
                else:
                    # For other groups, get the chosen group
                    chosen_group = Group.objects.get(name=role)
                    # Remove the user from all the other groups
                    user_to_update.groups.clear()
                    # Add the user to the chosen group
                    user_to_update.groups.add(chosen_group)
                    # Update user's is_superuser status
                    user.is_superuser = False
                    user.is_staff = False

            # Now commit the save
            user.save()
            profile_form.save()
            messages.success(request, f"{user_to_update.first_name} {user_to_update.last_name}'s Details"
                                      f" Have Been Updated Successfully!")
            return redirect('dogs_app:view_users')
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'user_to_update': user_to_update,
            'profile': user_to_update.profile
        }
        return render(request, 'update_user.html', context=context)
    # User is not logged in, redirect them to login
    else:
        messages.error(request, "You must be logged in to do that...")
        return redirect('dogs_app:home')


# User updating their own details view
# Only logged-in users permitted
@login_required
def update_user_self_view(request):
    if request.user.is_authenticated:
        user_to_update = User.objects.get(pk=request.user.pk)
        initial = {'role': get_user_role(user_to_update)}
        # Main User Form
        user_form = UpdateUserForm(request.POST or None,
                                   instance=user_to_update,
                                   initial=initial,
                                   request_user=user_to_update)

        profile_to_update = user_to_update.profile
        profile_form = ProfileUpdateForm(request.POST or None,
                                         request.FILES or None,
                                         instance=user_to_update.profile)
        if request.method == 'POST':
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save(commit=False)
                # Ensure non-admin users can't change their own roles
                if not request.user.is_superuser and 'role' in user_form.changed_data:
                    messages.error(request, "You are not allowed to change your role.")
                    return render(request, 'update_user.html', {
                        'user_form': user_form,
                        'profile_form': profile_form,
                        'profile': profile_to_update,
                    })

                # Check if the delete image button was clicked
                if 'deleteImage' in request.POST:
                    # Delete the user's profile image if it is not the default image
                    if profile_to_update.image and 'default.jpg' not in profile_to_update.image.name:
                        os.remove(os.path.join(settings.MEDIA_ROOT, profile_to_update.image.name))

                    profile_to_update.image = DEFAULT_IMAGE_SOURCE
                    profile_to_update.save()

                    messages.success(request, "Your Picture Has Been Removed Successfully!")
                    # Refresh the current page
                    return HttpResponseRedirect(request.path_info)

                profile_form.save()
                user.save()

                messages.success(request, f"Your Details Have Been Updated Successfully!")
                return redirect('dogs_app:update_user_self')
            else:
                return render(request, 'update_user.html', {
                    'user_form': user_form,
                    'profile_form': profile_form,
                    'profile': profile_to_update,
                })
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form,
                'profile_to_update': profile_to_update,
                'user_to_update': user_to_update
            }
            return render(request, 'update_user.html', context)
    else:
        messages.error(request, "You must be logged in to do that...")
        return redirect('dogs_app:home')


# Page for editing the news from the homepage. Only visible to Admins
@user_passes_test(lambda u: u.is_superuser)
def update_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    if request.method == 'POST':
        news.title = request.POST['title']
        news.content = request.POST['content']
        news.save()
        messages.success(request, f"News Story: '{request.POST['title']}' has been successfully edited...")
        return redirect('dogs_app:home')
    return render(request, 'update_news.html', {'news': news})


# View for deleting a News story from the homepage. Only available to Admins
@user_passes_test(lambda u: u.is_superuser)
def delete_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    if request.method == 'POST':
        news_title = news.title
        news.delete()
        messages.success(request, f"News Story: '{news_title}' has been successfully deleted...")
        return redirect('dogs_app:home')
    return render(request, 'delete_news.html', {'news': news})


# View for the Dynamic Graphs page
def chart_data(request):
    #DELETE#
    logger = logging.getLogger(__name__)

    from datetime import datetime, timedelta

    # Debugging code
    obs_with_kong = Observation.objects.filter(isKong='Y', obsDateTime__isnull=False)
    obs_with_kong_dates = [{'date': obs.obsDateTime.date()} for obs in obs_with_kong]
    logger.info(f"1) obs_with_kong_dates: {obs_with_kong_dates[:10]}")

    obs_without_kong = Observation.objects.filter(isKong='N', obsDateTime__isnull=False)
    obs_without_kong_dates = [{'date': obs.obsDateTime.date()} for obs in obs_without_kong]
    logger.info(f"2) obs_without_kong_dates: {obs_without_kong_dates[:10]}")

    # Now we manually aggregate and sum the session duration in Python
    obs_with_kong_grouped = {}
    for obs in obs_with_kong:
        date = obs.obsDateTime.date()
        if date not in obs_with_kong_grouped:
            obs_with_kong_grouped[date] = 0
        obs_with_kong_grouped[date] += obs.sessionDurationInMins

    obs_without_kong_grouped = {}
    for obs in obs_without_kong:
        date = obs.obsDateTime.date()

        if date not in obs_without_kong_grouped:
            obs_without_kong_grouped[date] = 0
        obs_without_kong_grouped[date] += obs.sessionDurationInMins

    logger.info(f"3) With kong data: {obs_with_kong_grouped}")
    logger.info(f"4) Without kong data: {obs_without_kong_grouped}")

    # Get all the Dogs that have received a Kong Toy
    dogs_with_kong = Dog.objects.filter(kongDateAdded__isnull=False)

    # Get all Observations with and without a Kong Toy
    obs_with_kong = Observation.objects.filter(isKong='Y', obsDateTime__isnull=False)
    obs_without_kong = Observation.objects.filter(isKong='N', obsDateTime__isnull=False)

    # Getting breeds and their counts
    dog_breeds = Dog.objects.values('breed').annotate(total=Count('breed')).order_by('-total')

    # Count of DogStances with and without kong toy
    stances_with_kong = DogStance.objects.filter(observation__in=obs_with_kong).values('dogStance').annotate(
        total=models.Count('observation'))
    stances_without_kong = DogStance.objects.filter(observation__in=obs_without_kong).values('dogStance').annotate(
        total=models.Count('observation'))

    # Make obsDateTime timezone-aware
    filtered_obs_with_kong = [{'date': k, 'total': v} for k, v in obs_with_kong_grouped.items()]
    filtered_obs_without_kong = [{'date': k, 'total': v} for k, v in obs_without_kong_grouped.items()]

    # Format dates for JavaScript
    jsl_tz = timezone('Asia/Jerusalem')

    for obs in filtered_obs_with_kong:
        if obs['date']:
            obs['date'] = obs['date'].strftime("%m/%d/%Y")

    for obs in filtered_obs_without_kong:
        if obs['date']:
            obs['date'] = obs['date'].strftime("%m/%d/%Y")

    #DELETE#
    # Log the data
    logger.info(f"5) With kong data: {list(filtered_obs_with_kong)}")
    logger.info(f"6) Without kong data: {list(filtered_obs_without_kong)}")

    # Preparing data to be used in the frontend
    data = {
        'dogs_with_kong': serializers.serialize('json', dogs_with_kong),
        'stances_with_kong': list(stances_with_kong),
        'stances_without_kong': list(stances_without_kong),
        'dog_breeds': list(dog_breeds),
        'durations_with_kong': list(filtered_obs_with_kong),
        'durations_without_kong': list(filtered_obs_without_kong),
    }

    return JsonResponse(data)


def graphs(request):
    return render(request, 'graphs.html')


# Helper function to filter out unwanted attributes.
def exclude_unwanted(attribute):
    exclusions = ["Unspecified", " ", "-", ""]
    return Q(**{f"{attribute}__isnull": True}) | Q(**{f"{attribute}__in": exclusions})


# Fetch unique values for a given dog attribute.
def get_unique_values(attribute):
    return Dog.objects.exclude(exclude_unwanted(attribute)).values(attribute).distinct().order_by(attribute)


# Fetch unique owner values.
def get_unique_owners():
    return Dog.objects.exclude(owner__isnull=True).values('owner__firstName',
                                                          'owner__lastName',
                                                          'owner').distinct().order_by('owner__firstName',
                                                                                       'owner__lastName')


# View for viewing all dogs in a table
def view_dogs(request):
    # Apply sorting by attributes
    sort_by = request.GET.get('sort_by', '-dateOfArrival')

    # Fetch all filtered dogs
    dog_filter = DogFilter(request.GET, queryset=Dog.objects.all().order_by(sort_by))
    filtered_dogs = dog_filter.qs

    # Prepare a list of unique breeds, fur colors and owners, exclude redundant results
    unique_breeds = get_unique_values('breed')
    unique_colors = get_unique_values('furColor')
    unique_owners = get_unique_owners()

    # Pagination logic
    paginator = Paginator(filtered_dogs, ENTRIES_PER_PAGE)
    page = request.GET.get('page', 1)
    dogs_page = paginator.get_page(page)
    pagination_start = max(dogs_page.number - 3, 1)
    pagination_end = min(dogs_page.number + 3, paginator.num_pages)

    context = {
        'dogs': dogs_page,
        'unique_breeds': unique_breeds,
        'unique_colors': unique_colors,
        'unique_owners': unique_owners,
        'pagination_start': pagination_start,
        'pagination_end': pagination_end,
    }

    return render(request, 'view_dogs.html', context=context)


# Helper function to filter dogs based on date range.
def date_filter_logic(dogs, start_date, end_date, field_name):
    if start_date and end_date:
        dogs = dogs.filter(**{f'{field_name}__range': [start_date, end_date]})
    elif start_date:
        dogs = dogs.filter(**{f'{field_name}__gte': start_date})
    elif end_date:
        dogs = dogs.filter(**{f'{field_name}__lte': end_date})
    return dogs


# Helper function to filter dogs based on 'Unspecified' value.
def unspecified_filter(dogs, field_name, value):
    if value == "Unspecified":
        dogs = dogs.filter(Q(**{f'{field_name}__exact': ''}) | Q(**{f'{field_name}__isnull': True}))
    return dogs


# Handling Dog Filtering in the view_dogs page
def filter_dogs(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Apply sorting by attributes
        sort_by = request.GET.get('sort_by', '-dateOfArrival')

        # Initialize queryset
        dogs = Dog.objects.all().order_by(sort_by)

        # Date filtering
        for field in ['dateOfArrival', 'dateOfVaccination', 'kongDateAdded']:
            adjusted_field = field if "kong" not in field else field.replace('Date', 'date', 1)  # Handle "kongDateAdded" having a capital D
            start = request.GET.get(adjusted_field.replace('date', 'startDate'), None)
            end = request.GET.get(adjusted_field.replace('date', 'endDate'), None)
            dogs = date_filter_logic(dogs, start, end, field)

        # Retrieve dog age range from the request, handle empty cases
        age_from_str = request.GET.get('ageFrom', '0')
        min_age = float(age_from_str) if age_from_str else 0.0

        age_to_str = request.GET.get('ageTo', '20')
        max_age = float(age_to_str) if age_to_str else 20.0

        # Convert age to date range
        end_date_birth = date.today() - timedelta(days=min_age * 365)
        start_date_birth = date.today() - timedelta(days=max_age * 365)

        # If the min and max age are default values, include dogs without age attribute as well.
        if min_age == 0 and max_age == 20:
            dogs = dogs.filter(
                Q(dateOfBirthEst__range=[start_date_birth, end_date_birth]) | Q(dateOfBirthEst__isnull=True))
        else:
            # Filter by age range
            dogs = dogs.filter(dateOfBirthEst__range=[start_date_birth, end_date_birth])

        # Apply Django Filters
        filtered_dogs = DogFilter(request.GET, queryset=dogs)
        dogs = filtered_dogs.qs

        # Check for "Unspecified" conditions and apply those filters.
        unspecified_fields = ['breed', 'gender', 'furColor', 'isNeutered', 'isDangerous']
        for field in unspecified_fields:
            value = request.GET.get(field, None)
            dogs = unspecified_filter(dogs, field, value)

        # Check for "Unspecified" in Owner separately, apply filters if needed.
        owner = request.GET.get('owner', None)
        if owner == "Unspecified":
            dogs = dogs.filter(Q(owner__isnull=True))

        # Pagination
        paginator = Paginator(dogs, ENTRIES_PER_PAGE)
        page = request.GET.get('page')
        dogs_page = paginator.get_page(page)
        pagination_start = max(dogs_page.number - 3, 1)
        pagination_end = min(dogs_page.number + 3, paginator.num_pages)

        # Render table and pagination
        table_rows = ''.join([render_to_string('_dog_row.html', {'dog': dog}) for dog in dogs_page])
        pagination_html = render_to_string('_pagination.html', {
            'dogs': dogs_page,
            'pagination_start': pagination_start,
            'pagination_end': pagination_end,
        })

        return JsonResponse({'table_rows': table_rows, 'pagination_html': pagination_html}, status=200)
    else:
        return JsonResponse({'error': 'Not an AJAX request'}, status=400)
