from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import SignUpForm, AddDogForm, UpdateUserForm
from .models import Dog, News


# Main Page view for displaying either dog records if  user is logged in,
# or a login page if user is logged out
def home_view(request):
    # Get all the dog records in the database
    all_dogs = Dog.objects.all().order_by('-dateOfArrival')

    # Get the total number of dogs
    total_dogs = Dog.objects.count()

    # Get the number of dogs that have received toy treatments
    toy_treatment_dogs = Dog.objects.filter(observation__isKong='Y').distinct().count()

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
        context = {
            'dogs': all_dogs,
            'total_dogs': total_dogs,
            'toy_treatment_dogs': toy_treatment_dogs,
            'news_items': news_items
        }
        return render(request, 'home.html', context=context)


# Logout Users view for displaying a user-logout option if they're already logged in
def logout_user_view(request):
    logout(request)
    messages.success(request, message='You have been logged out..')
    return redirect('home')


# User Registration view for new users
def register_user_view(request):

    # Check if the request is a POST request
    # (indicating that the user is submitting the form)
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        # Validate the data and see if it meets all the conditions
        if form.is_valid():
            user = form.save()

            # Add User to the Regulars Group
            regulars_group = Group.objects.get(name="Regular")
            user.groups.add(regulars_group)

            # Authenticate the user by verifying their credentials
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)

            # Login the user and display success message
            login(request, user)
            messages.success(request, f"Welcome, {username} and thank you for signing up! "
                                      "You're now a member of our Dogs Shelter community.")
            return redirect('home')

        # If the form data is invalid, display an error message
        else:
            return render(request, 'register.html', {'form': form})

    # If it's a GET request (indicating the user
    # wants to see the form), create a blank form
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})


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


def delete_dog_view(request, pk):
    # Check if the user is logged in
    if request.user.is_authenticated:
        # Check if the user has the right permissions
        if not request.user.has_perm('dogs_app.delete_dog'):
            raise PermissionDenied
        
        delete_dog = Dog.objects.get(dogID=pk)
        dog_name = delete_dog.dogName
        delete_dog.delete()
        messages.success(request, message=f'{dog_name} Has Been Deleted Successfully...')
        return redirect('home')
    else:
        messages.error(request, message='You must be logged in to do that...')
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
            form = AddDogForm(request.POST)
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


def update_dog_view(request, pk):
    # Check if user is logged in
    if request.user.is_authenticated:
        # Check if the user has the right permissions to edit dogs
        if not request.user.has_perm('dogs_app.change_dog'):
            raise PermissionDenied

        # Grab the Dog record
        current_dog = Dog.objects.get(dogID=pk)
        form = AddDogForm(request.POST or None, instance=current_dog)
        if form.is_valid():
            form.save()
            messages.success(request, f"{current_dog.dogName}'s Details Have Been Updated Successfully!")
            return redirect('home')
        # If request is not POST (i.e., GET), just render the form
        else:
            return render(request, 'update_dog.html', {'form': form})
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
    # Retrieve all the users in the system
    users = User.objects.all().prefetch_related('groups')
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
        delete_user = User.objects.get(pk=pk)
        user_name = delete_user.username
        delete_user.delete()
        messages.success(request, message=f'{user_name} Has Been Deleted Successfully...')
        return redirect('view_users')
    else:
        messages.error(request, message='You must be logged in to do that...')
        return redirect('home')


# Check user is Admin
@user_passes_test(lambda u: u.is_superuser)
def update_user_view(request, pk):
    # Check if user is logged in
    if request.user.is_authenticated:
        current_user = User.objects.get(pk=pk)
        initial = {'role': get_user_role(current_user)}
        form = UpdateUserForm(request.POST or None, instance=current_user, initial=initial, request_user=request.user)
        if form.is_valid():
            # Save form without committing (we'll modify the user before saving)
            user = form.save(commit=False)
            role = form.cleaned_data['role']
            # If the group name is not empty
            if role:
                # If group name is Admin, update is_superuser status and clear other groups
                if role == 'Admin':
                    user.is_superuser = True
                    user.is_staff = True
                    current_user.groups.clear()
                else:
                    # For other groups, get the chosen group
                    chosen_group = Group.objects.get(name=role)
                    # Remove the user from all the other groups
                    current_user.groups.clear()
                    # Add the user to the chosen group
                    current_user.groups.add(chosen_group)
                    # Update user's is_superuser status
                    user.is_superuser = False
                    user.is_staff = False

            # Now commit the save
            user.save()
            messages.success(request, f"{current_user.first_name} {current_user.last_name}'s Details"
                                      f" Have Been Updated Successfully!")
            return redirect('view_users')
        else:
            return render(request, 'update_user.html', {'form': form})
    # User is not logged in, redirect them to login
    else:
        messages.error(request, "You must be logged in to do that...")
        return redirect('home')


# Only logged-in users permitted
@login_required
def update_user_self_view(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(pk=request.user.pk)
        initial = {'role': get_user_role(current_user)}
        form = UpdateUserForm(request.POST or None, instance=current_user, initial=initial, request_user=request.user)
        if form.is_valid():
            # Save form without committing (we'll modify the user before saving)
            user = form.save()
            messages.success(request, f"Your Details Have Been Updated Successfully!")
            return redirect('update_user_self')
        else:
            return render(request, 'update_user.html', {'form': form})
    # User is not logged in, redirect them to login
    else:
        messages.error(request, "You must be logged in to do that...")
        return redirect('home')