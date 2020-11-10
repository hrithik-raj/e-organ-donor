from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name="login-view"),
    path('logout', views.LogoutView.as_view(), name="logout-view"),
    path('admin-logout', views.admin_logout, name="admin-logout-view"),
    path('register', views.RegisterView.as_view(), name="register-view"),
    path('username_validation', csrf_exempt(views.UsernameValidation.as_view()), name="username-validation"),
    path('email_validation', csrf_exempt(views.EmailValidation.as_view()), name="email-validation"),
    path('activate/<uid_b64>/<token>', views.VerificationView.as_view(), name='activate'),

    path('test', views.test_view, name='test'),
]