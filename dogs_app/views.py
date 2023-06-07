from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import SignUpForm
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
        User = get_user_model()

        # Check if username exists
        if User.objects.filter(username=username).exists():

            # Authenticate
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user=user)
                messages.success(request, message='You have successfully logged in!')
                return redirect('home')
            else:

                # Username exists but password was incorrect
                messages.error(request, message='The password is incorrect. Please try again...')
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
            messages.success(request, "Welcome and thank you for signing up! "
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
