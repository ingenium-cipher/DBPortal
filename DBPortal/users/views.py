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
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from DBPortal.settings import *


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
            print(sa.file.url[6:])
            print(MEDIA_ROOT)
            # loc = ("/home/ayush/Desktop/github/DBPortal/DBPortal" + sa.file.url)
            loc = (MEDIA_ROOT + sa.file.url[6:])

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
            return render(request, 'error.html', {'form': form})

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


def email(request):
    staff = StaffDetail.objects.get(staff_user=request.user)
    users = DBerDetail.objects.filter(linked=True, city=staff.city)
    recipient_list = []

    from_email = staff.email_address

    if request.method == 'POST':

        subject = request.POST['subject']
        message = request.POST['message']
        checkbox = request.POST.getlist('checkbox')
        checkbox = tuple(checkbox)

        for i in range(0, len(checkbox)):
            recipient_list.append(checkbox[i])

        send_mail(subject, message, from_email, recipient_list)
        return redirect('home')

    context = {
        'users': users,
        'from_email': from_email,
        'staff': staff,
    }
    return render(request, 'email.html', context)


def send_dber_email(request):

    if request.user.is_staff:
        global user_1
        global from_email
        user_1 = StaffDetail.objects.get(staff_user=request.user)
        from_email = user_1.email_address

    else:
        user_1 = DBerDetail.objects.get(user_detail=request.user)
        from_email = user_1.email_address
    to_email = []

    context = {
        'from_email': from_email,
        'user_1': user_1,
    }

    if request.method == 'POST':

        if 'sea' in request.POST:
            search = request.POST['search']
            print(search)

            try:
                global to_dber
                to_dber = DBerDetail.objects.get(name=search, linked=True)
                context['to_dber'] = to_dber
                return render(request, 'send_dber_email.html', context)
            except exceptions.ObjectDoesNotExist:
                try:
                    to_dber = DBerDetail.objects.get(aadhar_no=search, linked=True)
                    context['to_dber'] = to_dber
                    return render(request, 'send_dber_email.html', context)
                except exceptions.ObjectDoesNotExist:
                    try:
                        to_dber = DBerDetail.objects.get(email_address=search, linked=True)
                        context['to_dber'] = to_dber
                        return render(request, 'send_dber_email.html', context)
                    except exceptions.ObjectDoesNotExist:
                        messages.error(request, 'This DBer does not exist')

        elif 'sen' in request.POST:
            subject = request.POST['subject']
            message = request.POST['message']
            to_email.append(to_dber.email_address)
            send_mail(subject, message, from_email, to_email)
            return redirect('home')

    return render(request, 'send_dber_email.html', context)


def send_staff_email(request):

    global from_email
    to_email = []

    if request.user.is_staff:
        from_email = request.user.email
    else:
        from_email = DBerDetail.objects.get(user_detail=request.user).email_address

    context = {
        'from_email': from_email,
    }

    if request.method == 'POST':

        if 'sea' in request.POST:
            search = request.POST['search']

            try:
                global staff
                user = User.objects.get(username=search)
                staff = StaffDetail.objects.get(staff_user=user)
                context['staff'] = staff
                return render(request, 'send_staff_email.html', context)
            except exceptions.ObjectDoesNotExist:
                try:
                    staff = StaffDetail.objects.get(email_address=search)
                    context['staff'] = staff
                    return render(request, 'send_staff_email.html', context)
                except exceptions.ObjectDoesNotExist:
                    messages.error(request, 'This Staff does not exist')

        elif 'sen' in request.POST:
            subject = request.POST['subject']
            message = request.POST['message']
            print('hi')
            to_email.append(staff.email_address)
            send_mail(subject, message, from_email, to_email)
            return redirect('home')

    return render(request, 'send_staff_email.html', context)


@login_required
def profile(request):

    if request.user.is_staff:
        user_1 = StaffDetail.objects.get(staff_user=request.user)
        form = StaffProfileForm(instance=user_1)
        context = {
            'user_1': user_1,
            'form': form,
        }

        if request.method == 'POST':

            form = StaffProfileForm(request.POST, instance=user_1)

            if form.is_valid():
                form.save()
                # messages.success(request, 'Updated successfully!')
                return redirect('home')

    else:
        user_1 = DBerDetail.objects.get(user_detail=request.user)
        form = DBerProfileForm(instance=user_1)
        context = {
            'user_1': user_1,
            'form': form,
        }

        if request.method == 'POST':

            form = DBerProfileForm(request.POST, instance=user_1)

            if form.is_valid():
                form.save()
                # messages.success(request, 'Updated successfully!')
                return redirect('home')

    return render(request, 'profile.html', context)
# Create your views here.
