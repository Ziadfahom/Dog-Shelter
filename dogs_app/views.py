from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from .forms import SignUpForm, AddDogForm, UpdateUserForm, ProfileUpdateForm
from .models import Dog, News, Profile
from django.conf import settings
import os


# Location of the default User profile picture if they don't have a picture
DEFAULT_IMAGE_SOURCE = '/profile_pictures/default.jpg'


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
                    return redirect('home')
                else:
                    # Username exists but password was incorrect
                    messages.error(request, message='The password is incorrect. Please try again...')
                    return redirect('home')
            except Exception as e:
                messages.error(request, message=f'An error occurred during login: {e}')
                return redirect('home')
        else:
            # Username does not exist
            messages.error(request, message='The username does not exist. Please try again...')
            return redirect('home')
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
    return redirect('home')


# User Registration view for new users
def register_user_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            # Add User to the Regulars Group
            regulars_group = Group.objects.get(name="Regular")
            user.groups.add(regulars_group)

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
            return redirect('home')
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
            return redirect('home')
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
        return redirect('home')
    return render(request, 'add_news.html')


# Dog record page, displays the details for a single dog
# Takes in the dog's PK
def dog_record_view(request, pk):
    # Check if the user is logged in
    if request.user.is_authenticated:
        # Look up and save the dog's record
        dog_record = Dog.objects.get(dogID=pk)
        return render(request, 'dog_record.html', {'dog_record': dog_record})

    # User is NOT logged in --> send them to login page
    else:
        messages.error(request, message='You Must Be Logged In To View That Page...')
        return redirect('home')


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
            return redirect('home')
        # User clicked "Delete" button to confirm deletion
        return render(request, 'delete_dog.html', {'dog': delete_dog})
    # User not logged in, must login first
    else:
        messages.error(request, 'You must be logged in to do that...')
        return redirect('home')


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
                return redirect('home')
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
        return redirect('home')


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
            return redirect('dog_record', pk=current_dog.dogID)
        return render(request, 'update_dog.html', {'form': form, 'current_dogID': current_dog.dogID})

    # User is not logged in, redirect them to login
    else:
        messages.error(request, "You must be logged in to do that...")
        return redirect('home')


# Display all users for the admins only in view_users.html
# Check user is logged in
@login_required
# Check user is Admin
@user_passes_test(lambda u: u.is_superuser)
def view_users(request):
    # Retrieve all the users in the system, prefetch their groups, and select their profiles
    users = User.objects.all().prefetch_related('groups').select_related('profile')
    # Fetch each user's Status (E.g: "Admin", "Vet" or "Regular")
    for user in users:
        user.role = get_user_role(user)
    # pass all users on to viewers_users.html
    return render(request, 'view_users.html', {'users': users})


# Takes in a User, returns their ranking.
# Used in view_users and update_user to determine User Status
def get_user_role(user):
    if user.is_superuser:
        return "Admin"
    elif user.groups.filter(name="Vet").exists():
        return "Vet"
    elif user.groups.filter(name="Regular").exists():
        return "Regular"
    else:
        return ""


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
            return redirect('view_users')
        # User clicked "Delete" button to confirm deletion
        return render(request, 'delete_user.html', {'delete_user': delete_user})
    # User not logged in, must login first
    else:
        messages.error(request, message='You must be logged in to do that...')
        return redirect('home')


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
            messages.success(request, f"{user_to_update.first_name} {user_to_update.last_name}'s Picture Has Been Removed Successfully!")
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
            return redirect('view_users')
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
        return redirect('home')


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
                return redirect('update_user_self')
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
        return redirect('home')


# Page for editing the news from the homepage. Only visible to Admins
@user_passes_test(lambda u: u.is_superuser)
def update_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    if request.method == 'POST':
        news.title = request.POST['title']
        news.content = request.POST['content']
        news.save()
        messages.success(request, f"News Story: '{request.POST['title']}' has been successfully edited...")
        return redirect('home')
    return render(request, 'update_news.html', {'news': news})


# View for deleting a News story from the homepage. Only available to Admins
@user_passes_test(lambda u: u.is_superuser)
def delete_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    if request.method == 'POST':
        news_title = news.title
        news.delete()
        messages.success(request, f"News Story: '{news_title}' has been successfully deleted...")
        return redirect('home')
    return render(request, 'delete_news.html', {'news': news})
