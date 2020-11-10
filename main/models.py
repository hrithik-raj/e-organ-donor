from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class OrganBank(models.Model):
    branch_name = models.CharField(max_length=60)
    contact_number = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.branch_name


class EnrollList(models.Model):
    organ_bank = models.ForeignKey(OrganBank, on_delete=models.CASCADE)
    patient = models.OneToOneField(to=User, on_delete=models.CASCADE)
    enroll_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.patient.username

    class Meta:
        ordering: ['-enroll_date']


class OrganList(models.Model):
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
    organ_bank = models.ForeignKey(OrganBank, on_delete=models.CASCADE)
    organ_type = models.CharField(max_length=20)
    blood_type = models.CharField(max_length=10, blank=True, choices=TYPES)
    donor_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.organ_type + ' ' + str(self.blood_type)
