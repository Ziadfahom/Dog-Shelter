from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
from django import forms
from .models import (Dog, Owner, Profile, Treatment, EntranceExamination,
                     Observation, DogPlacement, Kennel, Observes, DogStance, News, Camera)
from django.core.exceptions import ValidationError
from datetime import date


# New User Registration Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'


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
                              widget=forms.widgets.TextInput(attrs={"placeholder": "Dog Name",
                                                                    "class": "form-control"}),
                              label="Dog Name")
    chipNum = forms.CharField(required=False,
                              max_length=30,
                              validators=[RegexValidator(r'^[0-9]*$', 'Chip Number can only have numbers')],
                              widget=forms.widgets.TextInput(attrs={"placeholder": "Chip Number",
                                                                    "class": "form-control"}),
                              label="Chip Number")
    dateOfBirthEst = forms.DateField(required=False,
                                     widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                    attrs={"type": "date",
                                                                           "placeholder": "Estimated Date of Birth",
                                                                           "class": "form-control"}),
                                     label="Estimated Date of Birth")
    dateOfArrival = forms.DateField(required=False,
                                    initial=timezone.now().date(),
                                    widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                   attrs={"type": "date",
                                                                          "placeholder": "Date of Arrival",
                                                                          "class": "form-control"}),
                                    label="Date of Arrival")
    dateOfVaccination = forms.DateField(required=False,
                                        widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                       attrs={"type": "date",
                                                                              "placeholder": "Date of Vaccination",
                                                                              "class": "form-control"}),
                                        label="Date of Vaccination")
    breed = forms.CharField(required=False,
                            max_length=30,
                            widget=forms.widgets.TextInput(attrs={"placeholder": "Breed",
                                                                  "class": "form-control"}),
                            label="Breed")
    gender = forms.ChoiceField(choices=Dog.GENDER_CHOICES,
                               required=False,
                               widget=forms.widgets.Select(attrs={"placeholder": "Gender",
                                                                  "class": "form-control"}),
                               label="Gender")
    furColor = forms.CharField(required=False,
                               max_length=20,
                               widget=forms.widgets.TextInput(attrs={"placeholder": "Fur Color",
                                                                     "class": "form-control"}),
                               label="Fur Color")
    isNeutered = forms.ChoiceField(choices=Dog.IS_NEUTERED_CHOICES,
                                   required=False,
                                   widget=forms.widgets.Select(attrs={"placeholder": "Neutered?",
                                                                      "class": "form-control"}),
                                   label="Neutered?")
    isDangerous = forms.ChoiceField(choices=Dog.IS_DANGEROUS_CHOICES,
                                    required=False,
                                    widget=forms.widgets.Select(attrs={"placeholder": "Dangerous?",
                                                                       "class": "form-control"}),
                                    label="Dangerous?")
    dogImage = forms.ImageField(required=False,
                                widget=forms.widgets.ClearableFileInput(attrs={"class": "form-control"}),
                                label="Dog Image",
                                help_text="Upload the dog's image here.")
    kongDateAdded = forms.DateField(required=False,
                                    widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                   attrs={"type": "date",
                                                                          "placeholder": "Last Date Given a Kong",
                                                                          "class": "form-control"}),
                                    label="Last Date Given a Kong")
    owner = forms.ModelChoiceField(queryset=Owner.objects.all(),
                                   required=False,
                                   widget=forms.widgets.Select(attrs={"placeholder": "Dog's Owner",
                                                                      "class": "form-control"}),
                                   label="Dog's Owner")

    class Meta:
        model = Dog
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddDogForm, self).__init__(*args, **kwargs)
        # Add a 'date-field' CSS class to date fields for easy targeting in JavaScript
        self.fields['dateOfArrival'].widget.attrs.update({'class': 'date-field'})
        self.fields['dateOfBirthEst'].widget.attrs.update({'class': 'date-field'})
        self.fields['dateOfVaccination'].widget.attrs.update({'class': 'date-field'})
        self.fields['kongDateAdded'].widget.attrs.update({'class': 'date-field'})

    def clean_dateOfBirthEst(self):
        dob = self.cleaned_data.get('dateOfBirthEst')
        if dob and dob > date.today():
            raise ValidationError('Estimated Date of Birth cannot be a future date')
        return dob


# Form for update users
class UpdateUserForm(UserChangeForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Email Address'}))
    first_name = forms.CharField(max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Last Name'}))
    # For displaying User Status (ranking)
    ROLE_CHOICES = [
        ('Viewer', 'Viewer'),
        ('Vet', 'Vet'),
        ('Admin', 'Admin'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, required=False)

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
                                                   'placeholder': 'Phone Number'}),
            'address': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Address'}),
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
            'treatmentName': forms.TextInput(attrs={'class': 'form-control'}),
            'treatmentDate': forms.DateInput(attrs={'class': 'form-control',
                                                    'type': 'text',
                                                    'data-provide': 'datepicker',
                                                    'readonly': 'readonly'}),
            'treatedBy': forms.TextInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
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
                                                      'readonly': 'readonly'}),
            'examinedBy': forms.TextInput(attrs={'class': 'form-control'}),
            'results': forms.TextInput(attrs={'class': 'form-control'}),
            'dogWeight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0-200'}),
            'dogTemperature': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0-200'}),
            'dogPulse': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0-200'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
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
            'firstName': forms.TextInput(attrs={'class': 'form-control'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control'}),
            'ownerID': forms.TextInput(attrs={'class': 'form-control'}),
            'ownerAddress': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'phoneNum': forms.TextInput(attrs={'class': 'form-control'}),
            'cellphoneNum': forms.TextInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# Form for Camera
class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ['camID']

        widgets = {
            'camID': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Form for adding new Kennel
class KennelForm(forms.ModelForm):
    kennelNum = forms.CharField(required=True,
                                error_messages={'required': 'Kennel Number cannot be empty'},
                                widget=forms.widgets.TextInput(attrs={"placeholder": "Kennel Number",
                                                                      "class": "form-control"}),
                                label="Kennel Number")
    kennelImage = forms.ImageField(required=False,
                                   widget=forms.widgets.ClearableFileInput(attrs={"class": "form-control"}),
                                   label="Kennel Image",
                                   help_text="Upload the kennel's image here.")

    class Meta:
        model = Kennel
        fields = '__all__'


# Form for editing a Kennel
class KennelEditForm(forms.ModelForm):
    # Disable editing Kennel Number
    kennelNum = forms.CharField(required=True,
                                error_messages={'required': 'Kennel Number cannot be empty'},
                                widget=forms.widgets.TextInput(attrs={"placeholder": "Kennel Number",
                                                                      "class": "form-control"}),
                                label="Kennel Number",
                                disabled=True)
    kennelImage = forms.ImageField(required=False,
                                   widget=forms.widgets.ClearableFileInput(attrs={"class": "form-control"}),
                                   label="Kennel Image",
                                   help_text="Upload the kennel's image here.")

    class Meta:
        model = Kennel
        fields = '__all__'


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
            'kennel': forms.Select(attrs={'class': 'form-control'}),
            'entranceDate': forms.DateInput(attrs={'class': 'form-control',
                                                   'type': 'text',
                                                   'data-provide': 'datepicker',
                                                   'readonly': 'readonly'}),
            'expirationDate': forms.DateInput(attrs={'class': 'form-control',
                                                     'type': 'text',
                                                     'data-provide': 'datepicker',
                                                     'readonly': 'readonly'}),
            'placementReason': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Form for adding new Camera Session (Observes)
class ObservesForm(forms.ModelForm):
    class Meta:
        model = Observes
        fields = ['sessionDate', 'camera', 'comments']
        labels = {
            'camera' : "Camera",
            'comments': "Comments",
            'sessionDate': 'Session Date'
        }
        widgets = {
            'sessionDate': forms.DateInput(attrs={'class': 'form-control',
                                                  'type': 'text',
                                                  'data-provide': 'datepicker',
                                                  'readonly': 'readonly'}),
            'camera': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        }

    def clean_camera(self):
        camera = self.cleaned_data['camera']
        if not camera:
            raise forms.ValidationError("A camera must be selected.")
        return camera


# Form for adding new Observation
class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = ['obsDateTime', 'sessionDurationInMins', 'isKong', 'jsonFile', 'rawVideo']
        widgets = {
            'sessionDurationInMins': forms.NumberInput(attrs={'class': 'form-control'}),
            'isKong': forms.Select(choices=Observation.IS_KONG_CHOICES, attrs={'class': 'form-control'}),
            'jsonFile': forms.FileInput(attrs={'class': 'form-control-file'}),
            'rawVideo': forms.FileInput(attrs={'class': 'form-control-file'})
        }


# Form for adding new Dog Stance
class DogStanceForm(forms.ModelForm):
    class Meta:
        model = DogStance
        fields = ['stanceStartTime', 'dogStance', 'dogLocation']

        widgets = {
            'stanceStartTime': forms.TimeInput(attrs={'class': 'form-control'}),
            'dogStance': forms.Select(attrs={'class': 'form-control'}),
            'dogLocation': forms.Select(attrs={'class': 'form-control'})
        }


# Form for Treatments in Portal
class TreatmentPortalForm(forms.ModelForm):
    treatmentName = forms.CharField(required=True,
                                    max_length=50,
                                    error_messages={'required': 'Treatment Name cannot be empty'},
                                    widget=forms.widgets.TextInput(attrs={"placeholder": "Treatment Name",
                                                                          "class": "form-control"}),
                                    label="Treatment Name")
    treatmentDate = forms.DateField(required=False,
                                    widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                   attrs={"type": "date",
                                                                          "placeholder": "Date of Treatment",
                                                                          "class": "form-control"}),
                                    label="Date of Treatment",
                                    initial=timezone.now().date())
    treatedBy = forms.CharField(required=True,
                                max_length=50,
                                error_messages={'required': '"Treated By" cannot be empty'},
                                widget=forms.widgets.TextInput(attrs={"placeholder": "Treated By",
                                                                      "class": "form-control"}),
                                label="Treated By")
    comments = forms.CharField(required=False,
                               max_length=250,
                               widget=forms.widgets.Textarea(attrs={"placeholder": "Comments",
                                                                    "class": "form-control",
                                                                    "rows": 3}),
                               label="Comments")
    dog = forms.ModelChoiceField(queryset=Dog.objects.all(),
                                 required=True,
                                 widget=forms.widgets.Select(attrs={"placeholder": "Dog",
                                                                    "class": "form-control"}),
                                 label="Dog")

    class Meta:
        model = Treatment
        fields = '__all__'


# Form for Examinations in Portal
class ExaminationPortalForm(forms.ModelForm):
    examinationDate = forms.DateField(required=True,
                                      widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                     attrs={"type": "date",
                                                                            "placeholder": "Date of Examination",
                                                                            "class": "form-control"}),
                                      label="Date of Examination",
                                      initial=timezone.now().date())
    examinedBy = forms.CharField(required=True,
                                 max_length=50,
                                 error_messages={'required': '"Examined By" cannot be empty'},
                                 widget=forms.widgets.TextInput(attrs={"placeholder": "Examined By",
                                                                       "class": "form-control"}),
                                 label="Examined By")
    results = forms.CharField(required=False,
                              max_length=100,
                              widget=forms.widgets.Textarea(attrs={"placeholder": "Results",
                                                                   "class": "form-control",
                                                                   "rows": 2}),
                              label="Results")
    dogWeight = forms.DecimalField(required=False,
                                   widget=forms.widgets.NumberInput(attrs={"placeholder": "Weight",
                                                                           "class": "form-control",
                                                                           "min": 0,
                                                                           "max": 250}),
                                   label="Weight")
    dogTemperature = forms.DecimalField(required=False,
                                        widget=forms.widgets.NumberInput(attrs={"placeholder": "Temperature",
                                                                                "class": "form-control",
                                                                                "min": 0,
                                                                                "max": 250}),
                                        label="Temperature")
    dogPulse = forms.DecimalField(required=False,
                                  widget=forms.widgets.NumberInput(attrs={"placeholder": "Pulse",
                                                                          "class": "form-control",
                                                                          "min": 0,
                                                                          "max": 250}),
                                  label="Pulse")
    comments = forms.CharField(required=False,
                               max_length=250,
                               widget=forms.widgets.Textarea(attrs={"placeholder": "Comments",
                                                                    "class": "form-control",
                                                                    "rows": 3}),
                               label="Comments")
    dog = forms.ModelChoiceField(queryset=Dog.objects.all(),
                                 required=True,
                                 widget=forms.widgets.Select(attrs={"placeholder": "Dog",
                                                                    "class": "form-control"}),
                                 label="Dog")

    class Meta:
        model = EntranceExamination
        fields = '__all__'


# Dog Placement Form in Portal
class PlacementPortalForm(forms.ModelForm):
    dog = forms.ModelChoiceField(queryset=Dog.objects.all(),
                                 required=True,
                                 widget=forms.widgets.Select(attrs={"placeholder": "Dog",
                                                                    "class": "form-control"}),
                                 label="Dog")
    kennel = forms.ModelChoiceField(queryset=Kennel.objects.all(),
                                    required=True,
                                    widget=forms.widgets.Select(attrs={"placeholder": "Kennel",
                                                                       "class": "form-control"}),
                                    label="Kennel")
    entranceDate = forms.DateField(required=True,
                                   widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                  attrs={"type": "date",
                                                                         "placeholder": "Date of Entrance",
                                                                         "class": "form-control"}),
                                   label="Date of Entrance",
                                   initial=timezone.now().date())
    expirationDate = forms.DateField(required=False,
                                     widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                    attrs={"type": "date",
                                                                           "placeholder": "Date of Expiration",
                                                                           "class": "form-control"}),
                                     label="Date of Expiration")
    placementReason = forms.CharField(required=False,
                                      max_length=75,
                                      widget=forms.widgets.Textarea(attrs={"placeholder": "Placement Reason",
                                                                           "class": "form-control",
                                                                           "rows": 2}),
                                      label="Placement Reason")

    class Meta:
        model = DogPlacement
        fields = '__all__'


# Session (Observes) Form in Portal
class ObservesPortalForm(forms.ModelForm):
    dog = forms.ModelChoiceField(queryset=Dog.objects.all(),
                                 required=True,
                                 widget=forms.widgets.Select(attrs={"placeholder": "Dog",
                                                                    "class": "form-control"}),
                                 label="Dog")
    camera = forms.ModelChoiceField(queryset=Camera.objects.all(),
                                    required=True,
                                    widget=forms.widgets.Select(attrs={"placeholder": "Camera",
                                                                       "class": "form-control"}),
                                    label="Camera")
    sessionDate = forms.DateField(required=True,
                                  widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                 attrs={"type": "date",
                                                                        "placeholder": "Session Start Date",
                                                                        "class": "form-control"}),
                                  label="Session Start Date",
                                  initial=timezone.now().date())
    comments = forms.CharField(required=False,
                               max_length=200,
                               widget=forms.widgets.Textarea(attrs={"placeholder": "Comments",
                                                                    "class": "form-control",
                                                                    "rows": 4}),
                               label="Comments")

    class Meta:
        model = Observes
        fields = '__all__'


# Observation Form in Portal
class ObservationPortalForm(forms.ModelForm):
    observes = forms.ModelChoiceField(queryset=Observes.objects.all(),
                                      required=True,
                                      widget=forms.widgets.Select(attrs={"placeholder": "Session",
                                                                         "class": "form-control"}),
                                      label="Session")
    obsDateTime = forms.DateTimeField(required=True,
                                      widget=forms.widgets.DateTimeInput(format='%Y-%m-%d %H:%M:%S',
                                                                         attrs={"type": "datetime",
                                                                                "placeholder": "Start Date and Time",
                                                                                "class": "form-control"}),
                                      label="Start Date and Time",
                                      initial=timezone.now()
                                      )
    sessionDurationInMins = forms.IntegerField(required=True,
                                               widget=forms.widgets.NumberInput(attrs={"placeholder": "Duration (mins)",
                                                                                       "class": "form-control"}),
                                               label="Duration (mins)",
                                               initial=2,
                                               min_value=0)
    isKong = forms.ChoiceField(choices=Observation.IS_KONG_CHOICES,
                               required=False,
                               widget=forms.widgets.Select(attrs={"placeholder": "With Kong?",
                                                                  "class": "form-control"}),
                               label="With Kong?")
    jsonFile = forms.FileField(required=False,
                               widget=forms.widgets.FileInput(attrs={"class": "form-control-file"}),
                               label="JSON File")
    rawVideo = forms.FileField(required=False,
                               widget=forms.widgets.FileInput(attrs={"class": "form-control-file"}),
                               label="Video File")

    class Meta:
        model = Observation
        fields = ['observes', 'obsDateTime', 'sessionDurationInMins', 'isKong', 'jsonFile', 'rawVideo']


# DogStance Form in Portal
class DogStancePortalForm(forms.ModelForm):
    observation = forms.ModelChoiceField(queryset=Observation.objects.all(),
                                         required=True,
                                         widget=forms.widgets.Select(attrs={"placeholder": "Observation",
                                                                            "class": "form-control"}),
                                         label="Observation")
    stanceStartTime = forms.TimeField(required=True,
                                      widget=forms.widgets.TimeInput(format='%H:%M:%S',
                                                                     attrs={"placeholder": "Start Time in the Video",
                                                                            "class": "form-control"}),
                                      label="Start Time in the Video",
                                      initial='00:00:00')
    dogStance = forms.ChoiceField(choices=DogStance.DOG_STANCE_CHOICES,
                                  required=True,
                                  widget=forms.widgets.Select(attrs={"placeholder": "Stance",
                                                                     "class": "form-control"}),
                                  label="Stance")
    dogLocation = forms.ChoiceField(choices=DogStance.DOG_LOCATION_CHOICES,
                                    required=False,
                                    widget=forms.widgets.Select(attrs={"placeholder": "Location",
                                                                       "class": "form-control"}),
                                    label="Location")

    class Meta:
        model = DogStance
        fields = ['observation', 'stanceStartTime', 'dogStance', 'dogLocation']
