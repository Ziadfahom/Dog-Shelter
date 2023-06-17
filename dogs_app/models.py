from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class Owner(models.Model):
    ownerSerialNum = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50, blank=True, null=True)
    ownerID = models.CharField(max_length=9, blank=True, null=True)
    ownerAddress = models.CharField(max_length=70, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    phoneNum = models.CharField(max_length=9, blank=True, null=True)
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
    dateOfBirthEst = models.DateField(blank=True, null=True)
    dateOfArrival = models.DateField(blank=True, null=True, default=timezone.now)
    dateOfVaccination = models.DateField(blank=True, null=True)
    breed = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    furColor = models.CharField(max_length=20, blank=True, null=True)
    isNeutered = models.CharField(max_length=1, choices=IS_NEUTERED_CHOICES, blank=True, null=True)
    isDangerous = models.CharField(max_length=1, choices=IS_DANGEROUS_CHOICES, blank=True, null=True)
    dogImageURL = models.URLField(max_length=200, blank=True, null=True)
    kongDateAdded = models.DateField(blank=True, null=True)
    ownerSerialNum = models.ForeignKey(Owner, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Owner')

    def __str__(self):
        if self.breed is None:
            return f"{self.dogName}"
        else:
            return f"{self.dogName} the {self.breed}"

    def clean(self):
        if self.dateOfBirthEst and self.dateOfBirthEst > timezone.now().date():
            raise ValidationError("dateOfBirthEst must be before or current date.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Camera(models.Model):
    camID = models.PositiveSmallIntegerField(primary_key=True)

    def __str__(self):
        return f"Camera #{self.camID}"

    class Meta:
        ordering = ['camID']


class Observes(models.Model):
    dogID = models.ForeignKey('Dog', models.CASCADE)
    camID = models.ForeignKey('Camera', models.CASCADE)
    comments = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.camID} on {self.dogID}"

    class Meta:
        verbose_name_plural = "Observes"
        unique_together = (('dogID', 'camID'),)


class Treatment(models.Model):
    treatmentID = models.AutoField(primary_key=True)
    treatmentName = models.CharField(max_length=50)
    treatmentDate = models.DateField(blank=True, null=True)
    treatedBy = models.CharField(max_length=50)
    comments = models.CharField(max_length=250, blank=True, null=True)
    dogID = models.ForeignKey('Dog', models.DO_NOTHING)

    def __str__(self):
        return f"Treatment: '{self.treatmentName}' on {self.dogID}, by {self.treatedBy}"


class EntranceExamination(models.Model):
    examinationID = models.AutoField(primary_key=True)
    examinationDate = models.DateField(default=timezone.now)
    examinedBy = models.CharField(max_length=50)
    results = models.CharField(max_length=100, blank=True, null=True)
    dogWeight = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    dogTemperature = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    dogPulse = models.PositiveSmallIntegerField(blank=True, null=True)
    comments = models.CharField(max_length=200, blank=True, null=True)
    dogID = models.ForeignKey('Dog', models.DO_NOTHING)

    def __str__(self):
        formatted_date = self.examinationDate.strftime("%d-%m-%Y")
        return f"{self.dogID}, examined by {self.examinedBy} on: {formatted_date}"


class Kennel(models.Model):
    kennelNum = models.PositiveSmallIntegerField(primary_key=True)
    kennelImageURL = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Kennel #{self.kennelNum}"

    class Meta:
        ordering = ['kennelNum']


class DogPlacement(models.Model):
    dogID = models.ForeignKey('Dog', models.DO_NOTHING)
    kennelNum = models.ForeignKey('Kennel', models.DO_NOTHING)
    entranceDate = models.DateField(default=timezone.now)
    expirationDate = models.DateField(blank=True, null=True)
    placementReason = models.CharField(max_length=75, blank=True, null=True)

    def __str__(self):
        formatted_date = self.entranceDate.strftime("%d-%m-%Y")
        return f"{self.dogID} in {self.kennelNum} entered on {formatted_date}"

    class Meta:
        unique_together = (('dogID', 'kennelNum', 'entranceDate'),)
        ordering = ['-entranceDate']


class Observation(models.Model):
    IS_KONG_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]

    dogID = models.ForeignKey('Dog', on_delete=models.DO_NOTHING)
    camID = models.ForeignKey('Camera', on_delete=models.DO_NOTHING)
    obsDateTime = models.DateTimeField(default=timezone.now)
    sessionDurationInMins = models.PositiveSmallIntegerField(default=2,
                                                             validators=[MinValueValidator(0), MaxValueValidator(255)])
    isKong = models.CharField(max_length=1, choices=IS_KONG_CHOICES, blank=True, null=True)
    jsonFileURL = models.URLField(max_length=200, blank=True, null=True)
    rawVideoURL = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        formatted_date = self.obsDateTime.strftime("%d-%m-%Y at %H:%M")
        return f"Camera #{self.camID.camID} on {self.dogID.dogName} the {self.dogID.breed}, on {formatted_date}"

    class Meta:
        unique_together = ('dogID', 'camID', 'obsDateTime')
        ordering = ['-obsDateTime']


class DogStance(models.Model):

    DOG_STANCE_CHOICES = [
        ('STANDING', 'Standing'),
        ('SITTING', 'Sitting'),
        ('WALKING_AROUND', 'Walking Around'),
        ('SLEEPING_LYING', 'Sleeping/Lying'),
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
        ('FLOOR', 'Floor'),
        ('BENCH', 'Bench'),
        ('ONBARS', 'On Bars'),
        ('WALLTOWALL', 'Wall to Wall'),
        ('ELSE', 'Else'),
    ]

    dogID = models.ForeignKey('Dog', on_delete=models.DO_NOTHING)
    camID = models.ForeignKey('Camera', on_delete=models.DO_NOTHING)
    obsDateTime = models.ForeignKey('Observation', on_delete=models.DO_NOTHING)
    stanceStartTime = models.TimeField()
    dogStance = models.CharField(max_length=15, choices=DOG_STANCE_CHOICES)
    dogLocation = models.CharField(max_length=10, choices=DOG_LOCATION_CHOICES, blank=True, null=True)

    def __str__(self):
        formatted_date = self.obsDateTime.obsDateTime.strftime("%d-%m-%Y at %H:%M")
        formatted_time = self.stanceStartTime.strftime("%H:%M")
        return f"Camera #{self.camID.camID} on {self.dogID.dogName} the {self.dogID.breed}, on" \
               f" {formatted_date}, starting at {formatted_time}"

    class Meta:
        unique_together = ('dogID', 'camID', 'obsDateTime', 'stanceStartTime')
        ordering = ['-stanceStartTime']

