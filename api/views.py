from django.shortcuts import render
from api.serializers import UserSerializer,CandidateProfileSerializer,CompanyProfileSerializer,JobSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet,GenericViewSet,ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework import authentication,permissions,serializers,views
from api.models import User,CandidateProfile,CompanyProfile,Job,Application
from rest_framework.decorators import action

# from django.contrib.auth.models import AbstractUser,User
# Create your views here.

class UsersView(GenericViewSet,CreateModelMixin):
    serializer_class=UserSerializer
    queryset=User.objects.all()

class CandidateProfileView(ModelViewSet):
    serializer_class=CandidateProfileSerializer
    queryset=CandidateProfile.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return CandidateProfile.objects.filter(user=self.request.user)

        

class CompanyProfileView(ModelViewSet):
    serializer_class=CompanyProfileSerializer
    queryset=CompanyProfile.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return CompanyProfile.objects.filter(user=self.request.user)
        
class JobView(ModelViewSet):
    serializer_class=JobSerializer
    queryset=Job.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        if self.request.user.role == 'employer':
            company=CompanyProfile.objects.get(user=self.request.user)
            serializer.save(company=company)
        else:
            raise serializers.ValidationError("not allowed to perform")
        
    def update(self, request, *args, **kwargs):
        job=self.get_object()
        company=CompanyProfile.objects.get(user=request.user)
        if job.company == company:
            return super().update(request, *args, **kwargs)
        else:
            raise serializers.ValidationError('not allowed to perform')
        
    def get_queryset(self):
        if self.request.user.role == 'employer':
            company=CompanyProfile.objects.get(user=self.request.user)
            return Job.objects.filter(company=company)
        else:
            return super().get_queryset()
        
    def destroy(self, request, *args, **kwargs):
        job=self.get_object()
        if request.user.role == 'employer':
            company=CompanyProfile.objects.get(user=request.user)
            if job.company == company:
                return super().destroy(request,*args,**kwargs)
            else:
                raise serializers.ValidationError('not allowed to perform')
        else:
            raise serializers.ValidationError('not allowed to perform')

    @action(methods=['get'],detail=True)
    def apply(self,request,*args,**kwargs):
        job=self.get_object()
        if request.user.role == 'candidate':
            candidate=CandidateProfile.objects.get(user=request.user)
            Application.objects.create(job=job,candidate=candidate)
            return Response('applied')
        else:
            raise serializers.ValidationError('not allowed to perform')
        
    @action(methods=['get'],detail=True)
    def cancel_application(self,request,*args,**kwargs):
        job=self.get_object()
        if request.user.role == 'candidate':
            candidate=CandidateProfile.objects.get(user=request.user)
            Application.objects.filter(job=job,candidate=candidate).delete()
            return Response('deleted')
        else:
            raise serializers.ValidationError('not allowed to perform')

    @action(methods=['get'],detail=True)
    def application_list(self,request,*args,**kwargs):
        job=self.get_object()
        if request.user.role == 'employer':
            qs=Application.objects.filter(job=job)
            return Response(qs)
        else:
            raise serializers.ValidationError('not allowed to perform')



