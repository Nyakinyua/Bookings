from django import forms
from .models import *
from pyuploadcare.dj.forms import ImageField
from django.contrib.auth.models import User


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['user','post']
        
        
class CreateAppointmentForm(forms.ModelForm):
    class Meta:
        
        model = Appointment
        fields = ("schedule","stylistName",)