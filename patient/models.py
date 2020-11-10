from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Patients(models.Model):
    TYPES = (
        ('A +ve', 'A+'),
        ('B +ve', 'B+'),
        ('O +ve', 'O+'),
        ('AB +ve', 'AB+'),
        ('A -ve', 'A-'),
        ('B -ve', 'B-'),
        ('O -ve', 'O-'),
        ('AB -ve', 'AB-'),
    )

    patient = models.OneToOneField(to=User, on_delete=models.CASCADE)
    mobile_number = models.CharField(verbose_name='mobile_number', max_length=10, unique=True)
    blood_type = models.CharField(verbose_name='blood_type', max_length=10, blank=True, choices=TYPES)
    city = models.CharField(verbose_name='city', max_length=100, blank=True)
    state = models.CharField(verbose_name='state', max_length=100, blank=True)
    address = models.CharField(verbose_name='address', max_length=500, blank=True)

    class Meta:
        verbose_name_plural = 'Patients'

    def __str__(self):
        return self.patient.username


class OrganRequirement(models.Model):
    patient = models.OneToOneField(to=User, on_delete=models.CASCADE)
    heart = models.BooleanField(default=False)
    kidney = models.BooleanField(default=False)
    liver = models.BooleanField(default=False)
    cornea = models.BooleanField(default=False)
    lung = models.BooleanField(default=False)
    pancreas = models.BooleanField(default=False)

    def __str__(self):
        return self.patient.username

    def get_organ_requirement(self):
        organ_requirements = []
        if self.heart:
            organ_requirements.append('heart')

        if self.kidney:
            organ_requirements.append('kidney')

        if self.liver:
            organ_requirements.append('liver')

        if self.cornea:
            organ_requirements.append('cornea')

        if self.lung:
            organ_requirements.append('lung')

        if self.pancreas:
            organ_requirements.append('pancreas')

        return organ_requirements
