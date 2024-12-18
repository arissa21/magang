# Generated by Django 5.1.4 on 2024-12-15 00:02

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
            name='MahasiswaMagang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=50)),
                ('no_hp', models.CharField(max_length=15)),
                ('asal_universitas', models.CharField(max_length=255)),
                ('tanggal_mulai', models.DateField()),
                ('tanggal_selesai', models.DateField(max_length=255)),
                ('status_magang', models.IntegerField(choices=[(1, 'Aktif'), (2, 'Selesai')], default=0)),
                ('proyek_magang', models.CharField(max_length=255)),
                ('keterangan', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
