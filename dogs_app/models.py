import os
import pytz
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


# Location of the default User profile picture if they don't have one
DEFAULT_PROFILE_IMAGE_SOURCE = 'profile_pictures/default.jpg'
ALTERNATIVE_DEFAULT_PROFILE_IMAGE_SOURCE = 'static/dogs_app/img/default.jpg'

# Location of the default Dog picture if they don't have one
DEFAULT_DOG_IMAGE_SOURCE = 'dog_pictures/default_dog.jpg'
ALTERNATIVE_DEFAULT_DOG_IMAGE_SOURCE = 'static/dogs_app/img/default_dog.jpg'

# Location of the default Kennel picture if they don't have one
DEFAULT_KENNEL_IMAGE_SOURCE = 'kennel_pictures/default_kennel.jpg'
ALTERNATIVE_DEFAULT_KENNEL_IMAGE_SOURCE = 'static/dogs_app/img/default_kennel.jpg'


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


class Owner(models.Model):
    ownerSerialNum = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50, blank=True, null=True)
    # The actual ID number of the person
    ownerID = models.CharField(max_length=9, blank=True, null=True)
    ownerAddress = models.CharField(max_length=70, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    phoneNum = models.CharField(max_length=9, blank=True, null=True, unique=True)
    cellphoneNum = models.CharField(max_length=10, blank=True, null=True)
    comments = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        if self.lastName is None:
            return f"{self.firstName}"
        else:
            return f"{self.firstName} {self.lastName}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(phoneNum__regex='^[0-9]{9}$'),
                name='phoneNum_check',
            ),
            models.CheckConstraint(
                check=models.Q(cellphoneNum__regex='^[0-9]{10}$'),
                name='cellphoneNum_check',
            ),
        ]


class Dog(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
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
    dateOfBirthEst = models.DateField(blank=True, null=True)
    dateOfArrival = models.DateField(blank=True, null=True, default=timezone.now)
    dateOfVaccination = models.DateField(blank=True, null=True)
    breed = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    furColor = models.CharField(max_length=20, blank=True, null=True)
    isNeutered = models.CharField(max_length=1, choices=IS_NEUTERED_CHOICES, blank=True, null=True)
    isDangerous = models.CharField(max_length=1, choices=IS_DANGEROUS_CHOICES, blank=True, null=True)
    dogImage = models.ImageField(upload_to='dog_pictures', default=DEFAULT_DOG_IMAGE_SOURCE, null=True, blank=True)
    kongDateAdded = models.DateField(blank=True, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Owner')

    # Returns True if the Dog's profile picture is the default.jpg
    def is_default_image(self):
        if not self.dogImage:
            return True
        return 'default_dog' in self.dogImage.name

    # For insuring dogImage is deleted if requested upon saving
    def save(self, *args, **kwargs):
        self.full_clean()

        # Check if dogImage is being deleted (i.e., set to None)
        if not self.dogImage:
            self.dogImage = DEFAULT_DOG_IMAGE_SOURCE

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dogName}"

    def clean(self):
        if self.dateOfBirthEst and self.dateOfBirthEst > timezone.now().date():
            raise ValidationError("dateOfBirthEst must be before or current date.")


class Camera(models.Model):
    camID = models.PositiveSmallIntegerField(primary_key=True)

    def __str__(self):
        return f"Camera #{self.camID}"

    class Meta:
        ordering = ['camID']


class Observes(models.Model):
    dog = models.ForeignKey('Dog', on_delete=models.SET_NULL, null=True, related_name='observers')
    camera = models.ForeignKey('Camera', on_delete=models.SET_NULL, null=True, related_name='observes')
    sessionDate = models.DateField(default=timezone.now)
    comments = models.CharField(max_length=200, blank=True, null=True)

    # Handling cases where a dog or camera entities were deleted and are empty
    def __str__(self):
        dog_str = str(self.dog) if self.dog else "Unknown dog"
        camera_str = str(self.camera) if self.camera else "Unknown camera"
        formatted_date = self.sessionDate.strftime("%d-%m-%Y")
        return f"{camera_str} on {dog_str} on {formatted_date}"

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
    treatmentID = models.AutoField(primary_key=True)
    treatmentName = models.CharField(max_length=50)
    treatmentDate = models.DateField(blank=True, null=True)
    treatedBy = models.CharField(max_length=50)
    comments = models.CharField(max_length=250, blank=True, null=True)
    dog = models.ForeignKey('Dog', on_delete=models.CASCADE)

    def __str__(self):
        return f"Treatment: '{self.treatmentName}' on {self.dog}, by {self.treatedBy}"


class EntranceExamination(models.Model):
    examinationID = models.AutoField(primary_key=True)
    examinationDate = models.DateField(default=timezone.now)
    examinedBy = models.CharField(max_length=50)
    results = models.CharField(max_length=100, blank=True, null=True)
    dogWeight = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    dogTemperature = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    dogPulse = models.PositiveSmallIntegerField(blank=True, null=True)
    comments = models.CharField(max_length=200, blank=True, null=True)
    dog = models.ForeignKey('Dog', on_delete=models.CASCADE)

    def __str__(self):
        formatted_date = self.examinationDate.strftime("%d-%m-%Y")
        return f"{self.dog}, examined by {self.examinedBy} on: {formatted_date}"


class Kennel(models.Model):
    kennelNum = models.PositiveSmallIntegerField(primary_key=True)
    kennelImage = models.ImageField(upload_to='kennel_pictures',
                                    default=DEFAULT_KENNEL_IMAGE_SOURCE,
                                    null=True, blank=True)

    # Deleting an old image, used in save() below it
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
        return f"Kennel #{self.kennelNum}"

    class Meta:
        ordering = ['kennelNum']


class DogPlacement(models.Model):
    dog = models.ForeignKey('Dog', models.SET_NULL, null=True)
    kennel = models.ForeignKey('Kennel', models.SET_NULL, null=True)
    entranceDate = models.DateField(default=timezone.now)
    expirationDate = models.DateField(blank=True, null=True)
    placementReason = models.CharField(max_length=75, blank=True, null=True)

    # Handling cases where a Kennel or a Dog was deleted, displays "Unknown" instead
    def __str__(self):
        formatted_date = self.entranceDate.strftime("%d-%m-%Y")
        if self.dog is None:
            dog_str = "an unknown dog"
        else:
            dog_str = str(self.dog)
        if self.kennel is None:
            kennel_str = "an unknown kennel"
        else:
            kennel_str = str(self.kennel)

        return f"{dog_str} in {kennel_str} entered on {formatted_date}"

    # Ensures that neither dog nor kennel is None when creating a new DogPlacement instance.
    def save(self, *args, **kwargs):
        if self.dog is None or self.kennel is None:
            raise ValidationError('Dog and Kennel are required fields.')
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

    # References the Observes instance
    observes = models.ForeignKey('Observes', on_delete=models.SET_NULL, null=True)
    obsDateTime = models.DateTimeField(default=timezone.now)
    sessionDurationInMins = models.PositiveIntegerField(default=2,
                                                        validators=[MinValueValidator(0)])
    isKong = models.CharField(max_length=1, choices=IS_KONG_CHOICES, blank=True, null=True, default='N')
    jsonFile = models.FileField(upload_to='json_files',
                                validators=[validate_json_file_extension],
                                null=True, blank=True)
    rawVideo = models.FileField(upload_to='raw_videos',
                                validators=[validate_video_file_extension],
                                null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overridden save method to ensure that:
        - An Observation instance must be associated with an Observes instance.
        - The jsonFile and rawVideo are deleted if replaced upon saving.
        """

        # Ensuring that the Observes instance exists
        if self.observes is None:
            raise ValidationError("An Observation must be associated with an Observes (Session) instance.")

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
        formatted_date = local_time.strftime("%d-%m-%Y at %H:%M")
        observes_str = str(self.observes) if self.observes else "Unknown dog or camera"
        return f"{observes_str}, on {formatted_date}"

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
        ('ELSE', 'And Else'),
    ]

    observation = models.ForeignKey('Observation', on_delete=models.SET_NULL, null=True)
    stanceStartTime = models.TimeField()
    dogStance = models.CharField(max_length=15, choices=DOG_STANCE_CHOICES)
    dogLocation = models.CharField(max_length=10, choices=DOG_LOCATION_CHOICES, blank=True, null=True)

    # Format the date and check if entity contains a valid Observation to display
    def __str__(self):
        formatted_time = self.stanceStartTime.strftime("%H:%M")
        observation_str = str(self.observation) if self.observation else "Unknown observation"
        return f"{observation_str}, starting at {formatted_time}"

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


# News Model for saving the latest website news and displaying them on the homepage
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
