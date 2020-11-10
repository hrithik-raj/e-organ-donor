from django.urls import path
from . import views

urlpatterns = [
    path('login', views.BankLogin.as_view(), name='bank-login'),
    path('home/<int:pk>', views.Home.as_view(), name='bank-home'),
    path('add_organs/<int:pk>', views.AddOrgans.as_view(), name='add_organs'),
    path('match/<int:pk>/<int:patient>', views.Matches.as_view(), name='match'),
    path('delete/<int:pk>/<int:patient>', views.delete, name='delete'),
]