
from django.contrib import messages

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control

from DT.form import PatientForm, AppointmentForm, SpecializationForm, Contact_usForm, PrescriptionForm, DoctorForm, \
    DoctorAllForm, FeedbackForm, MedicalReportForm
from DT.functions import handle_uploaded_file
from DT.models import Patient, Area, Doctor, Feedback, Specialization, Appointment, Contact_us, Prescription, \
    Prescription, City, Medical_report
import hashlib

# Create your views here.


def index(request):
    return render(request, "index.html")


import random
def patient_sendemail(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST['email']
    request.session['temail']=e
    obj = Patient.objects.filter(email=e , is_admin=0).count()

    if obj == 1:
        val = Patient.objects.filter(email=e, is_admin=0).update(otp=otp1 , otp_used=0)
        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
        return render(request, 'patient_set_password.html')


def patient_set_password(request):
    if request.method == "POST":
        totp = request.POST['otp']
        tpassword = request.POST['password']
        cpassword = request.POST['cpassword']

        if tpassword == cpassword:
            e = request.session['temail']
            val = Patient.objects.filter(email=e, is_admin=0,otp=totp).count()

            if val == 1:
                tpassword = hashlib.md5(tpassword.encode('utf')).hexdigest()
                val = Patient.objects.filter(email=e, is_admin=0).update(otp_used=1,password=tpassword)
                return render(request, "patient_login.html")
            else:
                messages.error(request, 'OTP does not match')
                return render(request, "patient_set_password.html")
        else:
            messages.error(request, 'New Password & Confirm Password does not match')
            return render(request, "patient_set_password.html")

    return render(request, "patient_set_password.html")


def patient_forgot_password(request):
    return render(request,"patient_forgot_password.html")


def patient_edit(request,patient_id):
    patient = Patient.objects.all().get(patient_id=patient_id , is_admin=0)
    area = Area.objects.all()
    if request.session.has_key('username'):
        return render(request, "patient_update.html", {'patient': patient,'area':area})
    else:
        return render(request, "home.html")


def patient_update(request, patient_id):
    patient = Patient.objects.get(patient_id=patient_id)
    form = PatientForm(request.POST, instance=patient)
    if form.is_valid():
        form.save()
        return redirect("/patient/home")
    return render(request, 'patient_edit.html', {'patient': patient})


def doctor_registration(request):
    city = City.objects.all()
    specialization = Specialization.objects.all()
    if request.method == "POST":
        form = DoctorAllForm(request.POST, request.FILES)
        # print("**********", form.errors)
        if form.is_valid():
            # handle_uploaded_file(request.FILES['image_path'])
            try:
                print("------------- Before save data ------------")
                newform = form.save(commit=False)
                newform.password = hashlib.md5(newform.password.encode('utf')).hexdigest()
                # print("@@@@@@",newform.password)
                newform.save()
                print("++++++save data +++++++++++")
                return redirect('/doctor/doctor_login/')
            except:
                pass
    else:
        form = DoctorForm()
        form.fields['is_active'].initial=1
    return render(request, 'doctor_registration.html', {'form':form, 'city':city,'specialization':specialization})


def patient_registration(request):
    area = Area.objects.all()
    if request.method == "POST":
        form = PatientForm(request.POST)
        print("**********", form.errors)
        if form.is_valid():
            try:
                print("------------- Before save data ------------")
                newform = form.save(commit=False)
                #newform.password = hashlib.md5(newform.password.encode('utf')).hexdigest()
                # print("@@@@@@",newform.password)
                newform.save()
                print("++++++save data +++++++++++")
                return redirect('/patient/patient_login/')
            except:
                pass
    else:
        form = PatientForm()
        form.fields['is_admin'].initial=1
    return render(request, 'patient_registration.html', {'form':form, 'area':area})


def patient_login(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pwd']
        newpassword = hashlib.md5(password.encode('utf')).hexdigest()
        print(newpassword)
        val = Patient.objects.filter(email=username, password=newpassword, is_admin=0).count()
        # cities = City.objects.all()
        print("+++++++++++++++++" , val)
        if val == 1:
            val1 = Patient.objects.filter(email=username, password=newpassword, is_admin=0)
            for item in val1:
                n = item.patient_name
                i = item.patient_id
                # print("++++++",n)
            request.session['username'] = username
            request.session['name'] = n
            request.session['pid'] = i
            return HttpResponseRedirect('/patient/home')
        else:
            messages.error(request, 'username or password not correct')
            return render(request, "patient_login.html")
    else:
        return render(request, "patient_login.html")


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def patient_logout(request):
    try:
        del request.session['username']
        del request.session['name']
        del request.session['pid']
    except:
        pass
    return render(request, "patient_login.html")


def homepage(request):
    pid=0
    val=""
    specialization = Specialization.objects.all()
    doctor = Doctor.objects.all()
    cd = Doctor.objects.all().count()
    cp = Patient.objects.all().count()
    feedback = Feedback.objects.all()
    if 'username' in request.session:
        val = request.session['username']
        # print("From session ----------------------", val)
    p = Patient.objects.filter(email=val)
    for d in p:
        pid = d.patient_id
        # print("patient data ****************", pid)
    patient = Patient.objects.filter(patient_id=pid)
    return render(request, "homepage.html",{'doctor':doctor,'cd':cd, 'feedback': feedback, 'specialization': specialization, 'patient': patient,'cp':cp})


def load_doctors(request):
    sid = request.GET.get('special')
    print("--------++++++++++++-----------",sid)
    doctors = Doctor.objects.filter(specialization_id=sid)
    return render(request, 'doctors_dropdown.html', {'doctors': doctors})


def patient_about_us(request):
    return render(request, "patient_about_us.html")


def patient_contact_us(request):
    # contact_us = Contact_us.objects.all()
    if request.method == "POST":
        form = Contact_usForm(request.POST)
        # print("**********", form.errors)
        if form.is_valid():
            try:
                # print("------------- Before save data ------------")
                form.save()

                # print("++++++save data +++++++++++")
                return redirect('/patient/home')

            except:
                pass
    else:
        form = Contact_usForm()
    return render(request, 'patient_contact_us.html', {'form': form})


def patient_doctor(request):
    doctor = Doctor.objects.all()
    return render(request, "patient_doctor.html",{'doctor':doctor})


def patient_doctordetails(request, doctor_id):
        pid=0
        if 'username' in request.session:
            val = request.session['username']
            p = Patient.objects.filter(email=val)
            for d in p:
                pid = d.patient_id
            patient = Patient.objects.filter(patient_id=pid)
        doctor = Doctor.objects.filter(doctor_id=doctor_id)
        if request.method == "POST":
            form1 = AppointmentForm(request.POST)
            print("**********", form1.errors)
            if form1.is_valid():
                try:
                    print("test test test Before save data ------------")
                    form1.save()
                    print("++++++save data +++++++++++")
                    return redirect('/patient/home')
                except:
                    pass
        else:
            form = AppointmentForm()

        if 'username' in request.session:
            return render(request, 'patient_doctordetails.html', {'form': form, 'doctor': doctor, 'patient': patient})
        else:
            return render(request, 'patient_doctordetails.html', {'form': form, 'doctor': doctor})


def patient_allappointment(request):
    aid=0
    # appointment = Appointment.objects.filter(appointment=appointment_id)
    val = request.session['username']
    print("From session ----------------------" , val)
    p = Patient.objects.filter(email=val)
    for d in p:
        pid = d.patient_id
    print("patient data ****************" , pid)
    appointment = Appointment.objects.filter(patient_id=pid)

    for a in appointment:
        aid = a.appointment_id
    m = Medical_report.objects.filter(appointment_id=aid)
    return render(request, "patient_appointment.html", {'appointment':appointment,'report':m})


def patient_feedback(request):
    if 'username' in request.session:
        val = request.session['username']
        patient = Patient.objects.filter(email=val)
        feedback = Feedback.objects.all()
        # patient = Patient.objects.all()
        if request.method == "POST":
            form = FeedbackForm(request.POST)
            print("****", form.errors)
            if form.is_valid():
                try:
                    print("------------- Before save data ------------")
                    form.save()
                    print("++++++save data +++++++++++")
                    return redirect('/patient/home')
                except:
                    pass
            else:
                form = FeedbackForm()
        return render(request, 'patient_doctordetails.html', {'form': form, 'feedback': feedback, 'patient': patient})
    else:
        return render(request, 'patient_login.html')


def patient_prescrition(request, appointment_id):
    prescription = Prescription.objects.filter(appointment_id=appointment_id)
    return render(request, 'patient_prescription.html', {'prescription':prescription})


def patient_homeappointment(request):
    # print("))))))))))))))))  " , request.session['username'])
    if 'username' in request.session:
        # print("inside session method")
        val = request.session['username']
        patient = Patient.objects.filter(email=val)
        doctor = Doctor.objects.all()

        if request.method == "POST":
            form = AppointmentForm(request.POST)
            print("**********", form.errors)
            if form.is_valid():
                try:
                    # print("------------- Before save data ------------")
                    form.save()
                    # print("++++++save data +++++++++++")
                    return redirect('/patient/home')
                except:
                    pass
        else:
            form = AppointmentForm()
            form.fields['status'].initial = 0
        return render(request, 'patient_login.html', {'form': form,'doctor':doctor , 'patient':patient})
    else:
        return render(request, 'patient_login.html')


def patient_appointment(request):
    patient = Patient.objects.all()
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        # print("**********", form.errors)
        if form.is_valid():
            try:
                # print("---- test --------- Before save data ------------")
                form.save()
                # print("++++++save data +++++++++++")
                return redirect('/patient/home')
            except:
                pass
    else:
        form = AppointmentForm()
        # form.fields['status'].initial = 0
    return render(request, 'patient_login.html', {'form': form, 'patient': patient})


def patient_appointment_page(request):

        val = request.session['username']
        specialization = Specialization.objects.all()
        patient = Patient.objects.filter(email=val)
        doctor = Doctor.objects.all()
        if request.method == "POST":
            form = AppointmentForm(request.POST)
            # print("**********", form.errors)
            if form.is_valid():
                try:
                    # print("test test test Before save data ------------")
                    form.save()
                    # print("++++++save data +++++++++++")
                    return redirect('/patient/home')
                except:
                    pass
        else:
            form = AppointmentForm()
            form.fields['status'].initial=0
        return render(request, 'patient_appointment_page.html', {'form': form,'doctor':doctor , 'patient':patient,'specialization':specialization})


def patient_medical_report(request, appointment_id):
    # print("--------- Function Call -----------------")
    appointment = Appointment.objects.filter(appointment_id=appointment_id)
    if request.method == "POST":
        form = MedicalReportForm(request.POST, request.FILES)
        print("+++++++++++++++", form.errors)
        if form.is_valid():
                print("------------- Before save data ------------")
                handle_uploaded_file(request.FILES['document'])
                form.save()
                print("++++++save data +++++++++++")
                return redirect('/patient/home')
    else:
        form = MedicalReportForm()
    return render(request, "patient_medical_report.html", {'form': form, 'appointment': appointment})