# Generated by Django 4.2.14 on 2024-08-17 11:28

import authentication.manage
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be 10 digits only.', regex='^\\d{10}')])),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('blood_group', models.CharField(blank=True, max_length=5, null=True)),
                ('marital_status', models.BooleanField(default=False)),
                ('height', models.FloatField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('emergency_contact', models.CharField(blank=True, max_length=10, null=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('otp', models.CharField(blank=True, max_length=4, null=True)),
                ('otp_verified', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='customuser_set', related_query_name='customuser', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='customuser_set', related_query_name='customuser', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', authentication.manage.CustomUserManager()),
            ],
        ),
    ]
