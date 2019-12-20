from django.shortcuts import render, redirect
from .forms import *
from .models import *
import xlsxwriter
import xlrd
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.core import exceptions
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def home(request):
    return render(request, 'home.html')


def get_model(name, model):
    obj = model.objects.get(name=name)
    return obj


def register_dber(request):
    if request.method == 'POST':
        u_form = DBerDetailForm(request.POST)
        e_form = UserExcelForm(request.POST, request.FILES)
        if u_form.is_valid():
            u_form.save()
            return redirect('home')

        elif e_form.is_valid():
            sa = e_form.save()
            loc = ("/home/ayush/Desktop/github/DBPortal/DBPortal" + sa.file.url)

            wb = xlrd.open_workbook(loc)
            sheet = wb.sheet_by_index(0)

            for i in range(1, sheet.nrows):
                state = get_model(sheet.cell_value(i, 4), State)
                city = get_model(sheet.cell_value(i, 5), City)
                DBerDetail.objects.create(aadhar_no=int(sheet.cell_value(i, 0)),
                                          name=sheet.cell_value(i, 1),
                                          DOB=str(xlrd.xldate_as_datetime(
                                              sheet.cell_value(i, 2), wb.datemode))[0:10],
                                          gender=sheet.cell_value(i, 3),
                                          state=state,
                                          city=city)
            return redirect('home')

        elif not (u_form.is_valid() or e_form.is_valid()):
            context = {
                'form': u_form
            }
            return render(request, 'error.html', context)

    u_form = DBerDetailForm()
    e_form = UserExcelForm()
    context = {
        'u_form': u_form,
        'e_form': e_form,
    }
    return render(request, 'register.html', context)


def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})


def staff_login(request):
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        if(authenticate(username=username, password=password)):
            user = authenticate(username=username, password=password)

            if user.is_staff:
                login(request, user)
                return redirect('home')

            else:
                return HttpResponse('<h1> You are not eligible to login as you are not a staff </h1> <br> <a href = "http://127.0.0.1:8000/"> Back to Home </a>')
    return render(request, 'login.html')


def dber_login(request):
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        if(authenticate(username=username, password=password)):
            user = authenticate(username=username, password=password)

            try:
                DBerDetail.objects.get(user_detail=user)
                login(request, user)
                return redirect('home')

            except exceptions.ObjectDoesNotExist:
                return HttpResponse('<h1> You are not eligible to login due to following reasons </h1> <br> <ul> <li> Maybe because you are not a dber </li> <li> Maybe you are not linked as dber </li> </ul> <a href = "http://127.0.0.1:8000/"> Back to Home </a>')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def link_dber(request):

    if request.method == 'POST':

        aadhar = request.POST['aadhar']

        try:
            dber = DBerDetail.objects.get(aadhar_no=aadhar)
        except exceptions.ObjectDoesNotExist:
            return HttpResponse("<h1> You are not registered!.. Please contact your staff immediately!</h1>")

        dber = DBerDetail.objects.get(aadhar_no=aadhar)
        dber.linked = True
        email = request.POST['dber_email']
        dber.email_address = email
        dber.save()
        form = DBerUserDetailForm(request.POST)

        if form.is_valid():
            fo = form.save()
            obj = User.objects.get(username=fo)
            dber.user_detail = obj
            dber.save()

        else:
            return HttpResponse("<h1> {{ form.errors }}</h1>")

        return redirect('home')

    form = DBerUserDetailForm()
    context = {
        'form': form
    }
    return render(request, 'link_dber.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })
# Create your views here.
