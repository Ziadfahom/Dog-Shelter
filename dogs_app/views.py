import json
from datetime import datetime, timedelta
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from django.db.models import Prefetch
from django.db.models import Value, CharField, Count, Q
from django.db.models.functions import Concat
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from .filters import DogFilter
from .forms import SignUpForm, AddDogForm, UpdateUserForm, ProfileUpdateForm, TreatmentForm, EntranceExaminationForm, \
    DogPlacementForm, ObservesForm, ObservationForm, DogStanceForm, LoginForm, NewsForm
from .models import *
from django.conf import settings
import os
from django.core import serializers
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from datetime import date, timedelta
from django.db import IntegrityError, transaction
from io import BytesIO
from .serializers import DogSerializer
from django.views.decorators.http import require_POST





# Location of the default User profile picture if they don't have a picture
DEFAULT_IMAGE_SOURCE = '/profile_pictures/default.jpg'

# Location of the default Dog picture if they don't have a picture
DEFAULT_DOG_IMAGE_SOURCE = '/dog_pictures/default_dog.jpg'

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
    news_items = News.objects.all().order_by('-created_at')[:3]

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

def login_user_view(request):
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
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})    

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

    return render(request, 'account/register.html', {'form': form, 'profile_form': profile_form})


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
    return render(request, 'account/change_password.html', {
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
    else:
        form = NewsForm()
        context = {
            'form': form
        }
    return render(request, 'add_news.html', context)


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

        # Initialize Treatment/Examination/Placement/Session(Observes) form when adding new entries
        treatment_form = TreatmentForm(request.POST or None)
        examination_form = EntranceExaminationForm(request.POST or None)
        placement_form = DogPlacementForm(request.POST or None)
        session_form = ObservesForm(request.POST or None)

        # Get page numbers for each table from request
        treatments_page_number = request.GET.get('treatments_page', 1)
        examinations_page_number = request.GET.get('examinations_page', 1)
        placements_page_number = request.GET.get('placements_page', 1)
        sessions_page_number = request.GET.get('sessions_page', 1)
        MAX_PER_PAGE = 6  # Limit entries per page

        # Create paginators for all tables
        treatments_paginator = Paginator(
            Treatment.objects.filter(dog=dog_record).order_by('-treatmentDate'), MAX_PER_PAGE)
        examinations_paginator = Paginator(
            EntranceExamination.objects.filter(dog=dog_record).order_by('-examinationDate'), MAX_PER_PAGE)
        placements_paginator = Paginator(
            DogPlacement.objects.filter(dog=dog_record).order_by('-entranceDate'), MAX_PER_PAGE)
        sessions_paginator = Paginator(
            Observes.objects.filter(dog=dog_record).prefetch_related('observation_set').order_by('-sessionDate'), MAX_PER_PAGE)

        # Get the relevant page
        treatments = treatments_paginator.get_page(treatments_page_number)
        examinations = examinations_paginator.get_page(examinations_page_number)
        placements = placements_paginator.get_page(placements_page_number)
        sessions = sessions_paginator.get_page(sessions_page_number)

        # Handle user submitting a new Treatment/Examination/Placement/Session form
        if request.method == "POST":

            # Ensure only one form is submitted
            # Check if it's a Treatment form
            if treatment_form.is_valid():
                new_treatment = treatment_form.save(commit=False)
                new_treatment.dog = dog_record
                new_treatment.save()

                # If this is an AJAX request, send back the new treatments data
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    treatments_data = Treatment.objects.filter(dog=dog_record).order_by('-treatmentDate')[:MAX_PER_PAGE]
                    data = {
                        'data': [render_to_string('_treatment_row.html',
                                                  {'treatment': treatment}) for treatment in treatments_data],
                        'pagination': render_to_string('_dog_record_pagination.html',
                                                       {'paginated_data': treatments,
                                                        'param_name': 'treatments_page'})
                    }
                    return JsonResponse(data)
                else:
                    # Redirect back to the dog_record_view to see the new treatment.
                    return redirect('dogs_app:dog_record', pk=dog_record.pk)

            # Check if it's an Examination form
            elif examination_form.is_valid():
                new_examination = examination_form.save(commit=False)
                new_examination.dog = dog_record
                new_examination.save()

                # If this is an AJAX request, send back the new Examination data
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    examinations_data = EntranceExamination.objects.filter(dog=dog_record).order_by('-examinationDate')[:MAX_PER_PAGE]
                    data = {
                        'data': [render_to_string('_examination_row.html',
                                                  {'examination': examination}) for examination in examinations_data],
                        'pagination': render_to_string('_dog_record_pagination.html',
                                                       {'paginated_data': examinations,
                                                        'param_name': 'examinations_page'})
                    }
                    return JsonResponse(data)
                else:
                    # Redirect back to the dog_record_view to see the new treatment.
                    return redirect('dogs_app:dog_record', pk=dog_record.pk)

            # Check if it's a Placement form
            elif placement_form.is_valid():
                new_placement = placement_form.save(commit=False)
                new_placement.dog = dog_record
                new_placement.save()

                # If this is an AJAX request, send back the new Placement data
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    placements_data = DogPlacement.objects.filter(dog=dog_record).order_by('-entranceDate')[:MAX_PER_PAGE]
                    data = {
                        'data': [render_to_string('_placement_row.html',
                                                  {'placement': placement}) for placement in placements_data],
                        'pagination': render_to_string('_dog_record_pagination.html',
                                                       {'paginated_data': placements,
                                                        'param_name': 'placements_page'})
                    }
                    return JsonResponse(data)
                else:
                    # Redirect back to the dog_record_view to see the new placement.
                    return redirect('dogs_app:dog_record', pk=dog_record.pk)

            # Check if it's a Session (Observes) form
            elif session_form.is_valid():
                new_session = session_form.save(commit=False)
                new_session.dog = dog_record
                new_session.save()

                # If this is an AJAX request, send back the new Session data
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    sessions_data = Observes.objects.filter(dog=dog_record).order_by('-sessionDate')[:MAX_PER_PAGE]
                    data = {
                        'data': [render_to_string('_session_row.html',
                                                  {'session': session}) for session in sessions_data],
                        'pagination': render_to_string('_dog_record_pagination.html',
                                                       {'paginated_data': sessions,
                                                        'param_name': 'sessions_page'})
                    }
                    return JsonResponse(data)
                else:
                    # Redirect back to the dog_record_view to see the new placement.
                    return redirect('dogs_app:dog_record', pk=dog_record.pk)

        # Check if request is AJAX call for switching pages
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'data': [],
                'pagination': ''
            }
            if 'treatments_page' in request.GET:
                data['data'] = [render_to_string('_treatment_row.html', {'treatment': treatment}) for treatment in
                                treatments]
                data['pagination'] = render_to_string('_dog_record_pagination.html',
                                                      {'paginated_data': treatments, 'param_name': 'treatments_page'})
            elif 'examinations_page' in request.GET:
                data['data'] = [render_to_string('_examination_row.html', {'examination': examination}) for examination
                                in examinations]
                data['pagination'] = render_to_string('_dog_record_pagination.html',
                                                      {'paginated_data': examinations, 'param_name': 'examinations_page'})
            elif 'placements_page' in request.GET:
                data['data'] = [render_to_string('_placement_row.html', {'placement': placement}) for placement
                                in placements]
                data['pagination'] = render_to_string('_dog_record_pagination.html',
                                                      {'paginated_data': placements, 'param_name': 'placements_page'})
            elif 'sessions_page' in request.GET:
                data['data'] = [render_to_string('_session_row.html', {'session': session}) for session
                                in sessions]
                data['pagination'] = render_to_string('_dog_record_pagination.html',
                                                      {'paginated_data': sessions, 'param_name': 'sessions_page'})
            return JsonResponse(data)

        context = {
            'dog_record': dog_record,
            'treatments': treatments,
            'examinations': examinations,
            'placements': placements,
            'sessions': sessions,
            'treatment_form': treatment_form,
            'examination_form': examination_form,
            'placement_form': placement_form,
            'session_form': session_form,
        }

        return render(request, 'dog_record.html', context=context)

    # User is NOT logged in --> send them to login page
    else:
        messages.error(request, message='You Must Be Logged In To View That Page...')
        return redirect('dogs_app:home')


# Handle Observations display
def view_observations(request, session_id):
    if request.user.is_authenticated:
        dog_stances = DogStance.objects.all().order_by('stanceStartTime')
        observations = Observation.objects.filter(observes_id=session_id).prefetch_related(
            Prefetch('dogstance_set', queryset=dog_stances, to_attr='related_dog_stances')
        ).order_by('-obsDateTime')
        session_instance = Observes.objects.get(pk=session_id)

        if request.method == 'POST':
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Handle DogStance form submission via AJAX
                stance_form = DogStanceForm(request.POST or None)
                if stance_form.is_valid():
                    try:
                        new_stance = stance_form.save(commit=False)
                        new_stance.observation_id = request.POST.get('observation_id')
                        new_stance.save()
                        return JsonResponse({
                            "status": "success",
                            "new_stance": {
                                'id': new_stance.id,
                                'stanceStartTime': new_stance.stanceStartTime,
                                'dogStance': new_stance.get_dogStance_display(),
                                'dogLocation': new_stance.get_dogLocation_display() if new_stance.dogLocation else "-",
                                'observation': new_stance.observation_id,
                            }
                        }, status=201)
                    except IntegrityError:
                        return JsonResponse({"status": "error", "errors": "Duplicate Stance Start Time"}, status=400)
                else:
                    return JsonResponse({"status": "error", "errors": stance_form.errors}, status=400)

            else:
                stance_form = DogStanceForm()

            observation_form = ObservationForm(request.POST or None, request.FILES or None)
            if observation_form.is_valid():
                new_observation = observation_form.save(commit=False)
                new_observation.observes = session_instance
                new_observation.save()
                messages.success(request, 'Success! Observation has been successfully added.')
                return redirect('dogs_app:view_observations', session_id=session_id)
        else:
            observation_form = ObservationForm()
            stance_form = DogStanceForm()

        # Pagination
        paginator = Paginator(observations, ENTRIES_PER_PAGE)
        page_number = request.GET.get('page')
        paginated_observations = paginator.get_page(page_number)
        context = {
            'observations': observations,
            'paginated_observations': paginated_observations,
            'session_instance': session_instance,
            'observation_form': observation_form,
            'stance_form': stance_form,
        }

        return render(request, 'view_observations.html', context=context)
    else:
        messages.error(request, message='You Must Be Logged In To View That Page...')
        return redirect('dogs_app:home')


# Handle deleting an Observation
@require_POST  # Ensures this view can only be accessed with POST request
def delete_observation(request):
    if request.method == 'POST' and request.user.is_authenticated and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        observation_id = request.POST.get('observation_id')
        try:
            observation = Observation.objects.get(id=observation_id)
            observation.delete()
            return JsonResponse({"status": "success"})
        except Observation.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Observation not found"}, status=404)
    else:
        return JsonResponse({"status": "error", "message": "Unauthorized"}, status=401)


# Handle editing an Observation
def edit_observation(request, observation_id):
    if request.method == 'GET':
        observation = Observation.objects.get(id=observation_id)
        observation_form = ObservationForm(instance=observation)
        # Exclude the file field from the JSON response
        observation_data = observation_form.initial
        # Temporary! Remove the file fields from the JSON response
        del observation_data['jsonFile'] # TODO: Remove this line once the JSON file is implemented
        del observation_data['rawVideo'] # TODO: Remove this line once the raw video is implemented
        return JsonResponse({"status": "success", "observation": observation_data}, status=200)

    elif request.method == 'POST':
        observation_form = ObservationForm(request.POST or None, instance=Observation.objects.get(id=observation_id))
        if observation_form.is_valid():
            observation_form.save()
            # Get the updated observation
            updated_observation = Observation.objects.get(id=observation_id)
            # Render the _observation_row.html template with the updated observation
            new_row_html = render_to_string('_observation_row.html', {'observation': updated_observation})
            return JsonResponse(
                {"status": "success", "observation": observation_form.cleaned_data, "newRowHtml": new_row_html},
                status=200)
        else:
            return JsonResponse({"status": "error", "errors": observation_form.errors}, status=400)


# Handle deleting a DogStance
@require_POST # Ensures this view can only be accessed with POST request
def delete_stance(request):
    if request.method == 'POST' and request.user.is_authenticated and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        stance_id = request.POST.get('stance_id')
        try:
            dog_stance = DogStance.objects.get(id=stance_id)
            dog_stance.delete()
            return JsonResponse({"status": "success"})
        except DogStance.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Dog Stance not found"}, status=404)
    else:
        return JsonResponse({"status": "error", "message": "Unauthorized"}, status=401)


# Handle editing a DogStance
def edit_dog_stance(request, stance_id):
    if request.method == 'GET':
        stance = DogStance.objects.get(id=stance_id)
        stance_form = DogStanceForm(instance=stance)
        stance_data = stance_form.initial
        return JsonResponse({"status": "success", "stance": stance_data}, status=200)

    elif request.method == 'POST':
        stance_form = DogStanceForm(request.POST or None, instance=DogStance.objects.get(id=stance_id))
        if stance_form.is_valid():
            saved_stance = stance_form.save()
            observation_id = saved_stance.observation.id

            updated_stance = DogStance.objects.get(id=stance_id)
            new_row_html = render_to_string('_observation_row.html', {'stance': updated_stance})
            return JsonResponse(
               {"status": "success", "stance": stance_form.cleaned_data, "newRowHtml": new_row_html, "observationId": observation_id},
               status=200)
        else:
            return JsonResponse({"status": "error", "errors": stance_form.errors}, status=400)


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
    else:
        form = NewsForm(instance=news)
    return render(request, 'update_news.html', {'news': news, 'form': form})


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


# Render Graphs page
def graphs(request):
    return render(request, 'graphs.html')


# View for the Dynamic Graphs page
def chart_data(request):

    # Prepare a dictionary in JSON for distribution of dogs by gender,  vaccination, isneutered, and isdangerous
    health_metrics = get_health_metrics_dict()

    # Get all the Dogs that have received a Kong Toy
    dogs_with_kong = Dog.objects.filter(kongDateAdded__isnull=False)

    # Get all Observations with and without a Kong Toy
    obs_with_kong = Observation.objects.filter(isKong='Y', obsDateTime__isnull=False)
    obs_without_kong = Observation.objects.filter(isKong='N', obsDateTime__isnull=False)

    # Fetch a dictionary of the top combined stance+position in DogStances,
    # with their counts of "with" and "without" kong individually
    top_stance_position_combos = fetch_top_stance_position_combos(obs_with_kong, obs_without_kong)

    # Getting breeds and their counts
    dog_breeds = Dog.objects.values('breed').annotate(total=Count('breed')).exclude(breed='').exclude(breed__isnull=True).order_by('-total')

    # Count of DogStances with and without kong toy, then make sure we use the front-end names of the values
    stances_with_kong = DogStance.objects.filter(observation__in=obs_with_kong).values('dogStance').annotate(
        total=models.Count('observation'))
    stances_with_kong = map_stances_to_frontend(list(stances_with_kong))

    stances_without_kong = DogStance.objects.filter(observation__in=obs_without_kong).values('dogStance').annotate(
        total=models.Count('observation'))
    stances_without_kong = map_stances_to_frontend(list(stances_without_kong))

    # Define the limit for the required top dog stances then fetch
    # those values for "Dog Stances Across The Week" Graph
    TOP_STANCES_LIMIT = 5
    top_dog_stances = get_top_dog_stances(TOP_STANCES_LIMIT)

    stance_count_by_day = get_stance_count_by_day(top_dog_stances)

    # Preparing data to be used in the frontend
    data = {
        'dogs_with_kong': serializers.serialize('json', dogs_with_kong),
        'stances_with_kong': list(stances_with_kong),
        'stances_without_kong': list(stances_without_kong),
        'dog_breeds': list(dog_breeds),
        'stance_count_by_day': stance_count_by_day,
        'top_stance_position_combos': top_stance_position_combos,
        'health_metrics': health_metrics,
    }

    return JsonResponse(data)


# Switch the Stances names to the front-end friendly version
def map_stances_to_frontend(stances):
    # Prepare a dictionary for the front-end names
    DOG_STANCE_DICT = dict(DogStance.DOG_STANCE_CHOICES)

    for stance in stances:
        stance['dogStance'] = DOG_STANCE_DICT.get(stance['dogStance'], stance['dogStance'])
    return stances


# Returns the top dog stances, parameter to set limit
def get_top_dog_stances(limit=5):

    # Fetch and count the occurrences of each dogStance from the database for Dog Stances Across The Week
    dog_stance_counts = DogStance.objects.values('dogStance').annotate(total_count=Count('dogStance')).order_by(
        '-total_count')

    # Create a list to store the top X dogStances
    top_dog_stances = []

    # Collect the top X dogStances
    for i, entry in enumerate(dog_stance_counts):
        if i >= limit:
            break
        top_dog_stances.append(entry['dogStance'])

    return top_dog_stances


# Get a dictionary of each Dog Stance's occurrences in every day of the week, for a selected list of Stances
def get_stance_count_by_day(top_dog_stances):
    days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']

    # Initialize a dictionary to hold the stance count for each day of the week
    stance_count_by_day = {}
    for day in days_of_week:
        stance_count_by_day[day] = {}
        for stance in top_dog_stances:
            stance_count_by_day[day][stance] = 0

    # Query the database to get the stances and their observation dates
    stances_with_datetime = DogStance.objects.select_related('observation').values('observation__obsDateTime',
                                                                                   'dogStance')
    # Mapping of Python's datetime.weekday() indexes to actual day names
    days_of_week_mapping = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday',
                            6: 'Sunday'}

    # Mapping of value names in Dog Stances
    stance_name_mapping = {backend: frontend for backend, frontend in DogStance.DOG_STANCE_CHOICES}

    # Loop to populate the dictionary with actual data
    for entry in stances_with_datetime:
        # Convert the UTC time in the database to local time
        utc_observation_time = entry['observation__obsDateTime']
        local_observation_time = timezone.localtime(utc_observation_time)

        # Get the local weekday index (Monday is 0, Sunday is 6)
        day_index = local_observation_time.weekday()

        # Map the weekday index to its string name
        day_name = days_of_week_mapping[day_index]

        # Skip Friday and Saturday
        if day_name in ['Friday', 'Saturday']:
            continue  # Skip to next iteration of the loop, ignoring this entry

        # Fetch the stance for this particular record
        stance = entry['dogStance']

        # If this stance is among the top stances we are tracking, update the count
        if stance in top_dog_stances:
            stance_count_by_day[day_name][stance] += 1

    transformed_stance_count_by_day = {}

    for day, stances in stance_count_by_day.items():
        transformed_stances = {}
        for stance_key, count in stances.items():
            transformed_key = stance_name_mapping.get(stance_key, "Unknown")
            transformed_stances[transformed_key] = count
        transformed_stance_count_by_day[day] = transformed_stances

    return transformed_stance_count_by_day


# Helper function for fetching a top 10 list of combined dogStances + dogPositions and their counts with/without kongs
def fetch_top_stance_position_combos(obs_with_kong, obs_without_kong):
    # Define the mapping dictionaries for the final display
    stance_choices_dict = dict(DogStance.DOG_STANCE_CHOICES)
    location_choices_dict = dict(DogStance.DOG_LOCATION_CHOICES)

    # Fetch a list of top stance+location combinations with kong
    stance_pos_combo_with = DogStance.objects \
                                .filter(observation__in=obs_with_kong) \
                                .annotate(stance_location=Concat('dogStance',
                                                                 Value(' + '),
                                                                 'dogLocation',
                                                                 output_field=CharField())) \
                                .values('stance_location') \
                                .annotate(count=Count('stance_location')) \
                                .order_by('-count')[:10]

    # Fetch a list of top stance+location combinations with kong
    stance_pos_combo_without = DogStance.objects \
                                   .filter(observation__in=obs_without_kong) \
                                   .annotate(stance_location=Concat('dogStance',
                                                                    Value(' + '),
                                                                    'dogLocation',
                                                                    output_field=CharField())) \
                                   .values('stance_location') \
                                   .annotate(count=Count('stance_location')) \
                                   .order_by('-count')[:10]

    # Replace the values in the QuerySets for both lists
    for stance in stance_pos_combo_with:
        stance_db, location_db = stance['stance_location'].split(' + ')
        location_display = location_choices_dict.get(location_db, '')
        stance[
            'stance_location'] = f"{stance_choices_dict[stance_db]} {location_display}".strip()

    for stance in stance_pos_combo_without:
        stance_db, location_db = stance['stance_location'].split(' + ')
        location_display = location_choices_dict.get(location_db, '')
        stance[
            'stance_location'] = f"{stance_choices_dict[stance_db]} {location_display}".strip()

    # Union of both lists keys
    unique_keys = set([item['stance_location'] for item in stance_pos_combo_with] + [item['stance_location'] for item in
                                                                                     stance_pos_combo_without])

    # Initialize dictionaries with zeros
    dict_with = {key: 0 for key in unique_keys}
    dict_without = {key: 0 for key in unique_keys}

    # Populate the dictionaries with actual counts
    for item in stance_pos_combo_with:
        dict_with[item['stance_location']] = item['count']

    for item in stance_pos_combo_without:
        dict_without[item['stance_location']] = item['count']

    # Create a list containing the unique combinations and their counts in both lists
    combined_list = [(key, dict_with[key], dict_without[key]) for key in unique_keys]

    # Sort the list based the sum of both counts for sorting
    combined_list.sort(key=lambda x: x[1] + x[2], reverse=True)

    # Return the combined top 10 Stance+Position combos and the counts for both with and without kong
    return combined_list[:10]


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


# Prepare a dictionary in JSON for distribution of dogs
# by gender,  vaccination, isneutered, and isdangerous. Used for health_metrics_chart.
def get_health_metrics_dict():
    # Fetch required attributes of all dogs
    dogs_data = Dog.objects.values_list('gender',  'dateOfVaccination', 'isNeutered', 'isDangerous')

    # Initialize data structure
    health_metrics_dict = {
        'gender': {'M': 0, 'F': 0},
        'vaccinated': {'M': {'Y': 0, 'N': 0}, 'F': {'Y': 0, 'N': 0}},
        'neutered': {
            'M': {'Y': {'Y': 0, 'N': 0, '-': 0}, 'N': {'Y': 0, 'N': 0, '-': 0}},
            'F': {'Y': {'Y': 0, 'N': 0, '-': 0}, 'N': {'Y': 0, 'N': 0, '-': 0}}}
        # 'dangerous': {
        #     'M': {'Y': {'Y': {'Y': 0, 'N': 0, '-': 0}, 'N': {'Y': 0, 'N': 0, '-': 0}, '-': {'Y': 0, 'N': 0, '-': 0}},
        #           'N': {'Y': {'Y': 0, 'N': 0, '-': 0}, 'N': {'Y': 0, 'N': 0, '-': 0}, '-': {'Y': 0, 'N': 0, '-': 0}}},
        #     'F': {'Y': {'Y': {'Y': 0, 'N': 0, '-': 0}, 'N': {'Y': 0, 'N': 0, '-': 0}, '-': {'Y': 0, 'N': 0, '-': 0}},
        #           'N': {'Y': {'Y': 0, 'N': 0, '-': 0}, 'N': {'Y': 0, 'N': 0, '-': 0}, '-': {'Y': 0, 'N': 0, '-': 0}}}}
    }

    # Loop through each dog entry to populate chart_data
    for gender, dateOfVaccination, isNeutered, isDangerous in dogs_data:
        # Gender can't be Null/empty

        # Calculate if vaccination is within the last 365 days or not, if null set as No as well
        if dateOfVaccination:
            current_date = datetime.now().date()
            delta = current_date - dateOfVaccination
            isVaccinated = 'Y' if delta.days <= 365 else 'N'
        else:
            isVaccinated = 'N'

        # Handle Nulls and empties
        isNeutered = isNeutered or '-'
        isDangerous = isDangerous or '-'

        # Populate the counters
        health_metrics_dict['gender'][gender] += 1
        health_metrics_dict['vaccinated'][gender][isVaccinated] += 1
        health_metrics_dict['neutered'][gender][isVaccinated][isNeutered] += 1
        # health_metrics_dict['dangerous'][gender][isVaccinated][isNeutered][isDangerous] += 1

    # def flatten_dict(d, parent_key='', sep='/'):
    #     items = {}
    #     for k, v in d.items():
    #         new_key = f"{parent_key}{sep}{k}" if parent_key else k
    #         if isinstance(v, dict):
    #             items.update(flatten_dict(v, new_key, sep=sep))
    #         else:
    #             items[new_key] = v
    #     return items
    #
    # flattened_dict = flatten_dict(health_metrics_dict)
    # print(flattened_dict)

    return health_metrics_dict


# View for displaying all News in a dedicated news page
def view_news(request):
    news_list = News.objects.all().order_by('-created_at')  # Fetch news in descending order
    context = {'news_list': news_list}
    return render(request, 'news_page.html', context)


# View for viewing all dogs in a table
def view_dogs(request):
    # Check if user is logged in
    if request.user.is_authenticated:
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
    # If user is not logged in/authenticated, show an error message and redirect to home.
    else:
        messages.error(request, "You Must Be Logged In To Add New Dogs...")
        return redirect('dogs_app:home')


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
            # Handle "kongDateAdded" having a capital D
            adjusted_field = field if "kong" not in field else field.replace('Date', 'date', 1)

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

        # Store all dog IDs being displayed in case user wants to export the data using get_filtered_dogs_id()
        filtered_dogs_ids = list(dogs.values_list('dogID', flat=True))
        request.session['filtered_dogs_ids'] = filtered_dogs_ids

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


# Helper function for getting all dog IDs for dogs being filtered on the page (for exporting data in JSON/Excel)
def get_filtered_dog_ids(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        filtered_dogs_ids = request.session.get('filtered_dogs_ids', [])
        return JsonResponse({'filtered_dogs_ids': filtered_dogs_ids}, status=200)
    else:
        return JsonResponse({'error': 'Not an AJAX request'}, status=400)


# Main function to export Dogs in JSON format
def export_dogs_json(request):
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            dog_ids = json.loads(request.POST.get('dog_ids'))

            # Use select_related and prefetch_related for optimization and fetching all associated entities
            dogs = Dog.objects\
                .select_related('owner')\
                .prefetch_related('entranceexamination_set',
                                  'treatment_set',
                                  'dogplacement_set__kennel',
                                  Prefetch('observers',
                                           queryset=Observes.objects.prefetch_related(
                                               Prefetch('observation_set',
                                                        queryset=Observation.objects
                                                        .prefetch_related('dogstance_set')))))\
                .filter(dogID__in=dog_ids)

            # Serialize dogs
            dog_data = DogSerializer.serialize_dogs(dogs)

            # Add a root key "data" to wrap the list
            wrapped_dog_data = {'data': dog_data}

            return JsonResponse(wrapped_dog_data, safe=False)


# View for handling Excel file exports in view_dogs page
def export_dogs_excel(request):
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body.decode('utf-8'))
                dog_ids = data.get('dog_ids', [])
                sort_by = data.get('sort_by', '-dateOfArrival')

                # Filter and sort dogs
                dogs = Dog.objects.filter(dogID__in=dog_ids).order_by(sort_by)

                # Create workbook and worksheet
                wb = Workbook()
                ws = wb.active
                ws.title = "Dogsheler Dogs Data"

                # Define headers and write them to the first row
                headers = ['Chip Number', 'Name', 'Date of Birth', 'Date of Arrival',
                           'Date of Vaccination', 'Breed', 'Gender', 'Fur Color', 'Neutered',
                           'Dangerous', 'Image', 'Last Kong Date Given', 'Owner']

                # Styling headers with bold font and background color
                header_font = Font(bold=True, color="FFFFFF")
                data_font = Font(name='Arial', size=11)

                # Define fills
                header_fill = PatternFill(start_color="0070C0",
                                          end_color="0070C0", fill_type="solid")
                light_blue_fill = PatternFill(start_color="D9EBF5", end_color="D9EBF5", fill_type="solid")
                light_gray_fill = PatternFill(start_color="E5E5E5", end_color="E5E5E5", fill_type="solid")

                # Define Center alignment
                center_aligned = Alignment(horizontal="center", vertical="center")

                # Define border
                thin_border = Border(left=Side(style='thin'),
                                     right=Side(style='thin'),
                                     top=Side(style='thin'),
                                     bottom=Side(style='thin'))

                # Header row styling
                for col_num, header in enumerate(headers, 1):
                    col_letter = get_column_letter(col_num)
                    cell = ws['{}1'.format(col_letter)]
                    cell.value = header
                    cell.font = header_font
                    cell.fill = header_fill
                    cell.alignment = center_aligned
                    cell.border = thin_border
                    ws.column_dimensions[col_letter].width = 15 if header not in ['Gender', 'Neutered', 'Dangerous'] else 10

                # Check if dogs queryset is empty
                if not dogs.exists():
                    # Merge cells from A2 to N2 (14 columns)
                    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=13)

                    # Reference to the merged cell
                    merged_cell = ws.cell(row=2, column=1)

                    # Populate the merged cell
                    merged_cell.value = "No Data Available"

                    # Style the merged cell
                    merged_cell.font = Font(name='Arial', size=12, bold=True)
                    merged_cell.alignment = center_aligned
                    merged_cell.fill = PatternFill(start_color="FFFF99", end_color="FFFF99", fill_type="solid")
                    merged_cell.border = thin_border

                # Otherwise, proceed with populating Excel file with dog data and apply styles
                else:
                    # Populate Excel file with dog data and apply styles
                    for row_num, dog in enumerate(dogs, 2):  # Start from row 2 to not overwrite headers
                        for col_num in range(1, 14):  # 13 columns in total
                            # Determine row color
                            if row_num % 2 == 0:
                                row_fill = light_gray_fill
                            else:
                                row_fill = light_blue_fill

                            cell = ws.cell(row=row_num, column=col_num)

                            # Populate the cell based on the column number
                            cell.value = {
                                1: dog.chipNum if dog.chipNum else "N/A",
                                2: dog.dogName if dog.dogName else "N/A",
                                3: dog.dateOfBirthEst if dog.dateOfBirthEst else "N/A",
                                4: dog.dateOfArrival if dog.dateOfArrival else "N/A",
                                5: dog.dateOfVaccination if dog.dateOfVaccination else "N/A",
                                6: dog.breed if dog.breed else "N/A",
                                7: dog.get_gender_display() if dog.gender else "N/A",
                                8: dog.furColor if dog.furColor else "N/A",
                                9: dog.get_isNeutered_display() if dog.isNeutered else "N/A",
                                10: dog.get_isDangerous_display() if dog.isDangerous else "N/A",
                                11: str(dog.dogImage) if dog.dogImage else "N/A",
                                12: dog.kongDateAdded if dog.kongDateAdded else "N/A",
                                13: str(dog.owner) if dog.owner else "N/A"
                            }.get(col_num)

                            # Apply styling
                            cell.font = data_font
                            cell.alignment = center_aligned
                            cell.border = thin_border
                            cell.fill = row_fill

                # Initialize BytesIO and save workbook to it
                excel_file = BytesIO()
                wb.save(excel_file)
                excel_file.seek(0)

                # Prepare the HttpResponse
                response = HttpResponse(
                    excel_file.read(),
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = 'attachment; filename=dogs_data.xlsx'

                return response
            except Exception as e:
                # Handling any exception that occurs during export
                error_message = f"Export failed due to error: {str(e)}"
                return JsonResponse({'status': 'error', 'message': error_message}, status=400)
        else:
            return JsonResponse({'error': 'Not an AJAX request'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


# View for handling Excel file imports in view_dogs page
def import_dogs_excel(request):
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                excel_file = request.FILES['excel_file']
                wb = load_workbook(excel_file)
                ws = wb.active

                dog_count = 0  # Initialize a counter for imported dogs

                # Start the transaction block
                with transaction.atomic():
                    # Iterate through each row in the worksheet
                    for row_number, row in enumerate(ws.iter_rows(min_row=2), start=2):
                        try:
                            # Validate Data First
                            gender_value = 'M'
                            is_neutered_value = ''
                            is_dangerous_value = ''

                            if row[6].value:
                                gender_value = 'M' if row[6].value.lower() in ['male', 'm'] or row[6].value in ['זכר', 'ז'] \
                                    else 'F' if row[6].value.lower() in ['female', 'f'] or row[6].value in ['נקבה', 'נ'] \
                                    else 'M'
                            if row[8].value:
                                is_neutered_value = 'Y' if row[8].value.lower() in ['yes', 'y'] or row[8].value in ['כן', 'כ'] \
                                    else 'N' if row[8].value.lower() in ['no', 'n'] or row[8].value in ['לא', 'ל'] \
                                    else ''
                            if row[9].value:
                                is_dangerous_value = 'Y' if row[9].value.lower() in ['yes', 'y'] or row[9].value in ['כן', 'כ'] \
                                    else 'N' if row[9].value.lower() in ['no', 'n'] or row[9].value in ['לא', 'ל'] \
                                    else ''

                            date_of_arrival_value = row[3].value
                            if not date_of_arrival_value:
                                date_of_arrival_value = timezone.now().date()

                            # dog_image_url = None if row[10].value is None else '/static/img/' + row[10].value
                            dog_image_url = None # TO-DO Work on Images

                            dog_data = {
                                'chipNum': row[0].value,
                                'dogName': row[1].value,
                                'dateOfBirthEst': row[2].value,
                                'dateOfArrival': date_of_arrival_value,
                                'dateOfVaccination': row[4].value,
                                'breed': row[5].value,
                                'gender': gender_value,
                                'furColor': row[7].value,
                                'isNeutered': is_neutered_value,
                                'isDangerous': is_dangerous_value,
                                'dogImage': dog_image_url,
                                'kongDateAdded': row[11].value,
                                'owner': None
                                # 'owner': omitted for now
                            }

                            # Attempt to create a new Dog instance
                            new_dog = Dog(**dog_data)
                            new_dog.full_clean()  # This will raise ValidationError for any field issues
                            new_dog.save()
                            # Increment dog count
                            dog_count += 1

                        except ValidationError as e:
                            # Handling specific field validation errors
                            error_details = "\n".join(
                                [f"Column '{k}': {', '.join(v)}" for k, v in e.message_dict.items()])
                            error_message = f"Import error at row {row_number}:{error_details}"
                            raise ValueError(error_message)

                        except IntegrityError as e:
                            # Handling unique constraint violations like chipNum uniqueness
                            error_message = f"Import error at row {row_number}:{str(e)}"
                            raise ValueError(error_message)

                    # add success message with dog count
                    if dog_count == 1:
                        success_message = "1 dog has been successfully imported!"
                    else:
                        success_message = f"{dog_count} dogs have been successfully imported!"
                    return JsonResponse({'status': 'success', 'message': success_message}, status=200)
            except ValueError as e:
                # Handling custom ValueError which now includes detailed row information
                error_message = f"Import cancelled due to error:{e}"
                return JsonResponse({'status': 'error', 'message': error_message}, status=400)

            except Exception as e:
                # General error handling
                general_error_message = f"General error occurred: {str(e)}. Import cancelled."
                return JsonResponse({'status': 'error', 'message': general_error_message}, status=400)
        else:
            # If request is not AJAX, return error
            return JsonResponse({'error': 'Not an AJAX request'}, status=400)
    else:
        # If request method is not POST, return error
        return JsonResponse({'error': 'Invalid request method'}, status=400)


# View for handling JSON file imports in view_dogs page
def import_dogs_json(request):
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                json_file = request.FILES['json_file']
                data = json.load(json_file)['data']

                dog_count = 1  # Initialize a counter for imported dogs

                # Start the transaction block
                with transaction.atomic():
                    # Iterate through each dog in the data
                    for dog_info in data:
                        try:
                            # Remove dogID from the data, hold the rest of the associated entities
                            dog_info.pop('dogID', None)

                            # Hold the rest of the associated entities
                            owner_info = dog_info.pop('owner', None)
                            treatments_info = dog_info.pop('treatments', [])
                            examinations_info = dog_info.pop('entranceExaminations', [])
                            dogPlacements_info = dog_info.pop('dogPlacements', [])
                            observes_info = dog_info.pop('observes', [])

                            # Default 'dateOfArrival' to today if not provided
                            if not dog_info.get('dateOfArrival'):
                                dog_info['dateOfArrival'] = timezone.now().date().isoformat()

                            # Handle 'owner' field
                            owner = None  # In case we don't need to associate Dog with an Owner
                            if owner_info:
                                owner_info.pop('ownerSerialNum', None)  # Remove ownerSerialNum which is PK auto field
                                owner_id = owner_info.get('ownerID', None)

                                if owner_id:
                                    # If ownerID is provided, use get_or_create
                                    owner, created = Owner.objects.get_or_create(
                                        ownerID=owner_id,
                                        defaults={k: v for k, v in owner_info.items()}
                                    )

                                    if not created:
                                        # If owner already exists, update the owner info
                                        for k, v in owner_info.items():
                                            setattr(owner, k, v)
                                        owner.save()
                                else:
                                    # ownerID not provided, create an owner without one
                                    owner = Owner(**owner_info)
                                    owner.save()

                            # Extract and validate dog data from dog_info
                            # Create Dog instance and save
                            new_dog = Dog(**dog_info, owner=owner)
                            new_dog.full_clean()
                            new_dog.save()

                            # Handle 'treatment' field
                            for treatment_info in treatments_info:
                                treatment_info.pop('treatmentID', None)
                                new_treatment = Treatment(**treatment_info, dog=new_dog)
                                new_treatment.full_clean()  # Validate the treatment data
                                new_treatment.save()

                            # Handle 'entranceExamination' field
                            for examination_info in examinations_info:
                                examination_info.pop('examinationID', None)
                                new_examination = EntranceExamination(**examination_info, dog=new_dog)
                                new_examination.full_clean()
                                new_examination.save()

                            # Handle 'dogPlacement' field
                            for dogPlacement_info in dogPlacements_info:
                                kennel_num = dogPlacement_info.pop('kennelNum', None)
                                kennel_image = dogPlacement_info.pop('kennelImage', None)

                                kennel = None

                                if kennel_num:
                                    kennel, created = Kennel.objects.get_or_create(
                                        kennelNum=kennel_num,
                                        defaults={'kennelImage': kennel_image}
                                    )

                                    if not created:
                                        # If kennel already exists, update the kennel info
                                        kennel.kennelImage = kennel_image
                                        kennel.save()

                                new_dogPlacement = DogPlacement(**dogPlacement_info, dog=new_dog, kennel=kennel)
                                new_dogPlacement.full_clean()
                                new_dogPlacement.save()

                            # Handle 'observes' field
                            for observes_data in observes_info:
                                camID = observes_data.pop('camID', None)
                                observations_info = observes_data.pop('observations', [])

                                # Default 'sessionDate' to today if not provided
                                if not observes_data.get('sessionDate'):
                                    observes_data['sessionDate'] = timezone.now().date().isoformat()

                                camera = None
                                if camID:
                                    camera, created = Camera.objects.get_or_create(camID=camID)

                                new_observes = Observes(**observes_data, dog=new_dog, camera=camera)
                                new_observes.full_clean()
                                new_observes.save()

                                # Handle 'observation' field
                                for observation_data in observations_info:

                                    # Default 'obsDateTime' to today if not provided
                                    if not observation_data.get('obsDateTime'):
                                        observation_data['obsDateTime'] = timezone.now().date().isoformat()

                                    dogStances_info = observation_data.pop('dogStances', [])

                                    new_observation = Observation(**observation_data, observes=new_observes)
                                    new_observation.full_clean()
                                    new_observation.save()

                                    # Handle 'dogStance' field
                                    for dogStance_data in dogStances_info:

                                        new_dogStance = DogStance(**dogStance_data, observation=new_observation)
                                        new_dogStance.full_clean()
                                        new_dogStance.save()

                        except ValidationError as e:
                            # Handling specific field validation errors
                            error_details = "\n".join(
                                [f"Field '{k}': {', '.join(v)}" for k, v in e.message_dict.items()])
                            error_message = f"Dog #{dog_count}, {error_details}"
                            raise ValueError(error_message)

                        except IntegrityError as e:
                            # Handling unique constraint violations like chipNum uniqueness
                            error_message = f"Dog #{dog_count}, {str(e)}"
                            raise ValueError(error_message)

                        dog_count += 1  # Increment after each successful processing

                    # add success message with dog count
                    if dog_count == 1:  # No dogs were successfully imported
                        success_message = ("Import Completed: No new dogs were added. "
                                           "Please check the data for accuracy or duplication.")
                    elif dog_count == 2:  # Since we start count from 1, 2 means only 1 dog processed
                        success_message = "1 dog has been successfully imported!"
                    else:
                        success_message = f"{dog_count - 1} dogs have been successfully imported!"
                    return JsonResponse({'status': 'success', 'message': success_message}, status=200)
            except ValueError as e:
                # Handling custom ValueError which now includes detailed row information
                error_message = f"Import Cancelled: Error Detected - {e}"
                return JsonResponse({'status': 'error', 'message': error_message}, status=400)

            except Exception as e:
                # General error handling
                general_error_message = f"General error occurred: {str(e)}. Import cancelled."
                return JsonResponse({'status': 'error', 'message': general_error_message}, status=400)
        else:
            # If request is not AJAX, return error
            return JsonResponse({'error': 'Not an AJAX request'}, status=400)
    else:
        # If request method is not POST, return error
        return JsonResponse({'error': 'Invalid request method'}, status=400)