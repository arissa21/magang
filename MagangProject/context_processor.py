def app_settings(request):
    """
    Context processor untuk menyediakan judul aplikasi dan nama aplikasi.
    """
    return {
        'APP_TITLE': 'Dashboard Mahasiswa Magang Disdukcapil Surakarta',
        'APP_NAME': 'Magang Dukcapil <sup>Surakarta</sup>',
    }
