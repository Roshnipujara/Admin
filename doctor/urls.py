from django.contrib import admin
from django.urls import path
from doctor import doctor_views

urlpatterns = [


    path('index/', doctor_views.index),
    # path('admin/', doctor_views.site.urls),
    # path('table/', doctor_views.viewtable),

    path('doctor_otp/', doctor_views.doctor_sendemail),
    path('doctor_forgot_password/', doctor_views.doctor_forgot_password),
    path('doctor_set_password/', doctor_views.doctor_set_password),

    path('patient_render/pdf/', doctor_views.patient_Pdf.as_view()),
    path('appointment_render/pdf/', doctor_views.appointment_Pdf.as_view()),

    path('doctor_login/', doctor_views.doctor_login),
    path('doctor_logout/', doctor_views.doctor_logout),

    path("doctor_home/", doctor_views.doctor_home),
    path('doctor_photo/', doctor_views.doctor_photo),
    # path('header/', doctor_views.login),
    # path('patient/', doctor_views.patient),
    path('all_doctor_patient/', doctor_views.all_doctor_patient),

    path('all_doctor_city/', doctor_views.all_doctor_city),
    path('all_doctor_area/', doctor_views.all_doctor_area),
    path('all_doctor/', doctor_views.all_doctor),

    path('doctor_edit/<int:doctor_id>', doctor_views.doctor_edit),
    path('doctor_update/<int:doctor_id>', doctor_views.doctor_update),


    path('all_doctor_available_time/', doctor_views.all_doctor_available_time),
    path('doctor_available_time_insert/', doctor_views.doctor_available_time_insert),
    path('doctor_available_time_del/<int:aid>', doctor_views.doctor_available_time_del),
    path('doctor_available_time_update/<int:aid>', doctor_views.doctor_available_time_update),
    path('doctor_available_time_edit/<int:aid>', doctor_views.doctor_available_time_edit),

    path('all_doctor_appointment/', doctor_views.all_doctor_appointment),
    path('accept/<int:id>', doctor_views.accept),
    path('reject/<int:id>', doctor_views.reject),
    path('confirm/<int:id>', doctor_views.confirm),
    path('not_confirm/<int:id>', doctor_views.not_confirm),


    path('all_doctor_specialization/', doctor_views.all_doctor_specialization),

    path('all_doctor_gallery/', doctor_views.all_doctor_gallery),
    path('doctor_gallery_insert/', doctor_views.doctor_gallery_insert),
    path('doctor_gallery_del/<int:image_id>', doctor_views.doctor_gallery_del),

    path('all_doctor_feedback/', doctor_views.all_doctor_feedback),
    path('feedback_accept/<int:fid>', doctor_views.feedback_accept),
    path('feedback_reject/<int:fid>', doctor_views.feedback_reject),

    path('all_doctor_prescription/', doctor_views.all_doctor_prescription),
    path('doctor_prescription/<int:appointment_id>', doctor_views.doctor_prescription),
    path('doctor_prescription_insert/<int:id>', doctor_views.doctor_prescription_insert),
    path('all_doctor_prescription_del/<int:prescription_id>', doctor_views.all_doctor_prescription_del),

    path('all_doctor_medical_report/<int:appointment_id>', doctor_views.all_doctor_medical_report),


]