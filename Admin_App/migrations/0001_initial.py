# Generated by Django 4.0.5 on 2022-07-20 10:17

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('area', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('pincode', models.CharField(max_length=6)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('account_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmailOtp',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('otp', models.IntegerField()),
                ('is_expire', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneOtp',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=10)),
                ('otp', models.IntegerField()),
                ('is_expire', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceCateory',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('is_payable', models.BooleanField(default=False)),
                ('price', models.JSONField(blank=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('image', models.ImageField(upload_to='category/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('user_type', models.CharField(choices=[(1, 'Admin'), (2, 'Vendor'), (3, 'Customer')], default=1, max_length=1)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone', models.CharField(max_length=10, unique=True)),
                ('first_name', models.CharField(max_length=225)),
                ('last_name', models.CharField(max_length=225)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now)),
                ('coin', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vender',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('profile_photo', models.ImageField(upload_to='profile_photo/')),
                ('pincode', models.CharField(max_length=6)),
                ('address', models.TextField()),
                ('account_active', models.BooleanField(default=False)),
                ('aletrnative_no', models.CharField(max_length=10)),
                ('address_proof_type', models.CharField(max_length=255)),
                ('address_proof_id', models.CharField(max_length=255)),
                ('address_proof_photo', models.ImageField(upload_to='address_proof/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.area')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.city')),
                ('cu', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('is_payable', models.BooleanField(default=False)),
                ('price', models.JSONField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.servicecateory')),
                ('vender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.vender')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('orderid', models.CharField(max_length=100, unique=True)),
                ('is_payable', models.BooleanField(default=False)),
                ('total_price', models.IntegerField(default=0)),
                ('day_price', models.IntegerField(default=0)),
                ('date_today', models.DateField(default=datetime.datetime.now)),
                ('status', models.CharField(choices=[(1, 'Running'), (2, 'Complete'), (3, 'Pending'), (4, 'Cancelled')], default=3, max_length=1)),
                ('is_added_today', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.customer')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.service')),
            ],
        ),
        migrations.CreateModel(
            name='ForgetpasswordOtp',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('otp', models.IntegerField()),
                ('is_expire', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='cu',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='area',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.city'),
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('cu', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
