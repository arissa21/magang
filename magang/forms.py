from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from .models import MahasiswaMagang

class MahasiswaMagangForm(forms.ModelForm):
    class Meta:
        model = MahasiswaMagang
        exclude = [
            'created_by', 'created_at', 'updated_at',
        ]
        widgets = {
            'tanggal_mulai': forms.DateInput(attrs={'type': 'date'}),
            'tanggal_selesai': forms.DateInput(attrs={'type': 'date'}),
            'keterangan': forms.Textarea(attrs={'rows':3}),
            'status_magang': forms.Select(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'no_hp': forms.NumberInput(attrs={'class': 'form-control'}),
        }
