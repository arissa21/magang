from django.contrib import admin

# Register your models here.
from magang.models import MahasiswaMagang


class MahasiswaMagangAdmin(admin.ModelAdmin):
    list_display = [f.name for f in MahasiswaMagang._meta.fields]
    search_fields = ('short_url','pemilik_url')

admin.site.register(MahasiswaMagang, MahasiswaMagangAdmin)