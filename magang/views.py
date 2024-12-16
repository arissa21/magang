from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import MahasiswaMagang
from .forms import MahasiswaMagangForm

def home(request):
    '''
    -menampilkan data magang
    -menambah data magang
    '''
    context = {}
    template = 'magang/index.html'
    magang_list = MahasiswaMagang.objects.all()
    if request.method == "POST":
        form = MahasiswaMagangForm(request.POST) #ambil form yang telah disubmit
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.created_by = request.user
            form_data.save()
            return redirect('home')
    else:
        form = MahasiswaMagangForm() #form tanpa action post
    context['magang_list'] = magang_list
    context['form'] = form
    return render(request, template , context)

def edit_magang(request, id):
    '''
    mengedit data magang berdasarkan id
    '''
    context = {}
    template = 'magang/index.html'

    magang_list = MahasiswaMagang.objects.all()
    magang_edit = MahasiswaMagang.objects.get(pk=id)  # Ambil data berdasarkan ID
    form = MahasiswaMagangForm(instance=magang_edit)  # instance untuk inisiasi form saat edit
    if request.method == 'POST':
        form = MahasiswaMagangForm(request.POST, instance=magang_edit)  # instance untuk inisiasi form saat edit
        if form.is_valid():
            form.save()  # Simpan perubahan
            return redirect('home')

    context['magang_list'] = magang_list
    context['magang_edit'] = magang_edit
    context['form'] = form
    context['edit'] = True
    return render(request, template, context)