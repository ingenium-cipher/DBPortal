# Generated by Django 2.2.7 on 2019-12-18 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffdetail',
            name='DOB',
            field=models.DateField(max_length=8, null=True),
        ),
    ]
