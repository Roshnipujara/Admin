"""Admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
# noinspection PyProtectedMember
from django.urls import path
from DT import views
from django.urls import include

from DT.views import HomeView,DoctorChart

urlpatterns = [
    # path('charthome/',HomeView.as_view(), name="home"),
    # path(r'^api/chart/data/$', DoctorChart.as_view(),name='api-data' ),
    # CLIENT SIDE
    path('patient/', include('patient.urls')),
    path('doctor/', include('doctor.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),

    path('patient_render/pdf/', views.patient_Pdf.as_view()),
    path('doctor_render/pdf/', views.doctor_Pdf.as_view()),
    path('appointment_render/pdf/', views.appointment_Pdf.as_view()),

    path('otp/', views.sendemail),
    path('forgot_password/', views.forgot_password),
    path('set_password/', views.set_password),

    path('admin/', admin.site.urls),
    path('home/', views.home),
    path('login/', views.login),
    path('logout/', views.logout),
    path('header/', views.login),
    path('patient/', views.patient),
    path('AllPatient/', views.showPatient),

    path('admin_edit/', views.admin_edit),
    path('admin_update/', views.admin_update),

    path('city/', views.city),
    path('area/', views.area),
    path('doctor/', views.doctor),
    path('available_time/', views.available_time),
    path('appointment/', views.appointment),
    path('specialization/', views.specialization),
    path('gallery/', views.gallery),
    path('feedback/', views.feedback),
    path('prescription/', views.prescription),
    path('contact_us/', views.contact_us),
    path('medical_report/', views.medical_report),

    path('city_insert/', views.city_insert),
    path('area_insert/', views.area_insert),
    path('gallery_insert/', views.gallery_insert),
    path('specialization_insert/', views.specialization_insert),
    path('available_time_insert/', views.available_time_insert),

    path('city_edit/<int:city_id>', views.city_edit),
    path('city_update/<int:city_id>', views.city_update),
    path('area_edit/<int:area_id>', views.area_edit),
    path('area_update/<int:area_id>', views.area_update),
    path('patient_edit/<int:patient_id>', views.patient_edit),
    path('patient_update/<int:patient_id>', views.patient_update),
    path('available_time_edit/<int:aid>', views.available_time_edit),
    path('available_time_update/<int:aid>', views.available_time_update),
    path('specialization_edit/<int:specialization_id>', views.specialization_edit),
    path('specialization_update/<int:specialization_id>', views.specialization_update),

    path('city_del/<int:city_id>', views.city_del),
    path('area_del/<int:area_id>', views.area_del),
    path('available_time_del/<int:aid>', views.available_time_del),
    path('specialization_del/<int:specialization_id>', views.specialization_del),
    path('feedback_del/<int:feedback_id>', views.feedback_del),
    path('prescription_del/<int:prescription_id>', views.prescription_del),
    path('contact_us_del/<int:co_id>', views.contact_us_del),
    path('medical_report_del/<int:medical_report_id>', views.medical_report_del),
    path('gallery_del/<int:image_id>', views.gallery_del),
    # path('patient_del/<int:patient_id>', views.patient_del),

    # path('patient/', include('patient.urls')),
    url(r'doctorhome', HomeView.as_view(), name='home'),
    url(r'^api/chart/data/$', DoctorChart.as_view(),name="api-data"),

]
