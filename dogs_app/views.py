from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages


# Main Page view for displaying either dog records if  user is logged in,
# or a login page if user is logged out
def home_view(request):
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
        return render(request, 'home.html', {})


# Logout Users view for displaying a user-logout option if they're already logged in
def logout_user_view(request):
    logout(request)
    messages.success(request, message='You have been logged out..')
    return redirect('home')

def register_user_view(request):
    return render(request, 'register.html', {})
