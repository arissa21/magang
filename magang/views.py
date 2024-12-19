from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.shortcuts import render

from .models import MahasiswaMagang
from .forms import MahasiswaMagangForm


def home(request):
    '''
    - Menampilkan halaman utama atau beranda (home page).
    - Fungsi ini menangani permintaan HTTP dari pengguna yang mengakses halaman utama aplikasi.

    Penjelasan:
    1. Variabel `context` disiapkan untuk menyimpan data yang akan dikirim ke template.
       Dalam hal ini, `context` kosong karena tidak ada data yang perlu dikirimkan ke template.
    2. Variabel `template` menyimpan nama file template yang akan digunakan untuk merender halaman,
       yaitu 'magang/index.html'.
    3. Fungsi `render` digunakan untuk menggabungkan template dengan `context` dan menghasilkan
       HTML yang akan dikirimkan ke browser pengguna sebagai respons.
    '''
    context = {}  # Menyiapkan konteks data yang akan dikirim ke template (kosong pada kasus ini)
    template = 'magang/index.html'  # Nama template yang akan dirender
    return render(request, template, context)  # Menggabungkan template dengan context dan mengirimkan HTML ke pengguna


@login_required
def data_magang(request):
    '''
    - Menampilkan data magang
    - Menambah data magang baru jika ada permintaan POST
    '''
    context = {}
    template = 'magang/data_magang.html'

    # Ambil semua data mahasiswa magang, urutkan berdasarkan ID terbaru
    magang_list = MahasiswaMagang.objects.all().order_by('-id')

    # Filter berdasarkan status magang jika ada parameter 'status' dalam URL
    if request.GET.get('status'):
        if request.GET.get('status') != '0':
            magang_list = magang_list.filter(status_magang=request.GET.get('status'))
            context['status'] = int(request.GET.get('status'))
    else:
        context['status'] = 0  # Jika tidak ada filter status, tampilkan semua data

    # Jika ada POST request (misalnya menambah data magang baru)
    if request.method == "POST":
        form = MahasiswaMagangForm(request.POST)  # Ambil data dari form
        if form.is_valid():  # Validasi form
            form_data = form.save(commit=False) #tidak langsung dilakukan commit, jadi form akan dimodifikasi dulu
            #proses modifikasi
            form_data.created_by = request.user  # Set user yang membuat data
            form_data.save()  # Simpan data magang dari form yang telah dimodifikasi
            messages.add_message(request, messages.SUCCESS, 'Data %s berhasil ditambah' % form_data)
            return redirect('data_magang')  # Redirect ke halaman data magang setelah berhasil tambah
    else:
        form = MahasiswaMagangForm()  # Jika GET, tampilkan form kosong untuk penambahan data baru

    context['magang_list'] = magang_list
    context['form'] = form
    return render(request, template, context)  # Render halaman dengan data magang dan form


@login_required
def edit_magang(request, id):
    '''
    Mengedit data magang berdasarkan ID
    '''
    context = {}
    template = 'magang/data_magang.html'

    magang_list = MahasiswaMagang.objects.filter(pk=id)  # Ambil data berdasarkan ID
    magang_edit = MahasiswaMagang.objects.get(pk=id)  # Ambil data magang yang akan diedit
    form = MahasiswaMagangForm(instance=magang_edit)  # Inisialisasi form dengan data yang sudah ada (magang_edit)

    # Jika ada POST request, berarti form sedang disubmit untuk update
    if request.method == 'POST':
        form = MahasiswaMagangForm(request.POST, instance=magang_edit)  # Ambil data dari form POST
        if form.is_valid():  # Validasi form
            form.save()  # Simpan perubahan data magang. Yang ini langsung dicommit, karena tidak perlu ada modifikasi form
            messages.add_message(request, messages.INFO, 'Data %s berhasil diubah' % magang_edit)
            return redirect('data_magang')  # Redirect ke halaman data magang setelah sukses edit

    context['magang_list'] = magang_list
    context['magang_edit'] = magang_edit
    context['form'] = form
    context['edit'] = True  # Tampilkan flag edit pada halaman
    return render(request, template, context)  # Render halaman dengan data magang yang diedit dan form


@login_required
def delete_magang(request, id):
    '''
    Menghapus data magang berdasarkan ID
    '''
    magang_delete = MahasiswaMagang.objects.get(pk=id)  # Ambil data berdasarkan ID
    magang_delete.delete()  # Hapus data magang
    messages.add_message(request, messages.WARNING, 'Data %s berhasil dihapus' % magang_delete)
    return redirect('data_magang')  # Redirect ke halaman data magang setelah data dihapus


@login_required
def get_data(request, id):
    '''
    Mengambil data magang berdasarkan ID untuk ditampilkan di modal
    '''
    try:
        data = MahasiswaMagang.objects.get(pk=id)  # Ambil data berdasarkan ID
        # Siapkan data yang akan dikirimkan dalam format response JSON
        response = {
            'nama': data.nama,
            'email': data.email,
            'hp': data.no_hp,
            'nim': data.nim,
            'univ': data.asal_universitas,
            'periode': str(data.tanggal_mulai) + 's/d' + str(data.tanggal_selesai),
            'proyek': data.proyek_magang,
            'status': data.get_status_magang_display(),  # Ambil label status magang
            'pembimbing': data.pembimbing,
            'keterangan': data.keterangan,
            'created_by': data.created_by.username,
            'created_at': str(data.created_at),
            'updated_at': str(data.updated_at),
        }
        return JsonResponse(response)  # Kembalikan data dalam format JSON
    except MahasiswaMagang.DoesNotExist:
        return JsonResponse({'error': 'Data tidak ditemukan'}, status=404)  # Jika data tidak ditemukan


@login_required()
def ajax_cari_magang(request):
    '''
    Melakukan pencarian data magang berdasarkan parameter 'cari'
    '''
    query = request.GET.get('cari', '')  # Ambil query pencarian dari GET parameter
    if query:
        # Filter data magang berdasarkan nama, proyek, atau pembimbing yang mengandung karakter pada query
        magang_list = MahasiswaMagang.objects.filter(
            Q(nama__icontains=query) |
            Q(proyek_magang__icontains=query) |
            Q(pembimbing__icontains=query)
        ) #icontain, berarti mengandung string tanpa memperhatikan case nya => insensitive case
    else:
        magang_list = MahasiswaMagang.objects.all()  # Jika tidak ada query, tampilkan semua data

    results = []
    # Siapkan data hasil pencarian untuk dikirimkan dalam JSON
    for magang in magang_list:
        results.append({
            'id': magang.id,
            'nama': magang.nama,
            'nim': magang.nim,
            'asal_universitas': magang.asal_universitas,
            'tanggal_mulai': magang.tanggal_mulai.strftime('%Y-%m-%d') if magang.tanggal_mulai else None,
            'tanggal_selesai': magang.tanggal_selesai.strftime('%Y-%m-%d') if magang.tanggal_selesai else None,
            'proyek_magang': magang.proyek_magang,
            'pembimbing': magang.pembimbing,
            'status': magang.get_status_magang_display(),  # Ambil label status magang
        })

    return JsonResponse({'results': results})  # Kembalikan hasil pencarian dalam format JSON