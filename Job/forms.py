from django import forms
from django.contrib.auth.models import AbstractUser
from api.models import CandidateProfile,CompanyProfile,User,Job
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):

    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2","role"]


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class CandidateProfileForm(forms.ModelForm):

    class Meta:
        model=CandidateProfile
        fields=["phone","image","gender","qualification","resume","location","ready_to_relocate","skills","experience"]

class CompanyProfileForm(forms.ModelForm):

    class Meta:
        model=CompanyProfile
        fields=["phone","logo","description","location","adress","company_name"]

class JobForm(forms.ModelForm):

    class Meta:
        model=Job
        fields=["start_date","end_date","title","salary","description","qualification","experience","location","skills"]

# class ApplicationForm(forms.ModelForm):
    
#     class Meta:
#         model=Application
#         fields=["options"]