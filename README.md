
# Dog-Shelter
Getting Started:

We recommend creating a Python virtual environment for this project to avoid conflicts with packages in your global Python environment. You can create a virtual environment using the following command:

python -m venv venv

Then, activate it with the following command:

``source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows``

After setting up and activating the virtual environment, you can install the required packages. We have listed them at the bottom under "Manual Installations", or you can simply run this command to install the necessary packages:

pip install -r requirements.txt

The requirements.txt is a list of the packages and versions we used. It was automatically generated using "pip freeze > requirements.txt".

**Make sure you also run the following command to install python-decouple, in case Environment Variables for passwords/keys don't work correctly:**

**pip install python-decouple**



After downloading the packages, you will need to set up a .env file with the necessary environment variables for your database and AWS (if in production mode) like this (place this code inside a file named '.env' with your Database details):

DATABASE_NAME=

DATABASE_USER=

DATABASE_PASSWORD=

DATABASE_HOST=

DATABASE_PORT=

These variables are used in settings.py to set up the connection to the MySQL Database, and appear in Django's settings.py as follows:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
    }
}



The AWS S3 settings are also configured via environment variables in the settings.py like below, but you can leave these as they are for now. They will only come into play once the project moves from the Development stage to the Production stage, when DEBUG is set to False. Currently, during the Development stage, images, videos, and JSON files are all stored locally inside the project files:

if not DEBUG:
    # AWS S3 settings
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')




Once the environment variables are set and the packages are installed, you can run the migrations for the database:

python manage.py migrate

Now, you should be ready to run the server:

python manage.py runserver



----------------------------------------
Manual Installations (optional):
----------------------------------------
pip install Django

pip install mysql

pip install mysql-connector-python

pip install mysql-connector

pip install django-widget-tweaks

pip install django-storages boto3

pip install python-decouple           #For hiding environmental variables such as Amazon Access Key

pip install pillow		                #For managing locally saved images/videos/files when DEBUG=True

pip install django-crispy-forms	      #Better looking forms

pip install crispy-bootstrap5


pip install django-imagekit           #Handling image thumbnails for smaller-sized dog images

pip install sorl-thumbnail	          #Handling thumbnails

pip install django-extensions 	      #Used for resetting DB



____________________
----------------------------------------
Running the Website:
----------------------------------------
python manage.py runserver
