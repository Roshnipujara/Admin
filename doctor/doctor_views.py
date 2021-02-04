from django.contrib import messages

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone
from django.views.generic.base import View

from DT.functions import handle_uploaded_file
from DT.models import City, Patient, Area, Doctor, Available_time, Appointment, Specialization, Gallery, Feedback, \
    Prescription, Contact_us, Medical_report
from DT.form import CityForm, AreaForm, Available_timeForm, SpecializationForm, GalleryForm, PatientForm, \
    AppointmentForm, PrescriptionForm, DoctorForm
import hashlib
from django.db.models import Count
from DT.render import Render
from DT.views import appointment


def index(request):
    return render(request, "index.html")

import random
def doctor_sendemail(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST['email']
    request.session['temail']=e
    obj = Doctor.objects.filter(email=e).count()

    if obj == 1:
        val = Doctor.objects.filter(email=e).update(otp=otp1 , otp_used=0)
        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
        return render(request, 'doctor_set_password.html')


def doctor_set_password(request):

    if request.method == "POST":
        totp = request.POST['otp']
        tpassword = request.POST['password']
        cpassword = request.POST['cpassword']

        if tpassword == cpassword :
            e = request.session['temail']
            val = Doctor.objects.filter(email=e, otp=totp).count()

            if val == 1:
                tpassword = hashlib.md5(tpassword.encode('utf')).hexdigest()
                val = Doctor.objects.filter(email=e).update(otp_used=1,password=tpassword)
                return render(request, "doctor_login.html")
            else:
                messages.error(request, 'OTP does not match')
                return render(request, "doctor_set_password.html")
        else:
            messages.error(request, 'New Password & Confirm Password does not match')
            return render(request, "doctor_set_password.html")
    return render(request, "doctor_set_password.html")


def doctor_forgot_password(request):
    return render(request, "doctor_forgot_password.html")


class patient_Pdf(View):

    def get(Self, request):
        patient = Patient.objects.all().select_related("area_id").values('area_id','area_id__area_name').annotate(total=Count('area_id'))
        patients = Patient.objects.all().select_related("area_id")
        for p in patient:
            # print (p)
            today = timezone.now()
        params = {
            'today': today,
            'patient': patient,
            'patients' : patients,
            'request': request
        }
        return Render.render('report_patient_doctor.html', params)


class appointment_Pdf(View):

    def get(Self, request):
        val = request.session['username']
        d = Doctor.objects.filter(email=val)
        for doc in d:
            did = doc.doctor_id
        doctor = Doctor.objects.filter(doctor_id=did)
        appointment = Appointment.objects.all().select_related("doctor_id").select_related("patient_id")
        today = timezone.now()
        params = {
            'today': today,
            'appointment': appointment,
            'request': request
        }
        return Render.render('report_appointment_doctor.html', params)


def doctor_edit(request,doctor_id):
    doctor = Doctor.objects.filter(doctor_id=doctor_id , is_active=1)
    print(Doctor.objects.filter(doctor_id=doctor_id , is_active=1).count())
    city = City.objects.all()
    specialization = Specialization.objects.all()
    if request.session.has_key('username'):
        return render(request, "doctor_update.html", {'doctor': doctor,'city':city,'specialization':specialization})
    else:
        return render(request, "doctor_home.html")


def doctor_update(request, doctor_id):
    doctor = Doctor.objects.get(doctor_id=doctor_id)
    form = DoctorForm(request.POST, instance=doctor)
    if form.is_valid():
        form.save()
        return redirect("/doctor/doctor_home/")
    return render(request, 'doctor_edit.html', {'doctor': doctor})


def doctor_photo(request):
    val = request.session['username']
    d = Doctor.objects.filter(email=val)
    # print("count =     ===============",d.count())
    did=0
    for doc in d:
        did = doc.doctor_id
        # print("*************",did)
    doctor = Doctor.objects.filter(doctor_id=did)
    return doctor


def doctor_home(request):
    doctor = doctor_photo(request)
    return render(request, "doctor_home.html", {'doctor': doctor})


def doctor_logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, "doctor_login.html")


def doctor_login(request):
    appointment = Appointment.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        pwd = request.POST['pwd']
        newpassword = hashlib.md5(pwd.encode('utf')).hexdigest()
        val = Doctor.objects.filter(email=username, password=newpassword, is_active=1).count()
        if val == 1:
            val1 = Doctor.objects.filter(email=username, password=newpassword, is_active=1)
            for item in val1:
                n = item.doctor_id
            request.session['username'] = username
            request.session['id'] = n
            # return render(request, "all_doctor_appointment.html", {'appointment': appointment})
            return HttpResponseRedirect('/doctor/doctor_home/')
        else:
            messages.error(request, 'username or password not correct')
            return render(request, "doctor_login.html")
    else:
        return render(request, "doctor_login.html")


def all_doctor_city(request):
    doctor = doctor_photo(request)
    city = City.objects.all()
    print("------------dOCTOR VIEW CALL ------------")
    # print("***********" , request.session.has_key('username'))
    if request.session.has_key('username'):
        return render(request, "all_doctor_city.html", {'city': city,'doctor':doctor})
    else:
        return render(request, "login.html")


def all_doctor_area(request):
    doctor = doctor_photo(request)
    area = Area.objects.all()
    if request.session.has_key('username'):
        return render(request, "all_doctor_area.html", {'area': area,'doctor':doctor})
    else:
        return render(request, "login.html")


def all_doctor_patient(request):
    doctor = doctor_photo(request)
    patient = Patient.objects.all()
    if request.session.has_key('username'):
        return render(request, "all_doctor_patients.html", {'patient': patient,'doctor':doctor})
    else:
        return render(request, "login.html")


def all_doctor(request):
    val = request.session['username']
    d = Doctor.objects.filter(email=val)
    for doc in d:
        did = doc.doctor_id
    doctor = Doctor.objects.filter(doctor_id=did)
    return render(request, 'all_doctor_doctor.html', {'doctor': doctor})


def all_doctor_available_time(request):
    doctor = doctor_photo(request)
    val = request.session['username']
    d = Doctor.objects.filter(email=val)
    for d in d:
        did = d.doctor_id
    available_time = Available_time.objects.filter(doctor_id=did)
    return render(request, 'all_doctor_available_time.html', {'available_time': available_time, 'doctor': doctor})


def doctor_available_time_insert(request):
    doctor = doctor_photo(request)
    d = Doctor.objects.all()
    if request.method == "POST":
        form = Available_timeForm(request.POST)
        # print("+++++++++++++++++++", form.errors)
        if form.is_valid():
            try:
                # print("------------- Before save data ------------")
                form.save()
                # print("++++++++++ save data +++++++++++")
                return redirect('/doctor/all_doctor_available_time')
            except:
                pass
    else:
        form = Available_timeForm()
    return render(request, 'doctor_available_time_insert.html', {'form': form, 'doctor' : doctor,'d':d})


def doctor_available_time_edit(request, aid):
    doctor = doctor_photo(request)
    availabletime = Available_time.objects.get(aid = aid)
    doc = Doctor.objects.all()
    d1 = availabletime.start_time
    nd = d1.strftime("%H:%M")
    d2 = availabletime.end_time
    nd1 = d2.strftime("%H:%M")
    return render(request, 'doctor_available_time_edit.html', {'availabletime': availabletime, 'doc': doc, 's': nd, 'e':nd1,'doctor':doctor})


def doctor_available_time_update(request, aid):
    doctor = doctor_photo(request)
    availabletime = Available_time.objects.get(aid = aid)
    form = Available_timeForm(request.POST, instance = availabletime)
    # print("+++++++++++++++++++", form.errors)
    if form.is_valid():
        # print("------------- Before save data ------------")
        form.save()
        # print("------------- After save data ------------")
        return redirect("/doctor/all_doctor_available_time")
    return render(request, 'doctor_available_time_edit.html', {'availabletime': availabletime,'doctor':doctor})


def doctor_available_time_del(request, aid):
    availabletime = Available_time.objects.get(aid=aid)
    availabletime.delete()
    return redirect("/doctor/all_doctor_available_time")


def all_doctor_specialization(request):
    specialization = Specialization.objects.all()
    if request.session.has_key('username'):
        return render(request, "all_doctor_specialization.html", {'specialization': specialization})
    else:
        return render(request, "login.html")


def all_doctor_gallery(request):
    doctor = doctor_photo(request)
    val = request.session['username']
    d = Doctor.objects.filter(email=val)
    for doc in d:
        did = doc.doctor_id
    gallery = Gallery.objects.filter(doctor_id=did)
    return render(request, 'all_doctor_gallery.html', {'gallery': gallery, 'doctor': doctor})


def doctor_gallery_insert(request):
    #doctor = doctor_photo(request)
    doc = Doctor.objects.all()

    if request.method == "POST":
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['image_path'])
            form.save()
            return redirect('/doctor/all_doctor_gallery')
    else:
        form = GalleryForm()
    return render(request, 'doctor_gallery_insert.html', {'form': form, 'doctor': doctor,'doc':doc})


def doctor_gallery_del(request, image_id):
    gallery = Gallery.objects.get(image_id=image_id)
    gallery.delete()
    return redirect("/doctor/all_doctor_gallery")


def all_doctor_feedback(request):
    doctor = doctor_photo(request)
    val = request.session['username']
    d = Doctor.objects.filter(email=val)
    for doc in d:
        did = doc.doctor_id
    feedback = Feedback.objects.filter(doctor_id=did)
    return render(request, 'all_doctor_feedback.html', {'feedback': feedback, 'doctor': doctor})


def feedback_accept(request,fid):
    feedback = Feedback.objects.get(feedback_id=fid)
    feedback.is_approve=1
    feedback.save()

    return HttpResponseRedirect("/doctor/all_doctor_feedback/")


def feedback_reject(request,fid):
    feedback = Feedback.objects.get(feedback_id=fid)
    feedback.is_approve = 2
    feedback.save()

    return HttpResponseRedirect("/doctor/all_doctor_feedback/")


def all_doctor_appointment(request):
    # appointment = Appointment.objects.all()
    doctor = doctor_photo(request)
    prescription = Prescription.objects.all()
    val = request.session['username']
    # print("From session ----------------------", val)
    doctor = Doctor.objects.filter(email=val)
    for d in doctor:
        did = d.doctor_id
    # print("patient data ****************", pid)
    appointment = Appointment.objects.filter(doctor_id=did)
    return render(request, 'all_doctor_appointment.html', {'appointment': appointment,'prescription':prescription,'doctor':doctor})


def accept(request,id):
    appointment = Appointment.objects.get(appointment_id=id)
    appointment.status=1
    appointment.save()

    return HttpResponseRedirect("/doctor/all_doctor_appointment/")


def reject(request,id):
    appointment = Appointment.objects.get(appointment_id=id)
    appointment.status = 2
    appointment.save()

    return HttpResponseRedirect("/doctor/all_doctor_appointment/")


def confirm(request,id):
    appointment = Appointment.objects.get(appointment_id=id)
    appointment.status = 3
    appointment.save()

    return HttpResponseRedirect("/doctor/all_doctor_appointment/")


def not_confirm(request,id):
    appointment = Appointment.objects.get(appointment_id=id)
    # print(+++++++++++,appointment)
    appointment.status = 4
    appointment.save()

    return HttpResponseRedirect("/doctor/all_doctor_appointment/")


def all_doctor_prescription(request):
    prescription = Prescription.objects.all()
    if request.session.has_key('username'):
        return render(request, "all_doctor_prescription.html", {'prescription': prescription})
    else:
        return render(request, "doctor_login.html")


def doctor_prescription(request,appointment_id):
    doctor = doctor_photo(request)
    prescription = Prescription.objects.filter(appointment_id=appointment_id)
    if request.session.has_key('username'):
        return render(request, "all_doctor_prescription.html", {'prescription': prescription, 'doctor':doctor})
    else:
        return render(request, "doctor_login.html")


def f_doctor_prescription(request,appointment_id):
    prescription = Prescription.objects.filter(appointment_id=appointment_id)
    return render(request, "f_doctor_prescription.html", {'prescription': prescription})


def doctor_prescription_insert(request,id):
    appointment = Appointment.objects.get(appointment_id=id)
    doctor = doctor_photo(request)
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        #form.instance.appointment_id = appointment.appointment_id
        print("****************" , form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect('/doctor/all_doctor_appointment/')
            except:
                pass
    else:
        form = PrescriptionForm()
    return render(request, 'doctor_prescription_insert.html', {'form': form,'appointment':appointment,'doctor':doctor})


def all_doctor_prescription_del(request, prescription_id):
    p = Prescription.objects.get(prescription_id=prescription_id)
    appointment_id = p.appointment_id_id

    p.delete()

    url="/doctor/doctor_prescription/" + str(appointment_id)

    return redirect(url)


# def all_doctor_medical_report(request,appointment_id=0):
#     doctor = doctor_photo(request)
#     medical_report = Medical_report.objects.all()
#     # appointment = Appointment.objects.all()
#     appointment = Appointment.objects.filter(appointment_id=appointment_id)
#     for a in appointment:
#         aid = a.appointment_id
#     m = Medical_report.objects.filter(appointment_id=aid)
#     if request.session.has_key('username'):
#         return render(request, "all_doctor_medical_report.html", {'medical_report': medical_report,'doctor':doctor,'report':m,'appointment':appointment})
#     else:
#         return render(request, "login.html")

def all_doctor_medical_report(request,appointment_id):
    medical_report = Medical_report.objects.filter(appointment_id=appointment_id)
    m = Medical_report.objects.filter(appointment_id=appointment_id)
    return render(request, "all_doctor_medical_report.html", {'medical_report': medical_report,'report':m})