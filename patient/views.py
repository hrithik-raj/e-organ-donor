from django.shortcuts import render, redirect
from django.views import View
from .models import OrganRequirement
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from main.models import EnrollList, OrganBank

from django.contrib import messages
import json


# Create your views here.
class UpdateOrganRequirement(View):
    def post(self, request):
        user = request.user
        organ_requirements = OrganRequirement.objects.get(patient=user)
        data = json.loads(request.body)
        organ = data['organ']

        if organ == 'heart':
            if organ_requirements.heart:
                organ_requirements.heart = False
            else:
                organ_requirements.heart = True

        if organ == 'liver':
            if organ_requirements.liver:
                organ_requirements.liver = False
            else:
                organ_requirements.liver = True

        if organ == 'kidney':
            if organ_requirements.kidney:
                organ_requirements.kidney = False
            else:
                organ_requirements.kidney = True

        if organ == 'eye':
            if organ_requirements.cornea:
                organ_requirements.cornea = False
            else:
                organ_requirements.cornea = True

        if organ == 'lungs':
            if organ_requirements.lung:
                organ_requirements.lung = False
            else:
                organ_requirements.lung = True

        if organ == 'pancreas':
            if organ_requirements.pancreas:
                organ_requirements.pancreas = False
            else:
                organ_requirements.pancreas = True

        organ_requirements.save()

        print(organ)

        return JsonResponse({'Success': 'Organ Added'}, status=200)


@login_required(login_url='/authentication/login')
def HomePage(request):
    user = request.user
    if user.is_superuser:
        return redirect('admin-logout-view')
    organ_requirements = OrganRequirement.objects.get(patient=user)

    context = {'user': request.user, 'organ_requirements': organ_requirements, 'page': 'dashboard'}
    return render(request, 'e_organ_donor/index.html', context=context)


def apply(request):
    user = request.user
    organ_banks = OrganBank.objects.all()

    context = {'organ_banks': organ_banks}
    if request.method == 'POST':
        organ_bank = request.POST['organ_bank']
        selected = OrganBank.objects.get(branch_name=organ_bank)
        enrolled_list = selected.enrolllist_set.all()

        for i in enrolled_list:
            if i.patient == user:
                messages.error(request, 'You have already been Enrolled')
                return render(request, 'e_organ_donor/Apply.html', context=context)

        new_enrollment = EnrollList.objects.create(organ_bank=selected, patient=user)
        new_enrollment.save()

        return redirect('e_organ_donor')
    if request.method == 'GET':
        return render(request, 'e_organ_donor/Apply.html', context=context)


def about(request):
    context = {'page': 'about'}
    return render(request, 'e_organ_donor/About.html', context=context)


def contact(request):
    context = {'page': 'contact'}
    return render(request, 'e_organ_donor/Contact.html', context=context)
