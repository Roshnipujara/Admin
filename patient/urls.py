# path('home',patient_views.home)
from django.urls import path
from patient import patient_views

urlpatterns = [

    path('index', patient_views.index),
    # path('admin/', admin.site.urls),
    path('patient_logout/', patient_views.patient_logout),
    path('home/', patient_views.homepage),

    path('patient_edit/<int:patient_id>', patient_views.patient_edit),
    path('patient_update/<int:patient_id>', patient_views.patient_update),

    path('patient_otp/', patient_views.patient_sendemail),
    path('patient_forgot_password/', patient_views.patient_forgot_password),
    path('patient_set_password/', patient_views.patient_set_password),

    path('ajax/load-cities/', patient_views.load_doctors, name='ajax_load_doctors'),
    path('patient_login/', patient_views.patient_login),
    path('doctor_registration/', patient_views.doctor_registration),
    path('patient_feedback/', patient_views.patient_feedback),
    path('patient_registration/', patient_views.patient_registration),

    path('patient_medical_report/<int:appointment_id>', patient_views.patient_medical_report),

    path('patient_appointment/', patient_views.patient_appointment),
    path('patient_homeappointment/', patient_views.patient_homeappointment),
    path('patient_appointment_page/', patient_views.patient_appointment_page),

    path('patient_about_us/', patient_views.patient_about_us),
    path('patient_prescription/<int:appointment_id>', patient_views.patient_prescrition),
    path('patient_doctor/', patient_views.patient_doctor),
    path('patient_doctordetails/<int:doctor_id>', patient_views.patient_doctordetails),
    path('patient_allappointment/', patient_views.patient_allappointment),
    path('patient_contact_us/', patient_views.patient_contact_us),
]