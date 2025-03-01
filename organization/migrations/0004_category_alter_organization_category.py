# Generated by Django 5.1.4 on 2025-01-01 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_organization_orgname'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='organization',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.category'),
        ),
    ]
