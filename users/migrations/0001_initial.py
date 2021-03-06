# Generated by Django 3.0 on 2019-12-17 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='UserExcel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='excel_sheets/')),
            ],
        ),
        migrations.CreateModel(
            name='StaffDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aadhar_no', models.CharField(max_length=12)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('DOB', models.DateField(max_length=8)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], max_length=1)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.City')),
                ('state', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.State')),
            ],
        ),
        migrations.CreateModel(
            name='DBerDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aadhar_no', models.CharField(max_length=12)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('DOB', models.DateField(max_length=8)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], max_length=1)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.City')),
                ('state', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.State')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.State'),
        ),
    ]
