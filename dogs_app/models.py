import os

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

# Video File Validator, raises an error if the file is not a video
def validate_video_file_extension(value):
    # List of allowed video file extensions, as defined in settings files
    from dogshelter_site.settings.base import ALLOWED_VIDEO_FILE_EXTENSIONS
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ALLOWED_VIDEO_FILE_EXTENSIONS
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported video file extension.')

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

    ENTRY_REASON_CHOICES = [
        ('STRAY', 'Stray'),
        ('BITE', 'Bite'),
        ('RETURN', 'Returning'),
        ('ELSE', 'Else'),
        ('', '-')
    ]

    COLOR_GROUP_CHOICES = [
        ('P', 'Purple'),
        ('O', 'Orange'),
        ('G', 'Green'),
        ('PO', 'Purple/Orange'),
        ('', '-')
    ]

    MOTIVATION_GROUP_CHOICES = [
        ('EXTERNALLY', 'Externally'),
        ('INTERNALLY', 'Internally'),
        ('SOCIALLY', 'Socially'),
        ('', '-')
    ]

    dogID = models.AutoField(primary_key=True)
    dogImage = models.ImageField(upload_to='dog_pictures', default=DEFAULT_DOG_IMAGE_SOURCE, null=True, blank=True)
    chipNum = models.CharField(max_length=30, unique=True, blank=True, null=True)
    dogName = models.CharField(max_length=35)
    city = models.CharField(max_length=30, blank=True, null=True)
    dateOfArrival = models.DateField(blank=True, null=True, default=current_timezone_aware_date)
    entryReason = models.CharField(max_length=10, choices=ENTRY_REASON_CHOICES, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    breed = models.CharField(max_length=30, blank=True, null=True)
    furColor = models.CharField(max_length=20, blank=True, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Owner')
    dateOfBirthEst = models.DateField(blank=True, null=True)
    dateOfVaccination = models.DateField(blank=True, null=True)
    isNeutered = models.CharField(max_length=1, choices=IS_NEUTERED_CHOICES, blank=True, null=True)
    isDangerous = models.CharField(max_length=1, choices=IS_DANGEROUS_CHOICES, blank=True, null=True)
    kongDateAdded = models.DateField(blank=True, null=True, verbose_name='Last Date Given a Kong', default=None)
    adoptionDate = models.DateField(blank=True, null=True, verbose_name='Adoption Date', default=None)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, verbose_name='Branch')

    releaseDate = models.DateField(blank=True, null=True)
    releaseReason = models.CharField(max_length=50, blank=True, null=True)
    releaseDetails = models.CharField(max_length=250, blank=True, null=True)
    dogImage2 = models.ImageField(upload_to='dog_pictures', null=True, blank=True)
    dogImage3 = models.ImageField(upload_to='dog_pictures', null=True, blank=True)
    dogImage4 = models.ImageField(upload_to='dog_pictures', null=True, blank=True)
    dogVideo = models.FileField(upload_to='dog_videos',
                                validators=[validate_video_file_extension],
                                null=True, blank=True, verbose_name='Video')
    # Attributes matching Lod's MYM (Meet Your Match) requirements
    colorGroup = models.CharField(max_length=2, choices=COLOR_GROUP_CHOICES, blank=True, null=True)
    motivationGroup = models.CharField(max_length=10, choices=MOTIVATION_GROUP_CHOICES, blank=True, null=True)

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

        # Check if the instance being saved is a new one or an existing one
        if self.pk:
            old_dogImage = Dog.objects.get(pk=self.pk).dogImage
            old_dogImage2 = Dog.objects.get(pk=self.pk).dogImage2
            old_dogImage3 = Dog.objects.get(pk=self.pk).dogImage3
            old_dogImage4 = Dog.objects.get(pk=self.pk).dogImage4
            old_dogVideo = Dog.objects.get(pk=self.pk).dogVideo

            # Check if images/video are being replaced
            if old_dogImage and self.dogImage != old_dogImage and old_dogImage != DEFAULT_DOG_IMAGE_SOURCE:
                old_dogImage.delete(save=False)
            if old_dogImage2 and self.dogImage2 != old_dogImage2:
                old_dogImage2.delete(save=False)
            if old_dogImage3 and self.dogImage3 != old_dogImage3:
                old_dogImage3.delete(save=False)
            if old_dogImage4 and self.dogImage4 != old_dogImage4:
                old_dogImage4.delete(save=False)
            if old_dogVideo and self.dogVideo != old_dogVideo:
                old_dogVideo.delete(save=False)

        super().save(*args, **kwargs)

    # Make sure the dog's images and video are deleted upon deletion of the Dog instance
    def delete(self, *args, **kwargs):

        # Delete the Image/Video files from the storage if they exist
        if self.dogImage and self.dogImage != DEFAULT_DOG_IMAGE_SOURCE:
            self.dogImage.delete(save=False)
        if self.dogImage2:
            self.dogImage2.delete(save=False)
        if self.dogImage3:
            self.dogImage3.delete(save=False)
        if self.dogImage4:
            self.dogImage4.delete(save=False)
        if self.dogVideo:
            self.dogVideo.delete(save=False)

        super(Dog, self).delete(*args, **kwargs)

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

    def delete(self, *args, **kwargs):
        # Make sure all dogs that are associated with this camera
        # through Observes have their kongDateAdded updated if needed
        try:
            local_tz = pytz.timezone('Asia/Jerusalem')
            dog_ids_list = []
            for observes_instance in Observes.objects.filter(camera=self):
                if observes_instance.dog and observes_instance.dog.pk not in dog_ids_list:
                    dog_instance = observes_instance.dog
                    # Find the latest observation with isKong='Y' for this dog
                    latest_observation = Observation.objects.filter(
                        observes__dog=dog_instance,
                        isKong='Y'
                    ).exclude(observes__camera=self).order_by('-obsDateTime').first()
                    if latest_observation:
                        # Convert the new obsDateTime to the local timezone
                        new_obsDateTime_instance = timezone.localtime(latest_observation.obsDateTime, local_tz)
                        dog_instance.kongDateAdded = new_obsDateTime_instance.date()
                    else:
                        dog_instance.kongDateAdded = None
                    dog_instance.save()
                    dog_ids_list.append(dog_instance.pk)
            super(Camera, self).delete(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred while updating the Dog's kongDateAdded field: {e}")

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

    def save(self, *args, **kwargs):
        # To ensure both values are always given by a user before changes.
        # They can only be blank because of deletion of Dog or Camera entities
        if self.dog is None or self.camera is None:
            raise ValidationError('Dog and Camera are required fields.')

        # Ensure that if the user is changing the dog, their kongDateAdded is updated accordingly
        if self.pk:
            try:
                old_instance = Observes.objects.get(pk=self.pk)
                if old_instance.dog and self.dog and old_instance.dog_id != self.dog_id:
                    local_tz = pytz.timezone('Asia/Jerusalem')
                    # Hold the current Observes instance's latest obsDateTime value
                    observes_observation_set = old_instance.observation_set.filter(isKong='Y')
                    if observes_observation_set.exists():
                        current_obsDateTime = observes_observation_set.order_by('-obsDateTime').first().obsDateTime
                        if current_obsDateTime:
                            current_obsDateTime = timezone.localtime(current_obsDateTime, local_tz).date() if current_obsDateTime else None

                    else:
                        current_obsDateTime = None

                    # Find the latest valid observation for the old dog
                    latest_observation_old_dog = Observation.objects.filter(
                        observes__dog=old_instance.dog, isKong='Y'
                    ).exclude(observes=old_instance).order_by('-obsDateTime').first()
                    if latest_observation_old_dog:
                        old_dog_kongDate = timezone.localtime(latest_observation_old_dog.obsDateTime, local_tz).date()
                        old_instance.dog.kongDateAdded = old_dog_kongDate
                    else:
                        old_instance.dog.kongDateAdded = None
                    old_instance.dog.save()

                    # Find the latest valid observation for the new dog
                    new_dog_kongDate = self.dog.kongDateAdded
                    # Compare the new kongDateAdded to the dog's kongDateAdded field and update it if necessary
                    if current_obsDateTime and (not new_dog_kongDate or current_obsDateTime > new_dog_kongDate):
                        self.dog.kongDateAdded = current_obsDateTime
                        self.dog.save()
            except Dog.DoesNotExist:
                pass
            except Dog.MultipleObjectsReturned:
                pass
            except Exception as e:
                print(f"An error occurred while updating the Dog's kongDateAdded field: {e}")
        super(Observes, self).save(*args, **kwargs)

    # Ensure that upon deletion of an Observes instance, the Dog's kongDateAdded field is handled correctly
    def delete(self, *args, **kwargs):
        try:
            dog_instance = self.dog
            # Fetch the latest observation with isKong='Y' from this Observes instance
            latest_session_observation = self.observation_set.filter(isKong='Y').order_by('-obsDateTime').first()
            if latest_session_observation and latest_session_observation.obsDateTime:
                # Convert its obsDateTime to the local timezone
                local_tz = pytz.timezone('Asia/Jerusalem')
                latest_obsDateTime_instance = timezone.localtime(latest_session_observation.obsDateTime, local_tz)

                # Compare to the dog's kongDateAdded field and update it if necessary
                if latest_session_observation and latest_obsDateTime_instance.date() == dog_instance.kongDateAdded:
                    # Find the latest Observation with isKong='Y' for this dog excluding from this Observes instance
                    new_latest_observation = Observation.objects.filter(
                        observes__dog=dog_instance,
                        isKong='Y'
                    ).exclude(observes=self).order_by('-obsDateTime').first()
                    if new_latest_observation:
                        # Convert the new obsDateTime to the local timezone
                        new_obsDateTime_instance = timezone.localtime(new_latest_observation.obsDateTime, local_tz)
                        dog_instance.kongDateAdded = new_obsDateTime_instance.date()
                    else:
                        dog_instance.kongDateAdded = None
                    dog_instance.save()
            super(Observes, self).delete(*args, **kwargs)
        except Dog.DoesNotExist:
            pass
        except Dog.MultipleObjectsReturned:
            pass
        except Exception as e:
            print(f"An error occurred while updating the Dog's kongDateAdded field: {e}")

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


# CSV File validator, raises an error if the file is not a CSV
def validate_csv_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.csv']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. File should have a valid .csv format.')


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
                              default='N', verbose_name='With Toy')
    isDog = models.CharField(max_length=1, choices=IS_DOG_CHOICES,
                             blank=True, null=True,
                             default=None, verbose_name='With Dog')
    isHuman = models.CharField(max_length=1, choices=IS_HUMAN_CHOICES,
                               blank=True, null=True,
                               default=None, verbose_name='With Human')
    jsonFile = models.FileField(upload_to='json_files',
                                validators=[validate_json_file_extension],
                                null=True, blank=True, verbose_name='JSON File')
    csvFile = models.FileField(upload_to='csv_files',
                               validators=[validate_csv_file_extension],
                               null=True, blank=True, verbose_name='Sensory Data')
    rawVideo = models.FileField(upload_to='raw_videos',
                                validators=[validate_video_file_extension],
                                null=True, blank=True, verbose_name='Video')
    original_csv_file_name = models.CharField(max_length=255,
                                              blank=True, null=True, default=None,
                                              verbose_name='Original File Name')
    original_video_file_name = models.CharField(max_length=255,
                                                blank=True, null=True, default=None,
                                                verbose_name='Original Video File Name')

    # Returns the latest observation with isKong='Y' for this dog excluding this one
    def get_latest_observation(self):
        if self.observes.dog:
            latest_observation = Observation.objects.filter(
                observes__dog=self.observes.dog,
                isKong='Y'
            ).exclude(pk=self.pk).order_by('-obsDateTime').first()
            if latest_observation:
                return latest_observation
            else:
                return None
        else:
            return None

    def save(self, *args, **kwargs):
        """
        Overridden save method to ensure that:
        - An Observation instance must be associated with an Observes instance.
        - The jsonFile and rawVideo are deleted if replaced upon saving.
        - The Dog's kongDateGiven field is updated if the isKong field is
        set to 'Y' and the obsDateTime is later than that date.
        """

        # Ensure original CSV file name is stored for display purposes
        if self.csvFile:
            # New entity being added, store the original CSV file name
            if not self.pk:
                self.original_csv_file_name = self.csvFile.name
            # Existing entity being edited, check if the csvFile is replaced as well to adjust stored name
            elif self.csvFile != Observation.objects.get(pk=self.pk).csvFile:
                self.original_csv_file_name = self.csvFile.name

        # Ensure original Video file name is stored for display purposes
        if self.rawVideo:
            # New entity being added, store the original Video file name
            if not self.pk:
                self.original_video_file_name = self.rawVideo.name
            # Existing entity being edited, check if the video file is replaced as well to adjust stored name
            elif self.rawVideo != Observation.objects.get(pk=self.pk).rawVideo:
                self.original_video_file_name = self.rawVideo.name

        # Ensuring that the Observes instance exists
        if self.observes is None:
            raise ValidationError("An Observation must be associated with a Session instance.")

        self.full_clean()

        # Check if the instance being saved is a new one or an existing one
        if self.pk:
            old_file_json = Observation.objects.get(pk=self.pk).jsonFile
            old_file_video = Observation.objects.get(pk=self.pk).rawVideo
            old_file_csv = Observation.objects.get(pk=self.pk).csvFile

            # Check if jsonFile is replaced
            if old_file_json and self.jsonFile != old_file_json:
                old_file_json.delete(save=False)

            # Check if rawVideo is replaced
            if old_file_video and self.rawVideo != old_file_video:
                old_file_video.delete(save=False)

            # Check if csvFile is replaced
            if old_file_csv and self.csvFile != old_file_csv:
                old_file_csv.delete(save=False)

        local_tz = pytz.timezone('Asia/Jerusalem')
        new_obsDateTime = timezone.localtime(self.obsDateTime, local_tz).date()
        try:
            # Get current dog instance
            current_dog_instance = self.observes.dog if self.observes and self.observes.dog else None

            # Variables to track if there is a change in Dog
            old_dog_instance = None
            dog_changed = False

            # Check if this is an existing instance and if Dog has changed
            if self.pk:
                current_instance = Observation.objects.get(pk=self.pk)
                old_dog_instance = current_instance.observes.dog if current_instance.observes and current_instance.observes.dog else None
                if old_dog_instance != current_dog_instance:
                    dog_changed = True

            # Logic for new instances or instances where isKong remains 'N'
            if not self.pk and self.isKong == 'Y' and current_dog_instance:
                if not current_dog_instance.kongDateAdded or new_obsDateTime > current_dog_instance.kongDateAdded:
                    current_dog_instance.kongDateAdded = new_obsDateTime
                    current_dog_instance.save()

            # If editing an existing instance, compare old and new values
            elif self.pk and current_dog_instance:
                current_isKong = self.isKong
                old_instance = Observation.objects.get(pk=self.pk)
                old_isKong = old_instance.isKong
                old_obsDateTime = timezone.localtime(old_instance.obsDateTime, local_tz).date()

                # Update logic when isKong or obsDateTime changes
                if old_isKong != current_isKong or old_obsDateTime != new_obsDateTime:
                    if current_isKong == 'Y' and (
                            not current_dog_instance.kongDateAdded or new_obsDateTime > current_dog_instance.kongDateAdded):
                        current_dog_instance.kongDateAdded = new_obsDateTime
                    elif old_isKong == 'Y' and old_obsDateTime == current_dog_instance.kongDateAdded:
                        latest_observation = self.get_latest_observation()
                        current_dog_instance.kongDateAdded = timezone.localtime(latest_observation.obsDateTime,
                                                                                local_tz).date() if latest_observation else None
                    current_dog_instance.save()

            # Handle the case where the Dog has changed
            if dog_changed and old_dog_instance:
                # Update old dog's kongDateAdded
                latest_observation_old_dog = Observation.objects.filter(
                    observes__dog=old_dog_instance,
                    isKong='Y'
                ).exclude(pk=self.pk).order_by('-obsDateTime').first()
                old_dog_new_kongDate = timezone.localtime(latest_observation_old_dog.obsDateTime,
                                                          local_tz).date() if latest_observation_old_dog else None
                if old_dog_instance.kongDateAdded != old_dog_new_kongDate:
                    old_dog_instance.kongDateAdded = old_dog_new_kongDate
                    old_dog_instance.save()

            # Update new dog's kongDateAdded
            if current_dog_instance and self.isKong == 'Y':
                if not current_dog_instance.kongDateAdded or current_dog_instance.kongDateAdded < new_obsDateTime:
                    current_dog_instance.kongDateAdded = new_obsDateTime
                    current_dog_instance.save()

        except Dog.DoesNotExist:
            raise ValidationError("The Dog associated with this Observation does not exist.")
        except Dog.MultipleObjectsReturned:
            raise ValidationError("Multiple Dogs are associated with this Observation.")
        except Exception as e:
            print(f"An error occurred while updating the Dog's kongDateAdded field: {e}")
            raise ValidationError(f"An error occurred while updating the Dog's kongDateAdded field: {e}")
        super().save(*args, **kwargs)

    # Make sure the dog's kongDateAdded is updated if the isKong field is set to 'Y'
    # and the obsDateTime is equal to this one's
    def delete(self, *args, **kwargs):

        # Delete the CSV file from the storage if it exists
        if self.csvFile:
            self.csvFile.delete(save=False)

        # Delete the Video file from the storage if it exists
        if self.rawVideo:
            self.rawVideo.delete(save=False)

        # Check if the dog's kongDateAdded field needs to be updated
        if self.isKong == 'Y':
            try:
                dog_instance = self.observes.dog if self.observes.dog else None
                if dog_instance:
                    # Convert the obsDateTime to the local timezone
                    local_tz = pytz.timezone('Asia/Jerusalem')
                    obsDateTime_instance = timezone.localtime(self.obsDateTime, local_tz)

                    if dog_instance.kongDateAdded and obsDateTime_instance.date() == dog_instance.kongDateAdded:
                        # Find the latest observation with isKong='Y' for this dog
                        latest_observation = self.get_latest_observation()

                        if latest_observation:
                            # Convert the new obsDateTime to the local timezone
                            new_obsDateTime_instance = timezone.localtime(latest_observation.obsDateTime, local_tz)
                            dog_instance.kongDateAdded = new_obsDateTime_instance.date()
                        else:
                            dog_instance.kongDateAdded = None
                        dog_instance.save()
            except Dog.DoesNotExist:
                pass
            except Dog.MultipleObjectsReturned:
                pass
            except Exception as e:
                print(f"An error occurred while updating the Dog's kongDateAdded field: {e}")
        super(Observation, self).delete(*args, **kwargs)

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
        ('ONBED', 'On Bed'),
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


# Choice model for the Poll model
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
    branchAddress = models.CharField(max_length=100, blank=True, null=True, verbose_name='Branch Address')
    branchCity = models.CharField(max_length=50, blank=True, null=True, verbose_name='Branch City')

    # Add more fields later if needed
    # branchPhone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Branch Phone Number')
    # branchEmail = models.EmailField(max_length=50, blank=True, null=True, verbose_name='Branch Email')
    # branchManager = models.CharField(max_length=50, blank=True, null=True, verbose_name='Branch Manager')

    def __str__(self):
        return f"{self.branchName}"

    class Meta:
        verbose_name_plural = "Branch"
