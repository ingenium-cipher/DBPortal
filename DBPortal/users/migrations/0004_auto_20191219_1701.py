# Generated by Django 3.0 on 2019-12-19 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20191218_0606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dberdetail',
            name='aadhar_no',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='StaffDetail',
        ),
    ]
