from django.contrib import admin

# Register your models here.
from magang.models import MahasiswaMagang


class MahasiswaMagangCantik(admin.ModelAdmin):
    list_display = [f.name for f in MahasiswaMagang._meta.fields]
    search_fields = ('nama','proyek_magang')

admin.site.register(MahasiswaMagang, MahasiswaMagangCantik)