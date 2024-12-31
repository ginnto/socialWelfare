# Generated by Django 5.1.4 on 2024-12-31 10:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='user', max_length=50)),
                ('photo', models.ImageField(upload_to='userimage')),
                ('cust_name', models.CharField(max_length=50)),
                ('cust_gender', models.CharField(max_length=20)),
                ('cust_houseno', models.CharField(max_length=50)),
                ('cust_city', models.CharField(max_length=50)),
                ('cust_district', models.CharField(max_length=50)),
                ('cust_pincode', models.IntegerField()),
                ('cust_email', models.EmailField(max_length=50)),
                ('cust_phno', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
