from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render

from .models import MahasiswaMagang
from .forms import MahasiswaMagangForm

def home(request):
    '''
    -menampilkan halaman utama
    '''
    context = {}
    template = 'magang/index.html'
    return render(request, template , context)

@login_required
def data_magang(request):
    '''
    -menampilkan data magang
    -menambah data magang
    '''
    context = {}
    template = 'magang/data_magang.html'
    magang_list = MahasiswaMagang.objects.all()

    #filter berdasarkan status magang
    if request.GET.get('status'):
        if request.GET.get('status') != '0':
            magang_list = magang_list.filter(status_magang=request.GET.get('status'))
            context['status']=int(request.GET.get('status'))
    else:
        context['status'] = 0 # tidak difilter alias ditampilkan semua

    if request.method == "POST":
        form = MahasiswaMagangForm(request.POST) #ambil form yang telah disubmit
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.created_by = request.user
            form_data.save()
            return redirect('data_magang')
    else:
        form = MahasiswaMagangForm() #form tanpa action post
    context['magang_list'] = magang_list
    context['form'] = form
    return render(request, template , context)

@login_required
def edit_magang(request, id):
    '''
    mengedit data magang berdasarkan id
    '''
    context = {}
    template = 'magang/data_magang.html'

    magang_list = MahasiswaMagang.objects.filter(pk=id)
    magang_edit = MahasiswaMagang.objects.get(pk=id)  # Ambil data berdasarkan ID
    form = MahasiswaMagangForm(instance=magang_edit)  # instance untuk inisiasi form saat edit
    if request.method == 'POST':
        form = MahasiswaMagangForm(request.POST, instance=magang_edit)  # instance untuk inisiasi form saat edit
        if form.is_valid():
            form.save()  # Simpan perubahan
            return redirect('data_magang')

    context['magang_list'] = magang_list
    context['magang_edit'] = magang_edit
    context['form'] = form
    context['edit'] = True
    return render(request, template, context)

@login_required
def delete_magang(request, id):
    '''
    mengedit data magang berdasarkan id
    '''
    magang_delete = MahasiswaMagang.objects.get(pk=id)  # Ambil data berdasarkan ID
    magang_delete.delete()
    messages.add_message(request, messages.WARNING, 'Data berhasil dihapus')
    return redirect('data_magang')