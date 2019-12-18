from django.shortcuts import render, redirect
from .forms import *
from .models import *
import xlsxwriter
import xlrd


def home(request):
    return render(request, 'home.html')


def get_model(name, model):
    obj = model.objects.get(name=name)
    return obj


def register_staff(request):
    if request.method == 'POST':
        u_form = StaffDetailForm(request.POST)
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
                StaffDetail.objects.create(aadhar_no=int(sheet.cell_value(i, 0)),
                                           first_name=sheet.cell_value(i, 1),
                                           last_name=sheet.cell_value(i, 2),
                                           DOB=str(xlrd.xldate_as_datetime(
                                               sheet.cell_value(i, 3), wb.datemode))[0:10],
                                           gender=sheet.cell_value(i, 4),
                                           state=state,
                                           city=city)
            return redirect('home')

    u_form = StaffDetailForm()
    e_form = UserExcelForm()
    context = {
        'u_form': u_form,
        'e_form': e_form,
    }
    return render(request, 'register.html', context)


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
                DBerDetail.objects.create(aadhar_no=int(sheet.cell_value(i, 0)),
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


# Create your views here.
