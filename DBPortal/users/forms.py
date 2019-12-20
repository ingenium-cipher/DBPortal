from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class StaffDetailForm(forms.ModelForm):

    class Meta:
        model = StaffDetail
        fields = ('staff_user', )


class DBerDetailForm(forms.ModelForm):

    class Meta:
        model = DBerDetail
        fields = ('aadhar_no', 'name', 'DOB', 'gender', 'state', 'city')


class UserExcelForm(forms.ModelForm):

    class Meta:
        model = UserExcel
        fields = ('file',)


class DBerUserDetailForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
