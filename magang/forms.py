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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'  # Add optional Bootstrap styling
        self.helper.layout = Layout(
            Field('nama'),
            Field('email'),
            Field('no_hp'),
            Field('asal_universitas'),
            Field('tanggal_mulai'),
            Field('tanggal_selesai'),
            Field('status_magang'),
            Field('proyek_magang'),
            Field('keterangan'),
        )
        self.helper.add_input(Submit('submit', 'Simpan'))
