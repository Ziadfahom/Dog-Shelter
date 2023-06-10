from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import SignUpForm, AddDogForm
from .models import Dog


# Main Page view for displaying either dog records if  user is logged in,
# or a login page if user is logged out
def home_view(request):
    # Get all the dog records in the database
    all_dogs = Dog.objects.all().order_by('-dateOfArrival')

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
        return render(request, 'home.html', {"dogs": all_dogs})


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
            form.save()

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


