# Generated by Django 5.1.4 on 2025-01-01 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_category_alter_organization_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(max_length=50),
        ),
    ]
