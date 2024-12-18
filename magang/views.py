from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
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
    #data yang mau ditampilkan, diurutkan berdasarkan id terberu
    magang_list = MahasiswaMagang.objects.all().order_by('-id')

    #filter berdasarkan status magang
    if request.GET.get('status'):
        if request.GET.get('status') != '0':
            magang_list = magang_list.filter(status_magang=request.GET.get('status'))
            context['status']=int(request.GET.get('status'))
    else:
        context['status'] = 0 # tidak difilter alias ditampilkan semua

    # cari berdasarkan nama/namaproyek/pembimbing
    if request.GET.get('cari'):
        magang_list = magang_list.filter(Q(nama__icontains=request.GET.get('cari'))|Q(proyek_magang__icontains=request.GET.get('cari'))|Q(pembimbing__icontains=request.GET.get('cari')))
        context['cari'] = request.GET.get('cari')

    if request.method == "POST":
        form = MahasiswaMagangForm(request.POST) #ambil form yang telah disubmit
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.created_by = request.user
            form_data.save()
            messages.add_message(request, messages.SUCCESS, 'Data %s berhasil ditambah' % form_data)
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
            messages.add_message(request, messages.INFO, 'Data %s berhasil diubah' % magang_edit)
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
    messages.add_message(request, messages.WARNING, 'Data %s berhasil dihapus' % magang_delete)
    return redirect('data_magang')

@login_required
def get_data(request, id):
    '''
        -mengambil data untuk modal
        '''
    try:
        data = MahasiswaMagang.objects.get(pk=id)
        response = {
            'nama': data.nama,
            'email': data.email,
            'hp': data.no_hp,
            'univ': data.asal_universitas,
            'periode': str(data.tanggal_mulai) + 's/d' + str(data.tanggal_selesai),
            'proyek': data.proyek_magang,
            'status': data.get_status_magang_display(),
            'pembimbing': data.pembimbing,
            'keterangan': data.keterangan,
            'created_by': data.created_by.username,
            'created_at': str(data.created_at),
            'updated_at': str(data.updated_at),
        }
        return JsonResponse(response)
    except MahasiswaMagang.DoesNotExist:
        return JsonResponse({'error': 'Data tidak ditemukan'}, status=404)

@login_required()
def ajax_cari_magang(request):
    query = request.GET.get('cari', '')
    if query:
        magang_list = MahasiswaMagang.objects.filter(
            Q(nama__icontains=query) |
            Q(proyek_magang__icontains=query) |
            Q(pembimbing__icontains=query)
        )
    else:
        magang_list = MahasiswaMagang.objects.all()

    results = []
    for magang in magang_list:
        results.append({
            'id': magang.id,
            'nama': magang.nama,
            'asal_universitas': magang.asal_universitas,
            'tanggal_mulai': magang.tanggal_mulai.strftime('%Y-%m-%d') if magang.tanggal_mulai else None,
            'tanggal_selesai': magang.tanggal_selesai.strftime('%Y-%m-%d') if magang.tanggal_selesai else None,
            'proyek_magang': magang.proyek_magang,
            'pembimbing': magang.pembimbing,
            'status': magang.get_status_magang_display(),  # Ambil label dari choice
        })

    return JsonResponse({'results': results})
