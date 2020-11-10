from django.shortcuts import render, redirect
from django.views import View
from .models import *
from patient.models import Patients, OrganRequirement
from django.contrib import messages

# Errors
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.
class BankLogin(View):
    def get(self, request):
        organ_banks = OrganBank.objects.all()
        context = {'organ_banks': organ_banks}
        return render(request, 'bank/Login.html', context=context)

    def post(self, request):
        branch = request.POST['branch']
        code = request.POST['code']
        branch_id = branch[0]
        branch_details = OrganBank.objects.get(id=branch_id)
        if code == branch_details.code:
            return redirect(f'/banks/home/{branch_id}')

        organ_banks = OrganBank.objects.all()
        context = {'organ_banks': organ_banks, 'error': 'Code did not match'}
        return render(request, 'bank/Login.html', context=context)


class Home(View):
    def get(self, request, pk):
        branch = OrganBank.objects.get(id=pk)
        branch_name = branch.branch_name

        enrolled_list = branch.enrolllist_set.all()

        patient_details = []
        for enrolled in enrolled_list:
            blood_type = Patients.objects.get(patient=enrolled.patient).blood_type
            organ_requirement = OrganRequirement.objects.get(patient=enrolled.patient)
            heart = organ_requirement.heart
            kidney = organ_requirement.kidney
            liver = organ_requirement.liver
            cornea = organ_requirement.cornea
            lung = organ_requirement.lung
            pancreas = organ_requirement.pancreas
            patient_details.append(
                {'id': enrolled.patient.id, 'name': enrolled.patient.first_name, 'blood_type': blood_type,
                 'heart': heart,
                 'kidney': kidney,
                 'liver': liver,
                 'cornea': cornea,
                 'lung': lung,
                 'pancreas': pancreas})

        return render(request, 'bank/index.html',
                      context={'branch_id': pk, 'branch_name': branch_name, 'patient_details': patient_details})

    def post(self, request):
        pass


class Matches(View):
    def get(self, request, pk, patient):
        organ_bank = OrganBank.objects.get(id=pk)
        user = User.objects.get(id=patient)
        organ_requirements_object = OrganRequirement.objects.get(patient=user)
        organ_requirements = organ_requirements_object.get_organ_requirement()
        organs_available = organ_bank.organlist_set.all()
        blood_type = Patients.objects.get(patient=user).blood_type
        blood_group_matches = {}

        for i in organ_requirements:
            blood_group_matches[str(i)] = (False, None)

        for organ_required in organ_requirements:
            for organ in organs_available:
                if blood_type == organ.blood_type:
                    if organ_required == organ.organ_type:
                        if not blood_group_matches[str(organ_required)][0]:
                            blood_group_matches[str(organ_required)] = (True, organ.donor_name)

        context = {'organs_required': organ_requirements, 'matches': blood_group_matches,
                   'username': user.first_name + ' ' + user.last_name}
        return render(request, 'bank/Match.html', context=context)


class AddOrgans(View):
    def get(self, request, pk):
        organ_bank = OrganBank.objects.get(id=pk)
        context = {'branch_name': organ_bank.branch_name, 'branch_id': pk}

        return render(request, 'bank/AddOrgan.html', context=context)

    def post(self, request, pk):
        organ_bank = OrganBank.objects.get(id=pk)
        donor_name = request.POST['donor_name']
        context = {'branch_name': organ_bank.branch_name, 'branch_id': pk, 'fields': request.POST}
        if not donor_name:
            messages.error(request, 'Donor Name Cannot Be Empty')
            return render(request, 'bank/AddOrgan.html', context=context)

        blood_type = request.POST['blood_type']

        if blood_type == '--blood type--':
            messages.error(request, 'Select A Blood Type')
            return render(request, 'bank/AddOrgan.html', context=context)

        try:
            heart = request.POST['heart']
            organ = OrganList.objects.create(organ_bank=organ_bank, organ_type=heart, blood_type=blood_type,
                                             donor_name=donor_name)
            organ.save()
        except MultiValueDictKeyError:
            print("Heart was not selected")
            heart = False

        try:
            kidney = request.POST['kidney']
            organ = OrganList.objects.create(organ_bank=organ_bank, organ_type=kidney, blood_type=blood_type,
                                             donor_name=donor_name)
            organ.save()
        except MultiValueDictKeyError:
            print("Kidney was not selected")
            kidney = False

        try:
            liver = request.POST['liver']
            organ = OrganList.objects.create(organ_bank=organ_bank, organ_type=liver, blood_type=blood_type,
                                             donor_name=donor_name)
            organ.save()
        except MultiValueDictKeyError:
            print("Liver was not selected")
            liver = False

        try:
            cornea = request.POST['cornea']
            organ = OrganList.objects.create(organ_bank=organ_bank, organ_type=cornea, blood_type=blood_type,
                                             donor_name=donor_name)
            organ.save()
        except MultiValueDictKeyError:
            print("Eye was not selected")
            cornea = False

        try:
            lung = request.POST['lung']
            organ = OrganList.objects.create(organ_bank=organ_bank, organ_type=lung, blood_type=blood_type,
                                             donor_name=donor_name)
            organ.save()
        except MultiValueDictKeyError:
            print("Lung was not selected")
            lung = False

        try:
            pancreas = request.POST['pancreas']
            organ = OrganList.objects.create(organ_bank=organ_bank, organ_type=pancreas, blood_type=blood_type,
                                             donor_name=donor_name)
            organ.save()
        except MultiValueDictKeyError:
            print("Pancreas was not selected")
            pancreas = False

        return redirect(f'/banks/home/{pk}')


def delete(request, pk, patient):
    user = User.objects.get(id=patient)
    enrolled_patient = EnrollList.objects.get(patient=user)
    enrolled_patient.delete()

    return redirect(f'/banks/home/{pk}')
