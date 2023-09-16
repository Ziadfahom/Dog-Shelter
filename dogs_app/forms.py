from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
from django import forms
from .models import Dog, Owner, Profile, Treatment, EntranceExamination, Observation, DogPlacement, Kennel
from django.core.exceptions import ValidationError
from datetime import date


# New User Registration Form
class SignUpForm(UserCreationForm):

    # Input fields
    email = forms.EmailField(label='',
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Email Address'}))
    first_name = forms.CharField(label='',
                                 max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'First Name'}))
    last_name = forms.CharField(label='',
                                max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Last Name'}))

    # Defining a user in the system
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    # Setting up the 'Username', 'Password' and 'Confirm Password' fields
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = 'User Name'
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters' \
                                            ' or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = 'Password'
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be' \
                                             ' too similar to your other personal information.</li><li>Your password' \
                                             ' must contain at least 8 characters.</li><li>Your password can\'t be' \
                                             ' a commonly used password.</li><li>Your password can\'t be' \
                                             ' entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password' \
                                             ' as before for verification.</small></span>'

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
        widgets = {
            'examinationDate': forms.DateInput(attrs={'class': 'form-control',
                                                      'type': 'text',
                                                      'data-provide': 'datepicker',
                                                      'readonly': 'readonly'}),
            'examinedBy': forms.TextInput(attrs={'class': 'form-control'}),
            'results': forms.TextInput(attrs={'class': 'form-control'}),
            'dogWeight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0-99'}),
            'dogTemperature': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0-99'}),
            'dogPulse': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0-200'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


# Form for adding new Dog Placements (in Kennels)
class DogPlacementForm(forms.ModelForm):
    class Meta:
        model = DogPlacement
        fields = ['kennel', 'entranceDate', 'expirationDate', 'placementReason']
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