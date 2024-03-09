import pytz
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
from django import forms
from .models import (Dog, Owner, Profile, Treatment, EntranceExamination,
                     Observation, DogPlacement, Kennel, Observes, DogStance, News, Camera, Branch)
from django.core.exceptions import ValidationError
from datetime import date
from django.utils.dateparse import parse_datetime
from django import forms
from .models import Choice, Poll
from django.forms import inlineformset_factory



# Helper function to get the user's current branch object (Israel/Italy)
def get_current_branch(request):
    # Get the current Branch (Israel/Italy)
    branch_name = request.session.get('branch', 'Israel')  # Default to Israel
    branch = Branch.objects.get(branchName=branch_name)  # Get the branch object

    return branch


# New User Registration Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # Exclude 'branch' from the form (automatically set based on current user's branch)
        exclude = ['branch']


class SignUpForm(UserCreationForm):

    # Input fields
    email = forms.EmailField(label='')
    first_name = forms.CharField(label='', max_length=50)
    last_name = forms.CharField(label='', max_length=50,)

    # Defining a user in the system
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    # # Setting up the 'Username', 'Password' and 'Confirm Password' fields
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = 'User Name'
        self.fields['username'].help_text = '(only letters, numbers, and underscores)'

        self.fields['password1'].label = 'Password'
        self.fields['password1'].help_text = '(min. 8 char)'

        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].help_text = '(enter the same password as before.)'

        self.fields['email'].label = 'Email Address'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'


# Add New Dog Form
class AddDogForm(forms.ModelForm):
    dogName = forms.CharField(required=True,
                              max_length=35,
                              error_messages={'required': 'Dog Name cannot be empty'},
                              widget=forms.widgets.TextInput(attrs={"class": "form-control",
                                                                    "required": "required",
                                                                    "title": "Please enter a dog name"}),
                              label="Dog Name")
    chipNum = forms.CharField(required=False,
                              max_length=30,
                              validators=[RegexValidator(r'^[0-9]*$',
                                                         'Chip Number can only have numbers')],
                              widget=forms.widgets.TextInput(attrs={"class": "form-control",
                                                                    "title": "Please enter a valid chip number"}),
                              label="Chip Number")
    dateOfBirthEst = forms.DateField(required=False,
                                     widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                    attrs={"type": "date",
                                                                           "class": "form-control",
                                                                           "title": "Please enter a valid date"}),
                                     label="Estimated Date of Birth")
    # Set the initial value to today's date adjusted for Jerusalem timezone
    dateOfArrival = forms.DateField(required=False,
                                    initial=timezone.localtime(timezone.now()).date(),
                                    widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                   attrs={"type": "date",
                                                                          "class": "form-control",
                                                                          "title": "Please enter a valid date"}),
                                    label="Date of Arrival")
    dateOfVaccination = forms.DateField(required=False,
                                        widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                       attrs={"type": "date",
                                                                              "class": "form-control",
                                                                              "title": "Please enter a valid date"}),
                                        label="Date of Vaccination")
    breed = forms.CharField(required=False,
                            max_length=30,
                            widget=forms.widgets.TextInput(attrs={"class": "form-control",
                                                                  "title": "Please enter a breed",
                                                                  "maxlength": 30}),
                            label="Breed")
    gender = forms.ChoiceField(choices=Dog.GENDER_CHOICES,
                               required=False,
                               widget=forms.widgets.Select(attrs={"class": "form-control",
                                                                  "title": "Please select the dog's gender"}),
                               label="Gender")
    furColor = forms.CharField(required=False,
                               max_length=20,
                               widget=forms.widgets.TextInput(attrs={"class": "form-control",
                                                                     "title": "Please enter the dog's fur color",
                                                                     "maxlength": 20}),
                               label="Fur Color")
    isNeutered = forms.ChoiceField(choices=Dog.IS_NEUTERED_CHOICES,
                                   required=False,
                                   widget=forms.widgets.Select(attrs={"class": "form-control",
                                                                      "title": "Select if the dog is neutered"}),
                                   label="Is the dog neutered?")
    isDangerous = forms.ChoiceField(choices=Dog.IS_DANGEROUS_CHOICES,
                                    required=False,
                                    widget=forms.widgets.Select(attrs={"class": "form-control",
                                                                       "title": "Select if the dog is dangerous"}),
                                    label="Is the dog dangerous?")
    dogImage = forms.ImageField(required=False,
                                widget=forms.widgets.ClearableFileInput(attrs={"class": "form-control",
                                                                               "title": "Upload the dog's image."}),
                                label="Dog Image",
                                help_text="Upload the dog's image here.")
    owner = forms.ModelChoiceField(queryset=Owner.objects.none(),  # Initially empty queryset
                                   required=False,
                                   widget=forms.widgets.Select(attrs={"class": "form-control",
                                                                      "title": "Select the dog's owner"}),
                                   label="Dog's Owner")
    adoptionDate = forms.DateField(required=False,
                                   widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                  attrs={"type": "date",
                                                                         "class": "form-control",
                                                                         "title": "Please enter a valid date",
                                                                         "id": "id_adoptionDate"}),
                                   label="Adoption Date")

    class Meta:
        model = Dog
        exclude = ['branch', 'dogID', 'kongDateAdded']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Extract the request object
        super(AddDogForm, self).__init__(*args, **kwargs)
        # Add a 'date-field' CSS class to date fields for easy targeting in JavaScript
        self.fields['dateOfArrival'].widget.attrs.update({'class': 'date-field'})
        self.fields['dateOfBirthEst'].widget.attrs.update({'class': 'date-field'})
        self.fields['dateOfVaccination'].widget.attrs.update({'class': 'date-field'})
        if request:
            # Get the current branch
            current_branch = get_current_branch(request)
            # Set the queryset to the current branch's owners
            self.fields['owner'].queryset = Owner.objects.filter(branch=current_branch)

    def clean_dateOfBirthEst(self):
        dob = self.cleaned_data.get('dateOfBirthEst')
        if dob and dob > date.today():
            raise ValidationError('Estimated Date of Birth cannot be a future date')
        return dob


# Form for update users
class UpdateUserForm(UserChangeForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'required': 'required',
                                                           'title': 'Please enter a valid email address'}))
    first_name = forms.CharField(max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'required': 'required',
                                                               'title': 'Please enter a first name'}))
    last_name = forms.CharField(max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'required': 'required',
                                                              'title': 'Please enter a last name'}))
    # For displaying User Status (ranking)
    ROLE_CHOICES = [
        ('Viewer', 'Viewer'),
        ('Vet', 'Vet'),
        ('Admin', 'Admin'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES,
                             required=False,
                             widget=forms.Select(attrs={'class': 'form-control',
                                                        'title': 'Please select a role'}),
                             label="Role")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role')

    # Admins can't change their own role to "Vet" or "Viewer"
    # They can only change other admins
    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)

        # Takes in a User, returns their current role.
        def get_user_role(user):
            if user.is_superuser:
                return "Admin"
            elif user.groups.filter(name="Vet").exists():
                return "Vet"
            elif user.groups.filter(name="Viewer").exists():
                return "Viewer"
            else:
                return ""

        # If the instance user (i.e., the user being edited) is the same as the
        # currently logged-in user, then roles should not be possible to edit.
        if self.instance == self.request_user:
            # Check if the user is Admin
            if self.request_user.is_superuser:
                # Only give them the option to choose "Admin"
                self.fields['role'].choices = [('Admin', 'Admin')]
            else:
                # Not an admin --> then give them the option to only choose their current role
                current_role = get_user_role(self.request_user)
                if current_role == 'Vet':
                    self.fields['role'].choices = [('Vet', 'Vet')]
                elif current_role == 'Viewer':
                    self.fields['role'].choices = [('Viewer', 'Viewer')]


# Add more attributes to User profiles
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'image']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control',
                                                   'title': 'Please enter a valid phone number'}),
            'address': forms.TextInput(attrs={'class': 'form-control',
                                              'title': 'Please enter an address',
                                              'maxlength': 100}),
            'image': forms.FileInput()
        }


# Form for adding new Treatments
class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ['treatmentName', 'treatmentDate', 'treatedBy', 'comments']
        labels = {
            'treatmentName': 'Treatment Name',
            'treatmentDate': 'Treatment Date',
            'treatedBy': 'Treated By',
            'comments': 'Comments',
        }
        widgets = {
            'treatmentName': forms.TextInput(attrs={'class': 'form-control',
                                                    'maxlength': 50,
                                                    'title': 'Please enter a maximum of 50 characters',
                                                    'required': 'required'}),
            'treatmentDate': forms.DateInput(attrs={'class': 'form-control',
                                                    'type': 'text',
                                                    'data-provide': 'datepicker',
                                                    'readonly': 'readonly',
                                                    'title': 'Please enter a valid date'}),
            'treatedBy': forms.TextInput(attrs={'class': 'form-control',
                                                'maxlength': 50,
                                                'title': 'Please enter a maximum of 50 characters',
                                                'required': 'required'}),
            'comments': forms.Textarea(attrs={'class': 'form-control',
                                              'maxlength': 250,
                                              'title': 'Please enter a maximum of 250 characters',
                                              'rows': 5}),
        }


# Form for adding new Examinations
class EntranceExaminationForm(forms.ModelForm):
    class Meta:
        model = EntranceExamination
        fields = ['examinationDate', 'examinedBy', 'results', 'dogWeight', 'dogTemperature', 'dogPulse', 'comments']
        labels = {
            'examinationDate': 'Examination Date',
            'examinedBy': 'Examined By',
            'results': 'Results',
            'dogWeight': 'Dog Weight',
            'dogTemperature': 'Dog Temperature',
            'dogPulse': 'Dog Pulse',
            'comments': 'Comments',
        }
        widgets = {
            'examinationDate': forms.DateInput(attrs={'class': 'form-control',
                                                      'type': 'text',
                                                      'data-provide': 'datepicker',
                                                      'readonly': 'readonly',
                                                      'required': 'required',
                                                      'title': 'Please enter a valid date'}),
            'examinedBy': forms.TextInput(attrs={'class': 'form-control',
                                                 'maxlength': 50,
                                                 'title': 'Please enter a maximum of 50 characters',
                                                 'required': 'required'}),
            'results': forms.Textarea(attrs={'class': 'form-control',
                                             'maxlength': 150,
                                             'rows': 3,
                                             'title': 'Please enter a maximum of 150 characters'}),
            'dogWeight': forms.NumberInput(attrs={'class': 'form-control',
                                                  'placeholder': '0-250',
                                                  'min': 0,
                                                  'max': 250,
                                                  'step': 1,
                                                  'title': 'Please enter a number'}),
            'dogTemperature': forms.NumberInput(attrs={'class': 'form-control',
                                                       'placeholder': '0-250',
                                                       'min': 0,
                                                       'max': 250,
                                                       'step': 1,
                                                       'title': 'Please enter a number'}),
            'dogPulse': forms.NumberInput(attrs={'class': 'form-control',
                                                 'placeholder': '0-250',
                                                 'min': 0,
                                                 'max': 250,
                                                 'step': 1,
                                                 'title': 'Please enter a number'}),
            'comments': forms.Textarea(attrs={'class': 'form-control',
                                              'rows': 5,
                                              'maxlength': 250,
                                              'title': 'Please enter a maximum of 250 characters'}),
        }


# Form for adding new Owner
class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['firstName', 'lastName', 'ownerID', 'ownerAddress', 'city', 'phoneNum', 'cellphoneNum', 'comments']
        labels = {
            'firstName': 'First Name',
            'lastName': 'Last Name',
            'ownerID': 'Owner ID',
            'ownerAddress': 'Owner Address',
            'city': 'City',
            'phoneNum': 'Phone Number',
            'cellphoneNum': 'Cellphone Number',
            'comments': 'Comments',
        }
        widgets = {
            'firstName': forms.TextInput(attrs={'class': 'form-control',
                                                'required': 'required',
                                                'title': 'Please enter a first name',
                                                'maxlength': 50}),
            'lastName': forms.TextInput(attrs={'class': 'form-control',
                                               'title': 'Please enter a last name',
                                               'maxlength': 50}),
            'ownerID': forms.TextInput(attrs={'class': 'form-control',
                                              'maxlength': 9,
                                              'title': 'Please enter a maximum of 9 letters'}),
            'ownerAddress': forms.TextInput(attrs={'class': 'form-control',
                                                   'title': 'Please enter an address',
                                                   'maxlength': 100}),
            'city': forms.TextInput(attrs={'class': 'form-control',
                                           'title': 'Please enter a city',
                                           'maxlength': 50}),
            'phoneNum': forms.TextInput(attrs={'class': 'form-control',
                                               'title': 'Please enter a phone number',
                                               'maxlength': 9}),
            'cellphoneNum': forms.TextInput(attrs={'class': 'form-control',
                                                   'title': 'Please enter a cellphone number',
                                                   'maxlength': 10}),
            'comments': forms.Textarea(attrs={'class': 'form-control',
                                              'rows': 5,
                                              'title': 'Please enter a maximum of 250 characters',
                                              'maxlength': 250}),
        }


# Form for Camera
class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ['camID']

        widgets = {
            'camID': forms.TextInput(attrs={'class': 'form-control',
                                            'required': 'required',
                                            'title': 'Please enter a camera ID'}),
        }


# Form for adding new Kennel
class KennelForm(forms.ModelForm):
    kennelNum = forms.CharField(required=True,
                                error_messages={'required': 'Kennel Number cannot be empty'},
                                widget=forms.widgets.TextInput(attrs={"class": "form-control",
                                                                      "required": "required",
                                                                      "title": "Please enter a kennel number"}),
                                label="Kennel Number")
    kennelImage = forms.ImageField(required=False,
                                   widget=forms.widgets.ClearableFileInput(attrs={"class": "form-control",
                                                                                  "title": "Upload the kennel's image"}),
                                   label="Kennel Image")

    class Meta:
        model = Kennel
        exclude = ['branch']


# Form for editing a Kennel
class KennelEditForm(forms.ModelForm):
    # Disable editing Kennel Number
    kennelNum = forms.CharField(required=True,
                                error_messages={'required': 'Kennel Number cannot be empty'},
                                widget=forms.widgets.TextInput(attrs={"class": "form-control",
                                                                      "required": "required",
                                                                      "title": "Please enter a kennel number",
                                                                      "readonly": "readonly"}),
                                label="Kennel Number")
    kennelImage = forms.ImageField(required=False,
                                   widget=forms.widgets.ClearableFileInput(attrs={"class": "form-control",
                                                                                  "title": "Upload the kennel's image"}),
                                   label="Kennel Image")

    class Meta:
        model = Kennel
        exclude = ['branch']


# Form for adding new Dog Placements (in Kennels)
class DogPlacementForm(forms.ModelForm):
    class Meta:
        model = DogPlacement
        fields = ['kennel', 'entranceDate', 'expirationDate', 'placementReason']
        labels = {
            'kennel': 'kennel',
            'entranceDate': 'Entrance Date',
            'expirationDate': 'Expiration Date',
            'placementReason': 'Placement Reason',
        }
        widgets = {
            'kennel': forms.Select(attrs={'class': 'form-control',
                                          'required': 'required',
                                          'title': 'Please select a kennel'}),
            'entranceDate': forms.DateInput(attrs={'class': 'form-control',
                                                   'type': 'text',
                                                   'data-provide': 'datepicker',
                                                   'readonly': 'readonly',
                                                   'title': 'Please enter a valid date',
                                                   'required': 'required'}),
            'expirationDate': forms.DateInput(attrs={'class': 'form-control',
                                                     'type': 'text',
                                                     'data-provide': 'datepicker',
                                                     'readonly': 'readonly',
                                                     'title': 'Please enter a valid date',}),
            'placementReason': forms.Textarea(attrs={'class': 'form-control',
                                                     'title': 'Please enter a maximum of 75 characters',
                                                     'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(DogPlacementForm, self).__init__(*args, **kwargs)
        if request:
            # Get the current branch
            current_branch = get_current_branch(request)
            # Set the queryset to the current branch's kennels
            self.fields['kennel'].queryset = Kennel.objects.filter(branch=current_branch)

    def clean(self):
        # Make sure expiration date is after entrance date
        cleaned_data = super().clean()
        entrance_date = cleaned_data.get('entranceDate')
        expiration_date = cleaned_data.get('expirationDate')
        if entrance_date and expiration_date and entrance_date > expiration_date:
            raise forms.ValidationError("Expiration Date must be after the Entrance Date")



# Form for adding new Camera Session (Observes)
class ObservesForm(forms.ModelForm):
    class Meta:
        model = Observes
        fields = ['sessionDate', 'camera', 'comments']
        labels = {
            'camera': "Camera",
            'comments': "Comments",
            'sessionDate': 'Session Date'
        }
        widgets = {
            'sessionDate': forms.DateInput(attrs={'class': 'form-control',
                                                  'type': 'text',
                                                  'data-provide': 'datepicker',
                                                  'readonly': 'readonly',
                                                  'title': 'Please enter a valid date',}),
            'camera': forms.Select(attrs={'class': 'form-control',
                                          'required': 'required',
                                          'title': 'Please select a camera'}),
            'comments': forms.Textarea(attrs={'class': 'form-control',
                                              'title': 'Please enter a maximum of 200 characters',
                                              'rows': 5})
        }

    def clean_camera(self):
        camera = self.cleaned_data['camera']
        if not camera:
            raise forms.ValidationError("A camera must be selected.")
        return camera

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(ObservesForm, self).__init__(*args, **kwargs)
        if request:
            # Get the current branch
            current_branch = get_current_branch(request)
            # Set the queryset to the current branch's cameras
            self.fields['camera'].queryset = Camera.objects.filter(branch=current_branch)


# Form for adding new Observation
class ObservationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(ObservationForm, self).__init__(*args, **kwargs)
        if request:
            # Get the current branch
            current_branch = get_current_branch(request)

            # If the current branch is not Italy, then exclude the isDog and isHuman fields
            if current_branch.branchName != "Italy":
                self.fields.pop('isDog')
                self.fields.pop('isHuman')

    class Meta:
        model = Observation
        fields = ['obsDateTime', 'sessionDurationInMins', 'isKong', 'isDog', 'isHuman', 'jsonFile', 'rawVideo']
        widgets = {
            'sessionDurationInMins': forms.NumberInput(attrs={'class': 'form-control',
                                                              'title': 'Please enter a duration (in minutes)',}),
            'isKong': forms.Select(choices=Observation.IS_KONG_CHOICES, attrs={'class': 'form-control',
                                                                               'title': 'Select if the dog is with a '
                                                                                        'Kong',
                                                                               'required': 'required'}),
            'isDog': forms.Select(choices=Observation.IS_DOG_CHOICES, attrs={'class': 'form-control',
                                                                             'title': 'Select if the dog is with '
                                                                                      'another dog',
                                                                             'required': 'required'}),
            'isHuman': forms.Select(choices=Observation.IS_HUMAN_CHOICES, attrs={'class': 'form-control',
                                                                                 'title': 'Select if the dog is with '
                                                                                          'a human',
                                                                                 'required': 'required'}),
            'jsonFile': forms.FileInput(attrs={'class': 'form-control-file'}),
            'rawVideo': forms.FileInput(attrs={'class': 'form-control-file'})
        }



# Form for adding new Dog Stance
class DogStanceForm(forms.ModelForm):
    class Meta:
        model = DogStance
        fields = ['stanceStartTime', 'dogStance', 'dogLocation']

        widgets = {
            'stanceStartTime': forms.TimeInput(attrs={'class': 'form-control',
                                                      'type': 'text',
                                                      'title': 'Please enter a valid time',
                                                      'required': 'required'}),
            'dogStance': forms.Select(attrs={'class': 'form-control',
                                             'title': 'Please select a stance',
                                             'required': 'required'}),
            'dogLocation': forms.Select(attrs={'class': 'form-control',
                                               'title': 'Please select a location'}),
        }


# Form for Treatments in Portal
class TreatmentPortalForm(forms.ModelForm):
    treatmentName = forms.CharField(required=True,
                                    max_length=50,
                                    error_messages={'required': 'Treatment Name cannot be empty'},
                                    widget=forms.widgets.TextInput(attrs={"class": "form-control",
                                                                          "required": "required",
                                                                          "title": "Please enter a treatment name"}),
                                    label="Treatment Name")
    treatmentDate = forms.DateField(required=False,
                                    widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                   attrs={"type": "date",
                                                                          "class": "form-control",
                                                                          "title": "Please enter a valid date"}),
                                    label="Date of Treatment",
                                    initial=timezone.localtime(timezone.now()).date())
    treatedBy = forms.CharField(required=True,
                                max_length=50,
                                error_messages={'required': '"Treated By" cannot be empty'},
                                widget=forms.widgets.TextInput(attrs={"class": "form-control",
                                                                      "required": "required",
                                                                      "title": "Please enter a name",
                                                                      "maxlength": 50}),
                                label="Treated By")
    comments = forms.CharField(required=False,
                               max_length=250,
                               widget=forms.widgets.Textarea(attrs={"class": "form-control",
                                                                    "title": "Please enter a maximum of 250 characters",
                                                                    "rows": 5}),
                               label="Comments")
    dog = forms.ModelChoiceField(queryset=Dog.objects.none(),
                                 error_messages={'required': 'Dog cannot be empty'},
                                 required=True,
                                 widget=forms.widgets.Select(attrs={"class": "form-control",
                                                                    "title": "Please select a dog",
                                                                    "required": "required"}),
                                 label="Dog")

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(TreatmentPortalForm, self).__init__(*args, **kwargs)
        if request:
            # Get the current branch
            current_branch = get_current_branch(request)
            # Set the queryset to the current branch's dogs
            self.fields['dog'].queryset = Dog.objects.filter(branch=current_branch).order_by('dogName')

    class Meta:
        model = Treatment
        fields = ['dog', 'treatmentName', 'treatmentDate', 'treatedBy', 'comments']


# Form for Examinations in Portal
class ExaminationPortalForm(forms.ModelForm):
    examinationDate = forms.DateField(required=True,
                                      error_messages={'required': 'Examination Date cannot be empty'},
                                      widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                     attrs={"type": "date",
                                                                            "required": "required",
                                                                            "title": "Please enter a valid date",
                                                                            "class": "form-control"}),
                                      label="Date of Examination",
                                      initial=timezone.localtime(timezone.now()).date())
    examinedBy = forms.CharField(required=True,
                                 max_length=50,
                                 error_messages={'required': 'Examined By cannot be empty'},
                                 widget=forms.widgets.TextInput(attrs={"class": "form-control",
                                                                       "required": "required",
                                                                       "title": "Please enter name of examiner",
                                                                       "maxlength": 50}),
                                 label="Examined By")
    results = forms.CharField(required=False,
                              max_length=100,
                              widget=forms.widgets.Textarea(attrs={"class": "form-control",
                                                                   "title": "Please enter a maximum of 100 characters",
                                                                   "rows": 3}),
                              label="Results")
    dogWeight = forms.DecimalField(required=False,
                                   widget=forms.widgets.NumberInput(attrs={"class": "form-control",
                                                                           "min": 0,
                                                                           "max": 250,
                                                                           "title": "Please enter the dog's weight"}),
                                   label="Weight")
    dogTemperature = forms.DecimalField(required=False,
                                        widget=forms.widgets.NumberInput(attrs={"class": "form-control",
                                                                                "min": 0,
                                                                                "max": 250,
                                                                                "title": "Please enter the dog's temperature"}),
                                        label="Temperature")
    dogPulse = forms.DecimalField(required=False,
                                  widget=forms.widgets.NumberInput(attrs={"class": "form-control",
                                                                          "min": 0,
                                                                          "max": 250,
                                                                          "title": "Please enter the dog's pulse"}),
                                  label="Pulse")
    comments = forms.CharField(required=False,
                               max_length=250,
                               widget=forms.widgets.Textarea(attrs={"class": "form-control",
                                                                    "title": "Please enter a maximum of 250 characters",
                                                                    "rows": 5}),
                               label="Comments")
    dog = forms.ModelChoiceField(queryset=Dog.objects.none(),
                                 error_messages={'required': 'Dog cannot be empty'},
                                 required=True,
                                 widget=forms.widgets.Select(attrs={"class": "form-control",
                                                                    "title": "Please select a dog",
                                                                    "required": "required"}),
                                 label="Dog")

    class Meta:
        model = EntranceExamination
        fields = ['dog', 'examinationDate', 'examinedBy', 'results',
                  'dogWeight', 'dogTemperature', 'dogPulse', 'comments']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(ExaminationPortalForm, self).__init__(*args, **kwargs)
        if request:
            # Get the current branch
            current_branch = get_current_branch(request)
            # Set the queryset to the current branch's dogs
            self.fields['dog'].queryset = Dog.objects.filter(branch=current_branch).order_by('dogName')


# Dog Placement Form in Portal
class PlacementPortalForm(forms.ModelForm):
    dog = forms.ModelChoiceField(queryset=Dog.objects.none(),
                                 required=True,
                                 error_messages={'required': 'Dog cannot be empty'},
                                 widget=forms.widgets.Select(attrs={"class": "form-control",
                                                                    "title": "Please select a dog",}),
                                 label="Dog")
    kennel = forms.ModelChoiceField(queryset=Kennel.objects.none(),
                                    required=True,
                                    error_messages={'required': 'Kennel cannot be empty'},
                                    widget=forms.widgets.Select(attrs={"class": "form-control",
                                                                       "title": "Please select a kennel"}),
                                    label="Kennel")
    entranceDate = forms.DateField(required=True,
                                   error_messages={'required': 'Entrance Date cannot be empty'},
                                   widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                  attrs={"type": "date",
                                                                         "class": "form-control",
                                                                         "title": "Please enter a valid date"}),
                                   label="Date of Entrance",
                                   initial=timezone.localtime(timezone.now()).date())
    expirationDate = forms.DateField(required=False,
                                     widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                    attrs={"type": "date",
                                                                           "class": "form-control",
                                                                           "title": "Please enter a valid date"}),
                                     label="Date of Expiration")
    placementReason = forms.CharField(required=False,
                                      max_length=75,
                                      widget=forms.widgets.Textarea(attrs={"class": "form-control",
                                                                           "title": "Please enter a maximum of 75 characters",
                                                                           "rows": 4}),
                                      label="Placement Reason")

    class Meta:
        model = DogPlacement
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(PlacementPortalForm, self).__init__(*args, **kwargs)
        if request:
            # Get the current branch
            current_branch = get_current_branch(request)
            # Set the queryset to the current branch's kennels and dogs
            self.fields['kennel'].queryset = Kennel.objects.filter(branch=current_branch)
            self.fields['dog'].queryset = Dog.objects.filter(branch=current_branch)


# Session (Observes) Form in Portal
class ObservesPortalForm(forms.ModelForm):
    dog = forms.ModelChoiceField(queryset=Dog.objects.none(),
                                 required=True,
                                 error_messages={'required': 'Dog cannot be empty'},
                                 widget=forms.widgets.Select(attrs={"class": "form-control",
                                                                    "title": "Please select a dog",
                                                                    "required": "required"}),
                                 label="Dog")
    camera = forms.ModelChoiceField(queryset=Camera.objects.none(),
                                    required=True,
                                    error_messages={'required': 'Camera cannot be empty'},
                                    widget=forms.widgets.Select(attrs={"class": "form-control",
                                                                       "title": "Please select a camera",
                                                                       "required": "required"}),
                                    label="Camera")
    sessionDate = forms.DateField(required=True,
                                  error_messages={'required': 'Session Date cannot be empty'},
                                  widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                 attrs={"type": "date",
                                                                        "class": "form-control",
                                                                        "title": "Please enter a valid date",}),
                                  label="Session Start Date",
                                  initial=timezone.localtime(timezone.now()).date())
    comments = forms.CharField(required=False,
                               max_length=200,
                               widget=forms.widgets.Textarea(attrs={"class": "form-control",
                                                                    "title": "Please enter a maximum of 200 characters",
                                                                    "rows": 5}),
                               label="Comments")

    class Meta:
        model = Observes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(ObservesPortalForm, self).__init__(*args, **kwargs)
        if request:
            # Get the current branch
            current_branch = get_current_branch(request)
            # Set the queryset to the current branch's cameras and dogs
            self.fields['dog'].queryset = Dog.objects.filter(branch=current_branch).order_by('dogName')
            self.fields['camera'].queryset = Camera.objects.filter(branch=current_branch).order_by('camID')


# Observation Form in Portal
class ObservationPortalForm(forms.ModelForm):
    observes = forms.ModelChoiceField(queryset=Observes.objects.none(),
                                      required=True,
                                      error_messages={'required': 'Observation cannot be empty'},
                                      widget=forms.widgets.Select(attrs={"class": "form-control",
                                                                         "title": "Please select a session",
                                                                         "required": "required"}),
                                      label="Session")
    obsDateTime = forms.DateTimeField(required=True,
                                      error_messages={'required': 'Start Date and Time cannot be empty'},
                                      widget=forms.widgets.DateTimeInput(format='%Y-%m-%d %H:%M:%S',
                                                                         attrs={"class": "form-control",
                                                                                "title": "Please enter a valid date and time",
                                                                                "required": "required"}),
                                      label="Start Date and Time",
                                      initial=timezone.localtime(timezone.now())
                                      )
    sessionDurationInMins = forms.IntegerField(required=True,
                                               error_messages={'required': 'Duration cannot be empty'},
                                               widget=forms.widgets.NumberInput(attrs={"class": "form-control",
                                                                                       "title": "Please enter a duration (in minutes)",
                                                                                       "required": "required"}),
                                               label="Duration (mins)",
                                               initial=2,
                                               min_value=0)
    isKong = forms.ChoiceField(choices=Observation.IS_KONG_CHOICES,
                               required=False,
                               initial='N',
                               widget=forms.widgets.Select(attrs={"class": "form-control",
                                                                  "title": "Select if the dog is with a Kong"}),
                               label="With Kong?")
    isDog = forms.ChoiceField(choices=Observation.IS_DOG_CHOICES,
                              required=False,
                              initial='N',
                              widget=forms.widgets.Select(attrs={"class": "form-control",
                                                                 "title": "Select if the dog is with another Dog"}),
                              label="With Another Dog?")
    isHuman = forms.ChoiceField(choices=Observation.IS_HUMAN_CHOICES,
                                required=False,
                                initial='N',
                                widget=forms.widgets.Select(attrs={"class": "form-control",
                                                                   "title": "Select if the dog is with a Human"}),
                                label="With a Human?")
    jsonFile = forms.FileField(required=False,
                               widget=forms.widgets.FileInput(attrs={"class": "form-control-file",
                                                                     "title": "Upload a JSON file"}),
                               label="JSON File")
    rawVideo = forms.FileField(required=False,
                               widget=forms.widgets.FileInput(attrs={"class": "form-control-file",
                                                                     "title": "Upload a video file"}),
                               label="Video File")

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(ObservationPortalForm, self).__init__(*args, **kwargs)
        if request:
            # Get the current branch
            current_branch = get_current_branch(request)
            # Set the queryset to the current branch's Observations (Sessions)
            self.fields['observes'].queryset = Observes.objects.filter(dog__branch=current_branch).order_by('-sessionDate')

            # If the current branch is not Italy, then exclude the isDog and isHuman fields
            if current_branch.branchName != "Italy":
                self.fields.pop('isDog')
                self.fields.pop('isHuman')

    class Meta:
        model = Observation
        fields = ['observes', 'obsDateTime', 'sessionDurationInMins', 'isKong', 'isDog', 'isHuman', 'jsonFile', 'rawVideo']


# DogStance Form in Portal
class DogStancePortalForm(forms.ModelForm):
    observation = forms.ModelChoiceField(queryset=Observation.objects.none(),
                                         required=True,
                                         error_messages={'required': 'Observation cannot be empty'},
                                         widget=forms.widgets.Select(attrs={"class": "form-control",
                                                                            "title": "Please select an observation",
                                                                            "required": "required"}),
                                         label="Observation")
    stanceStartTime = forms.TimeField(required=True,
                                      error_messages={'required': 'Start Time cannot be empty'},
                                      widget=forms.widgets.TimeInput(format='%H:%M:%S',
                                                                     attrs={"class": "form-control",
                                                                            "title": "Please enter a valid time",
                                                                            "required": "required"}),
                                      label="Start Time in the Video",
                                      initial='00:00:00')
    dogStance = forms.ChoiceField(choices=DogStance.DOG_STANCE_CHOICES,
                                  required=True,
                                  error_messages={'required': 'Stance cannot be empty'},
                                  widget=forms.widgets.Select(attrs={"class": "form-control",
                                                                     "title": "Please select a stance",
                                                                     "required": "required"}),
                                  label="Stance")
    dogLocation = forms.ChoiceField(choices=DogStance.DOG_LOCATION_CHOICES,
                                    required=False,
                                    widget=forms.widgets.Select(attrs={"class": "form-control",
                                                                       "title": "Please select a location"}),
                                    label="Location")

    class Meta:
        model = DogStance
        fields = ['observation', 'stanceStartTime', 'dogStance', 'dogLocation']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Extract the request object
        super(DogStancePortalForm, self).__init__(*args, **kwargs)
        if request:
            # Get the current branch
            current_branch = get_current_branch(request)
            # Set the queryset to the current branch's owners
            self.fields['observation'].queryset = (Observation.objects.
                                                   filter(observes__dog__branch=current_branch).
                                                   order_by('-obsDateTime'))

class VoteForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']

ChoiceFormSet = forms.inlineformset_factory(
    Poll, Choice, form=ChoiceForm, max_num=4, can_delete=True
)