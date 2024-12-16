def app_settings(request):
    """
    Context processor untuk menyediakan judul aplikasi dan nama aplikasi.
    """
    return {
        'APP_TITLE': 'Dashboard Magang Disdukcapil Surakarta',
        'APP_NAME': 'Magang Disdukcapil Surakarta',
        'COMPANY_NAME': 'Disdukcapil Surakarta'
    }
