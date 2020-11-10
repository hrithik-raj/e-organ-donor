from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.HomePage, name='e_organ_donor'),
    path('update_organ_requirement', csrf_exempt(views.UpdateOrganRequirement.as_view()),
         name='update_organ_requirement'),
    path('apply', views.apply, name='apply_view'),
    path('about', views.about, name='about_view'),
    path('contact', views.contact, name='contact_view'),
]
