from django.contrib.auth.models import User
from django.db import models

STATUS_MAGANG =(
    (1,'Aktif'),
    (2,'Selesai'),
)
# Create your models here.
class MahasiswaMagang(models.Model):
    nama = models.CharField(max_length=255)
    email = models.CharField(max_length=50)
    no_hp = models.CharField(max_length=15)
    asal_universitas = models.CharField(max_length=255)
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField(max_length=255)
    status_magang = models.IntegerField(default=0, choices=STATUS_MAGANG)
    proyek_magang = models.CharField(max_length=255)
    pembimbing = models.CharField(max_length=255)
    keterangan = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nama} dari {self.asal_universitas}'