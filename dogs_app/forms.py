from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
from django import forms
from .models import Dog, Owner
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
    dogImageURL = forms.URLField(required=False,
                                 max_length=200,
                                 widget=forms.widgets.URLInput(attrs={"placeholder": "Dog Image Link",
                                                                      "class": "form-control"}),
                                 label="Dog Image Link")
    kongDateAdded = forms.DateField(required=False,
                                    widget=forms.widgets.DateInput(format='%Y-%m-%d',
                                                                   attrs={"type": "date",
                                                                          "placeholder": "Last Date Given a Kong",
                                                                          "class": "form-control"}),
                                    label="Last Date Given a Kong")
    ownerSerialNum = forms.ModelChoiceField(queryset=Owner.objects.all(),
                                            required=False,
                                            widget=forms.widgets.Select(attrs={"placeholder": "Dog's Owner",
                                                                               "class": "form-control"}),
                                            label="Dog's Owner")

    class Meta:
        model = Dog
        exclude = ('dogID',)

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

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
