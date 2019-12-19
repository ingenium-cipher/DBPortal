from django.shortcuts import render, redirect
from .forms import *
from .models import *
import xlsxwriter
import xlrd
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.core import exceptions


def home(request):
    return render(request, 'home.html')


def get_model(name, model):
    obj = model.objects.get(name=name)
    return obj


def get_aadhar(number, model):
    obj = model.objects.get(number=number)
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
                state = get_model(sheet.cell_value(i, 5), State)
                city = get_model(sheet.cell_value(i, 6), City)
                AadharNo.objects.create(number=int(sheet.cell_value(i, 0)))
                aadhar = get_aadhar(int(sheet.cell_value(i, 0)), AadharNo)
                DBerDetail.objects.create(aadhar_no=aadhar,
                                          first_name=sheet.cell_value(i, 1),
                                          last_name=sheet.cell_value(i, 2),
                                          DOB=str(xlrd.xldate_as_datetime(
                                              sheet.cell_value(i, 3), wb.datemode))[0:10],
                                          gender=sheet.cell_value(i, 4),
                                          state=state,
                                          city=city)
            return redirect('home')

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
                return HttpResponse("<h1> You are not eligible to login as you are not a staff </h1> <br> <a href = {% url 'home' %} Back to Home </a>")
    return render(request, 'login.html')


def dber_login(request):
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        if(authenticate(username=username, password=password)):
            user = authenticate(username=username, password=password)

            if not user.is_staff:
                login(request, user)
                return redirect('home')

            else:
                return HttpResponse('<h1> You are not eligible to login as you are not a dber </h1> <br>')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def link_dber(request):
    if request.method == 'POST':

        aadhar = request.POST['aadhar']

        try:
            aadhar = get_aadhar(aadhar, AadharNo)
        except exceptions.ObjectDoesNotExist:
            return HttpResponse("<h1> You are not registered!.. Please contact your staff immediately!</h1>")

        dber = DBerDetail.objects.get(aadhar_no=aadhar)
        dber.linked = True
        email = request.POST['dber_email']
        dber.email_address = email
        dber.save()

        return redirect('home')

    return render(request, 'link_dber.html')

# Create your views here.
