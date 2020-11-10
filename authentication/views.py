import json
import os

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views import View
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth

# URL Encoding
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text, force_bytes, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site

from e_Organ_Donor import settings
from .utils import token_generator
from patient.models import Patients, OrganRequirement


# Create your views here.
def admin_logout(request):
    auth.logout(request)
    return redirect('login-view')


class LogoutView(View):
    def get(self, request):
        pass

    def post(self, request):
        auth.logout(request)
        return redirect('login-view')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/Login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            if User.objects.filter(username=username).exists():
                user = auth.authenticate(request, username=username, password=password)
                if user.is_active:
                    auth.login(request, user)
                    return redirect('e_organ_donor')
                messages.error(request, f'{user.username} is not active.')
                return render(request, 'authentication/login.html')
            messages.error(request, f'Account {username} does not exist')
            return render(request, 'authentication/login.html')
        messages.error(request, f'Please fill all fields')
        return render(request, 'authentication/Login.html')


class RegisterView(View):
    def get_states(self):
        file_path = os.path.join(settings.BASE_DIR, 'states.json')

        with open(file_path, 'r') as states:
            json_data = json.load(states)

        states = []

        for k, v in json_data.items():
            states.append({'key': k, 'value': v})

        return states

    def get(self, request):

        context = {
            'states': self.get_states()
        }
        return render(request, 'authentication/Register.html', context=context)

    def post(self, request):
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        mobile = request.POST['phone']
        blood_type = request.POST['blood_type']
        state = request.POST['state']
        city = request.POST['city']
        address = request.POST['address']

        print(username, email, password, mobile, blood_type, state, city, address)

        ready = True

        if not username:
            messages.error(request, 'Username Missing')
            ready = False
        if not email:
            messages.error(request, 'Email is missing')
            ready = False
        if not password:
            messages.error(request, 'Password is missing')
            ready = False
        if not mobile:
            messages.error(request, 'Mobile Number is missing')
            ready = False
        if blood_type == '--blood type--':
            messages.error(request, 'Blood Type is missing')
            ready = False
        if state == '--state--':
            messages.error(request, 'State is missing')
            ready = False
        if not city:
            messages.error(request, 'City is missing')
            ready = False
        if not address:
            messages.error(request, 'Address is missing')
            ready = False

        context = {
            'field_values': request.POST,
            'states': self.get_states(),
        }

        if ready:
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    if not Patients.objects.filter(mobile_number=mobile).exists():
                        user = User.objects.create(username=username, email=email, first_name=first_name,
                                                   last_name=last_name)
                        user.set_password(password)
                        user.is_active = False
                        user.save()

                        patient = Patients.objects.create(patient=user, mobile_number=mobile, blood_type=blood_type,
                                                          city=city, state=state, address=address)
                        patient.save()

                        organ_requirement = OrganRequirement.objects.create(patient=user)
                        organ_requirement.save()

                        # Obtaining Unique ID
                        user_idb64 = urlsafe_base64_encode(force_bytes(user.pk))
                        token = token_generator.make_token(user)

                        # Domain and link
                        domain = get_current_site(request).domain
                        link = reverse('activate', kwargs={'uid_b64': user_idb64, 'token': token})

                        activate_url = 'http://' + domain + link

                        email_subject = 'Account Activation Email'
                        email_body = f'Hi {user.username}, please use this link to verify your account \n {activate_url}'

                        mail = EmailMessage(
                            email_subject,
                            email_body,
                            'pivot_activator@gmail.com',
                            [email],
                        )

                        mail.send(fail_silently=False)

                        return render(request, 'authentication/Registration Success.html')

                    messages.error(request, 'Mobile Number is already in use')
                    return render(request, 'authentication/Register.html', context=context)

                messages.error(request, 'Email is already in use')
                return render(request, 'authentication/Register.html', context=context)

            messages.error(request, 'Username is taken')
            return render(request, 'authentication/Register.html', context=context)
        else:
            return render(request, 'authentication/Register.html', context=context)

        # return render(request, 'authentication/Registration Success.html')


class UsernameValidation(View):
    def post(self, request):
        username = json.loads(request.body)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_already_exists': 'username is taken'}, status=400)
        return JsonResponse({'username_valid': 'username is valid'}, status=200)


class EmailValidation(View):
    def post(self, request):
        email = json.loads(request.body)
        if validate_email(email):
            if User.objects.filter(email=email).exists():
                return JsonResponse({'email_already_exists': 'email is already in use'}, status=400)
            return JsonResponse({'email_valid': 'email is valid'}, status=200)
        else:
            return JsonResponse({'email_invalid': 'email is in an invalid format'}, status=400)


class VerificationView(View):
    def get(self, request, uid_b64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uid_b64))
            user = User.objects.get(id=uid)

            if not token_generator.check_token(user, token):
                messages.error(request, 'Token Already Used')
                return redirect('login-view')

            if user.is_active:
                messages.info(request, 'Account is already activated')
                return redirect('login-view')
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully')
            return redirect('login_view')
        except Exception:
            pass
        return redirect('login-view')


def test_view(request):
    return render(request, 'e_organ_donor/index.html')
