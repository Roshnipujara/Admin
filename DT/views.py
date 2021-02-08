import hashlib
import sys

from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from DT.functions import handle_uploaded_file
from DT.models import Patient, City, Area, Doctor, Available_time, Appointment, Specialization, Gallery, Feedback, \
    Prescription, Contact_us, Medical_report
from DT.form import CityForm, AreaForm, Available_timeForm, SpecializationForm, GalleryForm, PatientForm
from datetime import datetime
from django.http import HttpResponse
from django.utils import timezone
from .render import Render
from django.views.generic import View


import random

def sendemail(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST['email']
    request.session['temail']=e
    obj = Patient.objects.filter(email=e , is_admin=1).count()

    if obj == 1:
        val = Patient.objects.filter(email=e, is_admin=1).update(otp=otp1 , otp_used=0)
        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
        return render(request, 'set_password.html')
    else:
        return render(request,"forgot_password.html")


def set_password(request):
    totp = request.POST['otp']
    tpassword = request.POST['password']
    cpassword = request.POST['cpassword']

    if tpassword == cpassword :
        e = request.session['temail']
        val = Patient.objects.filter(email=e, is_admin=1,otp=totp).count()

        if val == 1:
            #tpassword = hashlib.md5(tpassword.encode('utf')).hexdigest()
            val = Patient.objects.filter(email=e, is_admin=1).update(otp_used=1,password=tpassword)
            return render(request, "login.html")
        else:
            messages.error(request, 'OTP does not match')
            return render(request, "set_password.html")
    else:
        messages.error(request, 'New Password & Confirm Password does not match')
        return render(request, "set_password.html")
    return render(request, "set_password.html")


def forgot_password(request):
    return render(request,"forgot_password.html")


class patient_Pdf(View):
    def get(Self, request):
        patient = Patient.objects.all().select_related("area_id").values('area_id', 'area_id__area_name').annotate(total=Count('area_id'))
        patients = Patient.objects.all().select_related("area_id")
        for p in patient:
            # print (p)
            today = timezone.now()
        params = {
            'today': today,
            'patient': patient,
            'patients': patients,
            'request': request
        }
        return Render.render('report_patient.html', params)


class doctor_Pdf(View):
    def get(Self, request):
        doctor = Doctor.objects.all().select_related("specialization_id")
        today = timezone.now()
        params = {
            'today': today,
            'doctor': doctor,
            'request': request
        }
        return Render.render('report_doctor.html', params)


class appointment_Pdf(View):
    def get(Self, request):
        appointment = Appointment.objects.all().select_related("doctor_id").select_related("patient_id")
        today = timezone.now()
        params = {
            'today': today,
            'appointment': appointment,
            'request': request
        }
        return Render.render('report_appointment.html', params)


# Create your views here.

#ADMIN SIDE


def home(request):
    return render(request, "home.html")


def city(request):
    return render(request, "showCity.html")


def showPatient(request):
    return render(request, "showPatient.html")


def admin_edit(request,patient_id):
    patient = Patient.objects.all().get(patient_id=patient_id , is_admin=1)
    area = Area.objects.all()
    if request.session.has_key('username'):
        return render(request, "admin_update.html", {'patient': patient,'area':area})
    else:
        return render(request, "home.html")


def admin_update(request, patient_id):
    patient = Patient.objects.get(patient_id=patient_id)
    form = PatientForm(request.POST, instance=patient)
    if form.is_valid():
        form.save()
        return redirect("/patient")
    return render(request, 'admin_update.html', {'patient': patient})


def logout(request):
    try:
        del request.session['username']
    except:
        pass
    #if request.POST.get("remember"):
    if request.COOKIES.get("cemail"):
        print("---------------", request.COOKIES.get('cemail'))
        return render(request, "login.html",
                       {'cookie1': request.COOKIES['cemail'], 'cookie2': request.COOKIES['cpass']})
    return redirect("/login/")


def login(request):


    if request.method == "POST":
        name = request.POST['uname']
        newpassword = request.POST['pwd']
        #newpassword = hashlib.md5(pwd.encode('utf')).hexdigest()
        val = Patient.objects.filter(email=name, password=newpassword, is_admin=1).count()
        if val == 1:
            val1 = Patient.objects.filter(email=name, password=newpassword, is_admin=1)
            for item in val1:
                n = item.patient_id
            request.session['username'] = name
            request.session['id'] = n

            if request.POST.get("remember"):
                response =redirect('/home/')
                #cookie_max_age = settings.TWO_FACTOR_REMEMBER_USER_SECONDS
                response.set_cookie('cemail', request.POST["uname"],3600 * 24 * 365 * 2)
                response.set_cookie('cpass', request.POST["pwd"],3600 * 24 * 365 * 2)
                return response
            return redirect("/home/")

        else:
            messages.error(request, 'Username or Password are invalid')
            return render(request, "login.html")
    else:
        if request.COOKIES.get("cemail"):
            print("---------------", request.COOKIES.get('cemail'))
            return render(request, "login.html",
                          {'cookie1': request.COOKIES['cemail'], 'cookie2': request.COOKIES['cpass']})
        else:
            return render(request,"login.html")

def city(request):
    city = City.objects.all()
    # print("***********" , request.session.has_key('username'))
    if request.session.has_key('username'):
        return render(request, "all_city.html", {'city': city})
    else:
        return render(request, "login.html")


def area(request):
    area = Area.objects.all()
    if request.session.has_key('username'):
        return render(request, "all_area.html", {'area': area})
    else:
        return render(request, "login.html")


def patient(request):
    patient = Patient.objects.all()
    if request.session.has_key('username'):
        return render(request, "all_patients.html", {'patient': patient})
    else:
        return render(request, "login.html")


def doctor(request):
    doctor = Doctor.objects.all()
    if request.session.has_key('username'):
        return render(request, "all_doctor.html", {'doctor': doctor})
    else:
        return render(request, "login.html")


def available_time(request):
    available_time = Available_time.objects.all()
    if request.session.has_key('username'):
        return render(request, "all_available_time.html", {'available_time': available_time})
    else:
        return render(request, "login.html")


def appointment(request):
    appointment = Appointment.objects.all()
    if request.session.has_key('username'):
        return render(request, "all_appointment.html", {'appointment': appointment})
    else:
        return render(request, "login.html")



def specialization(request):
    specialization = Specialization.objects.all()
    if request.session.has_key('username'):
        return render(request, "all_specialization.html", {'specialization': specialization})
    else:
        return render(request, "login.html")


def gallery(request):
    gallery = Gallery.objects.all()
    if request.session.has_key('username'):
        return render(request, "all_gallery.html", {'gallery': gallery})
    else:
        return render(request, "login.html")


def feedback(request):
    feedback = Feedback.objects.all()
    if request.session.has_key('username'):
        return render(request, "all_feedback.html", {'feedback': feedback})
    else:
        return render(request, "login.html")


def prescription(request):
    prescription = Prescription.objects.all()
    if request.session.has_key('username'):
        return render(request, "all_prescription.html", {'prescription': prescription})
    else:
        return render(request, "login.html")


def contact_us(request):
    contact_us = Contact_us.objects.all()
    if request.session.has_key('username'):
        return render(request, "all_contact_us.html", {'contact_us': contact_us})
    else:
        return render(request, "login.html")


def medical_report(request):
    medical_report = Medical_report.objects.all()
    if request.session.has_key('username'):
        return render(request, "all_medical_report.html", {'medical_report': medical_report})
    else:
        return render(request, "login.html")


def city_insert(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/city')
            except:
                print("---",sys.exc_info())
        else:
            pass
    else:
        form = CityForm()
    return render(request, "city_insert.html", {'form': form})


def area_insert(request):
    city = City.objects.all();
    if request.method == "POST":
        form = AreaForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                return redirect('/area')
            except:
                pass
    else:
        form = AreaForm()

    return render(request, 'area_insert.html', {'form': form, 'city': city})


def gallery_insert(request):
    doctor = Doctor.objects.all()
    if request.method == "POST":
        form = GalleryForm(request.POST, request.FILES)
        # print("++++++++++", form.errors)
        if form.is_valid():
            handle_uploaded_file(request.FILES['image_path'])
            form.save()
            return redirect('/gallery')
    else:
        form = GalleryForm()
        return render(request, 'gallery_insert.html', {'form': form, 'doctor': doctor})


def specialization_insert(request):
    if request.method == "POST":
        form = SpecializationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/specialization')

            except:
                pass
    else:
        form = SpecializationForm()
    return render(request, 'specialization_insert.html', {'form': form})


def available_time_insert(request):
    doctor = Doctor.objects.all()
    if request.method == "POST":
        form = Available_timeForm(request.POST)
        # print("+++++++++++++++" , form.errors)
        if form.is_valid():

            try:

                form.save()
                return redirect('/available_time')

            except:
                pass
    else:
        form = Available_timeForm()
    return render(request, 'available_time_insert.html', {'form': form, 'doctor' : doctor})


def city_edit(request, city_id):
    city = City.objects.get(city_id=city_id)
    return render(request, 'city_edit.html', {'city': city})


def city_update(request, city_id):
    city = City.objects.get(city_id=city_id)
    form = CityForm(request.POST, instance=city)
    if form.is_valid():
        form.save()
        return redirect("/city")
    return render(request, 'city_edit.html', {'city': city})


def area_edit(request, area_id):
    area = Area.objects.get(area_id=area_id)
    c = City.objects.all()
    return render(request, 'area_edit.html', {'area': area, 'c': c})


def area_update(request, area_id):
    area = Area.objects.get(area_id=area_id)
    form = AreaForm(request.POST, instance=area)
    if form.is_valid():
        form.save()
        return redirect("/area")
    return render(request, 'area_edit.html', {'area': area})


def patient_edit(request, patient_id):
    patient = Patient.objects.get(patient_id=patient_id, is_admin=1)
    area = Area.objects.all()
    return render(request, 'patient_edit.html', {'patient': patient, 'area': area})


def patient_update(request, patient_id):
    patient = Patient.objects.get(patient_id=patient_id)
    form = PatientForm(request.POST, instance=patient)
    if form.is_valid():
        form.save()
        return redirect("/patient")
    return render(request, 'patient_edit.html', {'patient': patient})


def available_time_edit(request, aid):
    available_time = Available_time.objects.get(aid=aid)
    doctor = Doctor.objects.all()

    d = available_time.start_time
    nd = d.strftime("%H:%M")

    d1 = available_time.end_time
    nd1 = d1.strftime("%H:%M")

    return render(request, 'available_time_edit.html', {'available_time': available_time, 'doctor': doctor, 's': nd, 'e': nd1})


def available_time_update(request, aid):
    available_time = Available_time.objects.get(aid=aid)
    form = Available_timeForm(request.POST, instance=available_time)
    # print("++++++++++++++++++++++++" , form.errors)
    if form.is_valid():
        form.save()
        return redirect("/available_time")
    return render(request, 'available_time_edit.html', {'available_time': available_time})


def specialization_edit(request, specialization_id):
    specialization = Specialization.objects.get(specialization_id=specialization_id)
    return render(request, 'specialization_edit.html', {'specialization': specialization})


def specialization_update(request, specialization_id):
    specialization = Specialization.objects.get(specialization_id=specialization_id)
    form = SpecializationForm(request.POST, instance=specialization)
    if form.is_valid():
        form.save()
        return redirect("/specialization")
    return render(request, 'specialization_edit.html', {'specialization': specialization})


def city_del(request, city_id):
    city = City.objects.get(city_id=city_id)
    city.delete()
    return redirect("/city")


def area_del(request, area_id):
    area = Area.objects.get(area_id=area_id)
    area.delete()
    return redirect("/area")


def patient_del(request, patient_id):
    patient = Patient.objects.get(patient_id=patient_id)
    patient.delete()
    return redirect("/patient")


def available_time_del(request, aid):
    available_time = Available_time.objects.get(aid=aid)
    available_time.delete()
    return redirect("/available_time")


def specialization_del(request, specialization_id):
    specialization = Specialization.objects.get(specialization_id=specialization_id)
    specialization.delete()
    return redirect("/specialization")


def feedback_del(request, feedback_id):
    feedback = Feedback.objects.get(feedback_id=feedback_id)
    feedback.delete()
    return redirect("/feedback")


def prescription_del(request, prescription_id):
    prescription = Prescription.objects.get(prescription_id=prescription_id)
    prescription.delete()
    return redirect("/prescription")


def contact_us_del(request, co_id):
    contact_us = Contact_us.objects.get(co_id=co_id)
    contact_us.delete()
    return redirect("/contact_us")


def medical_report_del(request, medical_report_id):
    medical_report = Medical_report.objects.get(medical_report_id=medical_report_id)
    medical_report.delete()
    return redirect("/medical_report")


def gallery_del(request, image_id):
    gallery = Gallery.objects.get(image_id=image_id)
    gallery.delete()
    return redirect("/gallery")






