from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('saml/acs/', views.saml_acs, name='saml_acs'),
    path('saml/login/', views.saml_login, name='saml_login'),
    path('saml/logout/', views.saml_logout, name='saml_logout'),
    
]
