from time import time

from django.db import models

# Create your models here.
from django.utils import timezone
from django.utils.formats import time_format


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=20)

    class Meta:
        db_table = "city"


class Area(models.Model):
    area_id = models.AutoField(primary_key=True)
    area_name = models.CharField(max_length=40)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)

    class Meta:
        db_table = "area"


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    contact_no = models.CharField(max_length=11)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=250)
    is_admin = models.IntegerField()
    otp = models.CharField(max_length=100)
    otp_used = models.IntegerField()

    class Meta:
        db_table = "patient"


class Specialization(models.Model):
    specialization_id = models.AutoField(primary_key=True)
    specialization_name = models.CharField(max_length=30)
    specialization_description = models.CharField(max_length=100)

    class Meta:
        db_table = "specialization"


class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    doctor_name = models.CharField(max_length=30)
    profile_photo = models.CharField(max_length=30)
    contact_no = models.CharField(max_length=11)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=250)
    otp = models.CharField(max_length=100)
    otp_used = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)
    licence_image = models.CharField(max_length=30)
    specialization_id = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    year_of_experience = models.IntegerField()
    clinic_hospital_name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    is_active = models.IntegerField()
    visiting_charges = models.CharField(max_length=10)

    class Meta:
        db_table = "doctor"


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    appointment_date = models.DateField()
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_time = models.TimeField()
    status = models.IntegerField()
    a_description = models.CharField(max_length=50)
    payment_date = models.DateField()
    amount = models.CharField(max_length=10)
    payment_status = models.IntegerField()

    class Meta:
        db_table = "appointment"


class Available_time(models.Model):
    aid = models.AutoField(primary_key=True)
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    class Meta:
        db_table = "available_time"


class Gallery(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_path = models.CharField(max_length=50)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    class Meta:
        db_table = "gallery"


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    feedback_date = models.DateField()
    description = models.CharField(max_length=100)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    is_approve = models.IntegerField()

    class Meta:
        db_table = "feedback"


class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    prescription_description = models.CharField(max_length=20)
    uploaded_date = models.DateField()
    appointment_id = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    class Meta:
        db_table = "prescription"


class Contact_us(models.Model):
    co_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField()
    contact_no = models.CharField(max_length=11)
    message = models.CharField(max_length=200)
    up_date = models.DateField()
    # up_time = models.TimeField(default=timezone.now)

    class Meta:
        db_table = "contact_us"


class Medical_report(models.Model):
    medical_report_id = models.AutoField(primary_key=True)
    up_date = models.DateField()
    appointment_id = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    document = models.CharField(max_length=30)

    class Meta:
        db_table = "medical_report"


