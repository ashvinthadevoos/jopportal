from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from api.models import User,CandidateProfile,Job,CompanyProfile

class UserSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=User
        fields=["id","username","email","password","role"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)