# Generated by Django 3.1.5 on 2021-01-21 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('appointment_id', models.IntegerField(primary_key=True, serialize=False)),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.TimeField()),
                ('status', models.IntegerField()),
                ('a_description', models.CharField(max_length=50)),
                ('payment_date', models.DateField()),
                ('amount', models.CharField(max_length=10)),
                ('payment_status', models.IntegerField()),
            ],
            options={
                'db_table': 'appointment',
            },
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('area_id', models.IntegerField(primary_key=True, serialize=False)),
                ('area_name', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'area',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_id', models.IntegerField(primary_key=True, serialize=False)),
                ('city_name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='Contact_us',
            fields=[
                ('co_id', models.IntegerField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=30)),
                ('lname', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('contact_no', models.CharField(max_length=11)),
                ('message', models.CharField(max_length=200)),
                ('up_date', models.DateField()),
            ],
            options={
                'db_table': 'contact_us',
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('doctor_id', models.IntegerField(primary_key=True, serialize=False)),
                ('doctor_name', models.CharField(max_length=30)),
                ('profile_photo', models.CharField(max_length=30)),
                ('contact_no', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=250)),
                ('otp', models.CharField(max_length=100)),
                ('otp_used', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('licence_image', models.CharField(max_length=30)),
                ('year_of_experience', models.IntegerField()),
                ('clinic_hospital_name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=200)),
                ('is_active', models.IntegerField()),
                ('visiting_charges', models.CharField(max_length=10)),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DT.city')),
            ],
            options={
                'db_table': 'doctor',
            },
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('specialization_id', models.IntegerField(primary_key=True, serialize=False)),
                ('specialization_name', models.CharField(max_length=30)),
                ('specialization_description', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'specialization',
            },
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('prescription_id', models.IntegerField(primary_key=True, serialize=False)),
                ('prescription_description', models.CharField(max_length=20)),
                ('uploaded_date', models.DateField()),
                ('appointment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DT.appointment')),
            ],
            options={
                'db_table': 'prescription',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patient_id', models.IntegerField(primary_key=True, serialize=False)),
                ('patient_name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=10)),
                ('contact_no', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=250)),
                ('is_admin', models.IntegerField()),
                ('otp', models.CharField(max_length=100)),
                ('otp_used', models.IntegerField()),
                ('area_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DT.area')),
            ],
            options={
                'db_table': 'patient',
            },
        ),
        migrations.CreateModel(
            name='Medical_report',
            fields=[
                ('medical_report_id', models.IntegerField(primary_key=True, serialize=False)),
                ('up_date', models.DateField()),
                ('document', models.CharField(max_length=30)),
                ('appointment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DT.appointment')),
            ],
            options={
                'db_table': 'medical_report',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('image_id', models.IntegerField(primary_key=True, serialize=False)),
                ('image_path', models.CharField(max_length=50)),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DT.doctor')),
            ],
            options={
                'db_table': 'gallery',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('feedback_id', models.IntegerField(primary_key=True, serialize=False)),
                ('feedback_date', models.DateField()),
                ('description', models.CharField(max_length=100)),
                ('is_approve', models.IntegerField()),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DT.doctor')),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DT.patient')),
            ],
            options={
                'db_table': 'feedback',
            },
        ),
        migrations.AddField(
            model_name='doctor',
            name='specialization_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DT.specialization'),
        ),
        migrations.CreateModel(
            name='Available_time',
            fields=[
                ('aid', models.IntegerField(primary_key=True, serialize=False)),
                ('day', models.CharField(max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DT.doctor')),
            ],
            options={
                'db_table': 'available_time',
            },
        ),
        migrations.AddField(
            model_name='area',
            name='city_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DT.city'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DT.doctor'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DT.patient'),
        ),
    ]
