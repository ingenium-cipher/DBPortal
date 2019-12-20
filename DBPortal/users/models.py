from django.db import models
from django.contrib.auth.models import User
import datetime
from rest_framework.permissions import IsAdminUser

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


class StaffDetail(models.Model):

    staff_user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_address = models.EmailField(null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{x} for city {y}".format(x=self.staff_user, y=self.city)


# Create your models here.
