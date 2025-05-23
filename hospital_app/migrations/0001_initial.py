# Generated by Django 5.2 on 2025-05-10 15:58

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(default='India', max_length=100)),
                ('pincode', models.CharField(help_text='Enter a valid pincode (4 to 10 digits)', max_length=10, validators=[django.core.validators.RegexValidator(regex='^\\d{4,10}$')])),
                ('phone', models.CharField(help_text="Enter phone in format: '+919999999999'", max_length=15, validators=[django.core.validators.RegexValidator(regex='^\\+?\\d{7,15}$')])),
                ('email', models.EmailField(blank=True, max_length=254, null=True, validators=[django.core.validators.EmailValidator()])),
                ('website', models.URLField(blank=True, null=True, validators=[django.core.validators.URLValidator()])),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hospitals_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hospitals_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='HospitalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='hospital_images/')),
                ('caption', models.CharField(blank=True, max_length=255)),
                ('sequence', models.PositiveIntegerField(default=0, help_text='Lower numbers appear first')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='hospital_app.hospital')),
            ],
            options={
                'ordering': ['sequence', 'uploaded_at'],
            },
        ),
        migrations.CreateModel(
            name='HospitalReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='hospital_app.hospital')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='hospital',
            index=models.Index(fields=['city'], name='hospital_ap_city_6ca709_idx'),
        ),
        migrations.AddIndex(
            model_name='hospital',
            index=models.Index(fields=['state'], name='hospital_ap_state_07fc96_idx'),
        ),
        migrations.AddIndex(
            model_name='hospital',
            index=models.Index(fields=['is_active'], name='hospital_ap_is_acti_5c3fb7_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='hospitalreview',
            unique_together={('hospital', 'user')},
        ),
    ]
