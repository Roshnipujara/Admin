from django import forms
from DT.models import City
from DT.models import Area
from DT.models import Available_time
from DT.models import Specialization
from DT.models import Gallery
from DT.models import Patient
from DT.models import Appointment
from DT.models import Contact_us
from DT.models import Prescription
from DT.models import Doctor
from DT.models import Feedback
from DT.models import Medical_report


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['city_name']


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['area_name', 'city_id']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['patient_name', 'address', 'gender', 'contact_no', 'email', 'password', 'area_id','is_admin']


class GalleryForm(forms.ModelForm):
    image_path = forms.FileField()
    class Meta:
        model = Gallery
        fields = ['image_path','doctor_id']


class Available_timeForm(forms.ModelForm):
    class Meta:
        model = Available_time
        fields = ['day','start_time','end_time','doctor_id']


class SpecializationForm(forms.ModelForm):
    class Meta:
        model = Specialization
        fields = ['specialization_name', 'specialization_description']


class Contact_usForm(forms.ModelForm):
    class Meta:
        model = Contact_us
        fields = ['fname', 'lname', 'email', 'contact_no', 'message', 'up_date']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time', 'a_description', 'doctor_id', 'patient_id','status']


class PrescriptionForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = ['prescription_description', 'uploaded_date', 'appointment_id']


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ['feedback_date', 'description', 'doctor_id','patient_id','is_approve']


class DoctorForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = ['doctor_name', 'contact_no', 'email','password','address','year_of_experience','clinic_hospital_name','description'
                  ,'is_active','visiting_charges','city_id','specialization_id']


class DoctorAllForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = ['doctor_name','profile_photo', 'contact_no', 'email','password','address','licence_image','year_of_experience',
                  'clinic_hospital_name','description','is_active','visiting_charges','city_id','specialization_id']


class MedicalReportForm(forms.ModelForm):
    document = forms.FileField()
    class Meta:
        model = Medical_report
        fields = ['up_date', 'document', 'appointment_id']
