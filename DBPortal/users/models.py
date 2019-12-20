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


class DBerDetail(models.Model):
    aadhar_no = models.CharField(max_length=12)
    user_detail = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    DOB = models.DateField()
    email_address = models.EmailField(null=True)
    linked = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class UserExcel(models.Model):
    file = models.FileField(upload_to='excel_sheets/')


# Create your models here.
