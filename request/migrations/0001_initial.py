# Generated by Django 4.0.2 on 2022-02-08 14:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('reqid', models.BigAutoField(primary_key=True, serialize=False)),
                ('user', models.CharField(default=None, max_length=100)),
                ('attendername', models.CharField(max_length=50)),
                ('attendernumber', models.CharField(max_length=14)),
                ('patientsname', models.CharField(max_length=50)),
                ('patientsage', models.IntegerField()),
                ('bloodgroup', models.CharField(max_length=10)),
                ('hospitalname', models.CharField(max_length=50)),
                ('level', models.IntegerField(default=0)),
                ('city', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('pincode', models.CharField(max_length=6)),
                ('bloodunit', models.IntegerField()),
                ('neededwithin', models.DateField()),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currentstatus', models.CharField(default='pending', max_length=20)),
                ('donorid', models.CharField(blank=True, max_length=10, null=True)),
                ('donateddate', models.DateField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('reqid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.request')),
            ],
        ),
    ]
