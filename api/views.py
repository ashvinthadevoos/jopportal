from django.shortcuts import render
from api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet,GenericViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from api.models import User,AbstractUser

# from django.contrib.auth.models import AbstractUser,User
# Create your views here.

class UsersView(GenericViewSet,CreateModelMixin):
    serializer_class=UserSerializer
    queryset=User.objects.all()