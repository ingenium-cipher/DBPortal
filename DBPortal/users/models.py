from django.db import models
from django.contrib.auth.models import User
import datetime

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('O', 'Others'))


class State(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class StaffDetail(models.Model):
    aadhar_no = models.CharField(max_length=12)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    DOB = models.DateField(max_length=8, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.first_name


class DBerDetail(models.Model):
    aadhar_no = models.CharField(max_length=12)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    DOB = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.first_name


class UserExcel(models.Model):
    file = models.FileField(upload_to='excel_sheets/')


# Create your models here.
