# Generated by Django 5.1.4 on 2025-01-01 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_alter_category_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='admin_approval',
            field=models.CharField(choices=[('approved', 'Approved'), ('not approved', 'Not Approved')], default='not approved', max_length=20),
        ),
    ]
