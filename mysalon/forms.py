from django import forms
from .models import *
from pyuploadcare.dj.forms import ImageField
from django.contrib.auth.models import User


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['user','post']

# class CustomSignupForm(signupForm):
#     first_name = forms.CharField(max_length=30, label='First Name')
#     last_name = forms.CharField(max_length=30, label='Last Name')
#     def signup(self,request,user):
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.save()
#         return user
    
 
