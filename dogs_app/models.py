import os
from django.utils.dateparse import parse_datetime
import pytz
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
import re


# Location of the default User profile picture if they don't have one
DEFAULT_PROFILE_IMAGE_SOURCE = 'profile_pictures/default.jpg'
ALTERNATIVE_DEFAULT_PROFILE_IMAGE_SOURCE = 'static/dogs_app/img/default.jpg'

# Location of the default Dog picture if they don't have one
DEFAULT_DOG_IMAGE_SOURCE = 'dog_pictures/default_dog.jpg'
ALTERNATIVE_DEFAULT_DOG_IMAGE_SOURCE = 'static/dogs_app/img/default_dog.jpg'

# Location of the default Kennel picture if they don't have one
DEFAULT_KENNEL_IMAGE_SOURCE = 'kennel_pictures/default_kennel.jpg'
ALTERNATIVE_DEFAULT_KENNEL_IMAGE_SOURCE = 'static/dogs_app/img/default_kennel.jpg'


# return the current date in the timezone of the user
def current_timezone_aware_date():
    return timezone.localtime(timezone.now()).date()


# return the current datetime in the timezone of the user
def current_timezone_aware_datetime():
    return timezone.localtime(timezone.now())


# Adding more attributes to the User model
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pictures', default=DEFAULT_PROFILE_IMAGE_SOURCE)

    def __str__(self):
        return f'{self.user.username} Profile'

    # Returns True if the user's profile picture is the default.jpg
    def is_default_image(self):
        if self.image is None or self.image.name == "" or 'default.jpg' in self.image.name:
            return True
        return self.image.name in [DEFAULT_PROFILE_IMAGE_SOURCE, ALTERNATIVE_DEFAULT_PROFILE_IMAGE_SOURCE]


def validate_phoneNum(value):
    if not re.match(r'^\d{0,9}$', value):
        raise ValidationError("Phone number must be up to 9 digits long and only contain digits.")


def validate_cellphoneNum(value):
    if not re.match(r'^\d{0,10}$', value):
        raise ValidationError("Cellphone number must be up to 10 digits long and only contain digits.")


def validate_ownerID(value):
    if not re.match(r'^\d*$', value):  # Matches only digits, allows empty string
        raise ValidationError("Owner ID must contain only digits.")


class Owner(models.Model):
    ownerSerialNum = models.AutoField(primary_key=True,
                                      verbose_name='Owner Serial Number')
    firstName = models.CharField(max_length=50,
                                 verbose_name='First Name')
    lastName = models.CharField(max_length=50, blank=True, null=True,
                                verbose_name='Last Name')
    # The actual ID number of the person
    ownerID = models.CharField(max_length=9, blank=True, null=True, unique=True,
                               validators=[validate_ownerID],
                               verbose_name='ID Number')
    ownerAddress = models.CharField(max_length=100, blank=True, null=True,
                                    verbose_name='Address')
    city = models.CharField(max_length=50, blank=True, null=True,
                            verbose_name='City')
    phoneNum = models.CharField(max_length=9, blank=True, null=True,
                                validators=[validate_phoneNum],
                                verbose_name='Phone Number')
    cellphoneNum = models.CharField(max_length=10, blank=True, null=True,
                                    validators=[validate_cellphoneNum],
                                    verbose_name='Cellphone Number')
    comments = models.CharField(max_length=250, blank=True, null=True,
                                verbose_name='Comments')
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE,
                               verbose_name='Branch')

    def __str__(self):
        if self.lastName is None:
            return f"{self.firstName}"
        else:
            return f"{self.firstName} {self.lastName}"


class Dog(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('', '-')
    ]

    IS_NEUTERED_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
        ('', '-')
    ]

    IS_DANGEROUS_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
        ('', '-')
    ]

    dogID = models.AutoField(primary_key=True)
    chipNum = models.CharField(max_length=30, unique=True, blank=True, null=True)
    dogName = models.CharField(max_length=35)
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Owner')
    dateOfBirthEst = models.DateField(blank=True, null=True)
    dateOfArrival = models.DateField(blank=True, null=True, default=current_timezone_aware_date)
    dateOfVaccination = models.DateField(blank=True, null=True)
    breed = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    furColor = models.CharField(max_length=20, blank=True, null=True)
    isNeutered = models.CharField(max_length=1, choices=IS_NEUTERED_CHOICES, blank=True, null=True)
    isDangerous = models.CharField(max_length=1, choices=IS_DANGEROUS_CHOICES, blank=True, null=True)
    dogImage = models.ImageField(upload_to='dog_pictures', default=DEFAULT_DOG_IMAGE_SOURCE, null=True, blank=True)
    kongDateAdded = models.DateField(blank=True, null=True)
    adoptionDate = models.DateField(blank=True, null=True, verbose_name='Adoption Date', default=None)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, verbose_name='Branch')

    # Returns True if the Dog's profile picture is the default.jpg
    def is_default_image(self):
        if not self.dogImage:
            return True
        return 'default_dog' in self.dogImage.name

    # For insuring dogImage is deleted if requested upon saving
    def save(self, *args, **kwargs):
        # If chipNum is an empty string, set it to None
        if self.chipNum == '':
            self.chipNum = None

        self.full_clean()

        # Check if dogImage is being deleted (i.e., set to None)
        if not self.dogImage:
            self.dogImage = DEFAULT_DOG_IMAGE_SOURCE

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dogName}"

    def clean(self):
        if self.dateOfBirthEst and self.dateOfBirthEst > timezone.localtime(timezone.now()).date():
            raise ValidationError("dateOfBirthEst must be before or current date.")

    class Meta:
        unique_together = (('chipNum', 'branch'),)


class Camera(models.Model):
    camID = models.PositiveSmallIntegerField(verbose_name='Camera ID')
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, verbose_name='Branch')

    def __str__(self):
        return f"Camera #{self.camID} - ({self.branch})"

    class Meta:
        ordering = ['branch', 'camID']
        unique_together = (('camID', 'branch'),)


# Returns the current date in Jerusalem timezone
def get_current_date_jerusalem():
    # Set timezone to 'Asia/Jerusalem'
    timezone.activate(pytz.timezone('Asia/Jerusalem'))
    # Return current date in Jerusalem timezone
    return timezone.localtime().date()


class Observes(models.Model):
    dog = models.ForeignKey('Dog', on_delete=models.CASCADE, null=True, related_name='observers', verbose_name='Dog')
    camera = models.ForeignKey('Camera', on_delete=models.CASCADE, null=True, related_name='observes', verbose_name='Camera')
    sessionDate = models.DateField(default=get_current_date_jerusalem, verbose_name='Session Start Date')
    comments = models.CharField(max_length=200, blank=True, null=True, verbose_name='Comments')

    # Handling cases where a dog or camera entities were deleted and are empty
    def __str__(self):
        dog_str = str(self.dog) if self.dog else "Unknown dog"
        camera_str = f"Camera #{self.camera.camID}" if self.camera else "Unknown camera"
        formatted_date = self.sessionDate.strftime("%d/%m/%Y")
        return f"{camera_str} on {dog_str} ({formatted_date})"

    # To ensure both values are always given by a user before changes.
    # They can only be blank because of deletion of Dog or Camera entities
    def save(self, *args, **kwargs):
        if self.dog is None or self.camera is None:
            raise ValidationError('Dog and Camera are required fields.')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Observes"
        unique_together = (('dog', 'camera', 'sessionDate'),)


class Treatment(models.Model):
    treatmentID = models.AutoField(primary_key=True,
                                   verbose_name='Treatment ID')
    treatmentName = models.CharField(max_length=50,
                                     verbose_name='Treatment Name')
    treatmentDate = models.DateField(blank=True, null=True,
                                     verbose_name='Date of Treatment',
                                     default=current_timezone_aware_date)
    treatedBy = models.CharField(max_length=50,
                                 verbose_name='Treated By')
    comments = models.CharField(max_length=250, blank=True, null=True,
                                verbose_name='Comments')
    dog = models.ForeignKey('Dog', on_delete=models.CASCADE,
                            verbose_name='Dog')

    def __str__(self):
        return f"'{self.treatmentName}' on {self.dog} (by {self.treatedBy})"


class EntranceExamination(models.Model):
    examinationID = models.AutoField(primary_key=True,
                                     verbose_name='Examination ID')
    examinationDate = models.DateField(default=current_timezone_aware_date,
                                       verbose_name='Examination Date')
    examinedBy = models.CharField(max_length=50,
                                  verbose_name='Examined By')
    results = models.CharField(max_length=150, blank=True, null=True,
                               verbose_name='Results')
    dogWeight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                    verbose_name='Weight',
                                    validators=[MinValueValidator(0), MaxValueValidator(250)],
                                    help_text='In Kilograms')
    dogTemperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                         verbose_name='Temperature',
                                         validators=[MinValueValidator(0), MaxValueValidator(250)],
                                         help_text='In Celsius')
    dogPulse = models.PositiveSmallIntegerField(blank=True, null=True,
                                                verbose_name='Pulse',
                                                validators=[MinValueValidator(0), MaxValueValidator(250)],
                                                help_text='In BPM')
    comments = models.CharField(max_length=250, blank=True, null=True,
                                verbose_name='Comments')
    dog = models.ForeignKey('Dog', on_delete=models.CASCADE,
                            verbose_name='Dog')

    def __str__(self):
        formatted_date = self.examinationDate.strftime("%d/%m/%Y")
        return f"{self.dog} by {self.examinedBy} ({formatted_date})"


class Kennel(models.Model):
    kennelNum = models.PositiveSmallIntegerField(verbose_name='Kennel Number')
    kennelImage = models.ImageField(upload_to='kennel_pictures',
                                    default=DEFAULT_KENNEL_IMAGE_SOURCE,
                                    null=True, blank=True,
                                    verbose_name='Kennel Image')
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, verbose_name='Branch')

    # Deleting an old image, used in save() below
    def delete_old_image(self):
        if self.kennelImage and hasattr(self.kennelImage, 'path'):
            old_image_path = self.kennelImage.path
            if os.path.isfile(old_image_path) and not self.is_default_image():
                os.remove(old_image_path)

    # Insuring kennelImage is deleted if requested upon saving
    def save(self, *args, **kwargs):
        self.full_clean()

        # Check if dogImage is being deleted (i.e., set to None)
        if not self.kennelImage:
            self.delete_old_image()
            self.kennelImage = DEFAULT_KENNEL_IMAGE_SOURCE

        super().save(*args, **kwargs)

    # Returns True if the Kennel's profile picture is the default_kennel.jpg
    def is_default_image(self):
        if not self.kennelImage:
            return True
        return self.kennelImage.name.startswith('default_kennel')

    def __str__(self):
        return f"Kennel #{self.kennelNum} ({self.branch})"

    class Meta:
        ordering = ['branch', 'kennelNum']
        unique_together = (('kennelNum', 'branch'),)


class DogPlacement(models.Model):
    dog = models.ForeignKey('Dog', models.CASCADE, null=True,
                            verbose_name='Dog')
    kennel = models.ForeignKey('Kennel', models.CASCADE, null=True,
                               verbose_name='Kennel')
    entranceDate = models.DateField(default=current_timezone_aware_date,
                                    verbose_name='Entrance Date')
    expirationDate = models.DateField(blank=True, null=True,
                                      verbose_name='Expiration Date')
    placementReason = models.CharField(max_length=75, blank=True, null=True,
                                       verbose_name='Placement Reason')

    # Handling cases where a Kennel or a Dog was deleted, displays "Unknown" instead
    def __str__(self):
        formatted_date = self.entranceDate.strftime("%d/%m/%Y")
        if self.dog is None:
            dog_str = "an unknown dog"
        else:
            dog_str = str(self.dog)
        if self.kennel is None:
            kennel_str = "an unknown kennel"
        else:
            kennel_str = str(self.kennel.kennelNum)

        return f"{dog_str} in {kennel_str} ({formatted_date})"

    # Ensures that neither dog nor kennel is None when creating a new DogPlacement instance.
    def save(self, *args, **kwargs):
        if self.dog is None or self.kennel is None:
            raise ValidationError('Dog and Kennel are required fields.')
        # Ensure expirationDate is not before entranceDate
        if self.expirationDate and self.entranceDate and self.expirationDate < self.entranceDate:
            raise ValidationError("Expiration Date cannot be before Entrance Date.")

        super().save(*args, **kwargs)

    # Calculates dog's stay duration in the kennel (expiratedDate-entranceDate)
    def duration(self):
        if self.expirationDate and self.entranceDate:
            return (self.expirationDate - self.entranceDate).days
        else:
            return 'N/A'

    class Meta:
        unique_together = (('dog', 'kennel', 'entranceDate'),)
        ordering = ['-entranceDate']


# Defining Validators for validating Observation data below
# JSON File validator, raises an error if the file is not JSON
def validate_json_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.json']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. File should have a valid .json format.')


# Video File Validator, raises an error if the file is not a video
def validate_video_file_extension(value):
    # List of allowed video file extensions, as defined in settings.py
    from dogshelter_site.settings import ALLOWED_VIDEO_FILE_EXTENSIONS
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ALLOWED_VIDEO_FILE_EXTENSIONS
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported video file extension.')


class Observation(models.Model):
    IS_KONG_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]

    IS_DOG_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]

    IS_HUMAN_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]

    # References the Observes instance
    observes = models.ForeignKey('Observes', on_delete=models.CASCADE, null=True, verbose_name='Session')
    obsDateTime = models.DateTimeField(default=current_timezone_aware_datetime, verbose_name='Starting Date and Time', db_index=True)
    sessionDurationInMins = models.PositiveIntegerField(default=2,
                                                        validators=[MinValueValidator(0)],
                                                        verbose_name='Session Duration (mins)')
    isKong = models.CharField(max_length=1, choices=IS_KONG_CHOICES,
                              blank=True, null=True,
                              default='N', verbose_name='With Kong')
    isDog = models.CharField(max_length=1, choices=IS_DOG_CHOICES,
                             blank=True, null=True,
                             default=None, verbose_name='With Dog')
    isHuman = models.CharField(max_length=1, choices=IS_HUMAN_CHOICES,
                               blank=True, null=True,
                               default=None, verbose_name='With Human')
    jsonFile = models.FileField(upload_to='json_files',
                                validators=[validate_json_file_extension],
                                null=True, blank=True, verbose_name='JSON File')
    rawVideo = models.FileField(upload_to='raw_videos',
                                validators=[validate_video_file_extension],
                                null=True, blank=True, verbose_name='Video')

    def save(self, *args, **kwargs):
        """
        Overridden save method to ensure that:
        - An Observation instance must be associated with an Observes instance.
        - The jsonFile and rawVideo are deleted if replaced upon saving.
        """

        # Ensuring that the Observes instance exists
        if self.observes is None:
            raise ValidationError("An Observation must be associated with a Session instance.")

        self.full_clean()

        # Check if the instance being saved is a new one or an existing one
        if self.pk:
            old_file_json = Observation.objects.get(pk=self.pk).jsonFile
            old_file_video = Observation.objects.get(pk=self.pk).rawVideo

            # Check if jsonFile is replaced
            if old_file_json and self.jsonFile != old_file_json:
                old_file_json.delete(save=False)

            # Check if rawVideo is replaced
            if old_file_video and self.rawVideo != old_file_video:
                old_file_video.delete(save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        local_tz = pytz.timezone('Asia/Jerusalem')
        local_time = timezone.localtime(self.obsDateTime, local_tz)
        formatted_date = local_time.strftime("%d/%m/%Y at %H:%M:%S")
        observes_str = str(self.observes) if self.observes else "Unknown dog or camera"
        return f"Session: [{observes_str}] - Observation: {formatted_date}"

    class Meta:
        unique_together = ('observes', 'obsDateTime')
        ordering = ['-obsDateTime']


class DogStance(models.Model):

    DOG_STANCE_CHOICES = [
        ('STANDING', 'Standing'),
        ('SITTING', 'Sitting'),
        ('WALKING_AROUND', 'Walking Around'),
        ('SLEEPING_LYING', 'Sleeping/Laying'),
        ('EATING', 'Eating'),
        ('DRINKING', 'Drinking'),
        ('UNDER', 'Under'),
        ('JUMPING', 'Jumping'),
        ('PACING', 'Pacing'),
        ('CIRCLING', 'Circling'),
        ('ALERT', 'Alert'),
        ('ELSE', 'Else'),
    ]

    DOG_LOCATION_CHOICES = [
        ('FLOOR', 'On Floor'),
        ('BENCH', 'On Bench'),
        ('ONBARS', 'On Bars'),
        ('WALLTOWALL', 'From Wall to Wall'),
        ('ELSE', 'Else'),
    ]

    observation = models.ForeignKey('Observation', on_delete=models.CASCADE, null=True, verbose_name='Observation')
    stanceStartTime = models.TimeField(verbose_name='Stance Start Time')
    dogStance = models.CharField(max_length=15, choices=DOG_STANCE_CHOICES, verbose_name='Stance')
    dogLocation = models.CharField(max_length=10, choices=DOG_LOCATION_CHOICES, blank=True, null=True, verbose_name='Location')

    # Format the date and check if entity contains a valid Observation to display
    def __str__(self):
        formatted_time = self.stanceStartTime.strftime("%H:%M:%S")
        observation_str = str(self.observation) if self.observation else "Unknown observation"
        return f"Starting at {formatted_time} ({observation_str})"

    def save(self, *args, **kwargs):
        """
        Overrides the default save method.
        Raise a ValidationError if the 'observation' field is not provided (NULL).
        """
        if self.observation is None:
            raise ValidationError("'observation' field must be provided.")
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('observation', 'stanceStartTime')
        ordering = ['-stanceStartTime']


# Poll model for showing the latest polls and displaying them on the homepage
class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, verbose_name='Branch')

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name_plural = "Poll"

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


# News Model for saving the latest website news and displaying them on the homepage
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, verbose_name='Branch')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name_plural = "News"


# Branch model for handling the different branches of the shelter (default: Israel, secondary: Italy)
class Branch(models.Model):
    branchName = models.CharField(max_length=20, unique=True, verbose_name='Branch Name')

    # Add more fields later if needed
    # branchAddress = models.CharField(max_length=100, verbose_name='Branch Address')
    # branchPhone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Branch Phone Number')
    # branchEmail = models.EmailField(max_length=50, blank=True, null=True, verbose_name='Branch Email')
    # branchManager = models.CharField(max_length=50, blank=True, null=True, verbose_name='Branch Manager')

    def __str__(self):
        return f"{self.branchName}"

    class Meta:
        verbose_name_plural = "Branch"
