# Generated by Django 5.1.4 on 2024-12-31 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_remove_organization_org_name_organization_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='orgname',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
