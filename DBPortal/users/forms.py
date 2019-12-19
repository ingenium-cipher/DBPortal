from django import forms
from .models import *


# class StaffDetailForm(forms.ModelForm):
#
#     class Meta:
#         model = StaffDetail
#         fields = ('aadhar_no', 'first_name', 'last_name', 'DOB', 'gender', 'state', 'city')


class DBerDetailForm(forms.ModelForm):

    class Meta:
        model = DBerDetail
        fields = ('aadhar_no', 'first_name', 'last_name', 'DOB', 'gender', 'state', 'city')


class UserExcelForm(forms.ModelForm):

    class Meta:
        model = UserExcel
        fields = ('file',)
