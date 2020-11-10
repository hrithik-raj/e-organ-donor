from django.contrib import admin
from .models import Patients, OrganRequirement

# Register your models here.
admin.site.register(Patients)
admin.site.register(OrganRequirement)
