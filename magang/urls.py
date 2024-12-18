from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.data_magang, name='data_magang'),
    path('edit/<int:id>/', views.edit_magang, name='edit_magang'),
    path('delete/<int:id>/', views.delete_magang, name='delete_magang'),
    path('get-data/<int:id>/', views.get_data, name='get_data'),
    path('ajax/cari-magang/', views.ajax_cari_magang, name='ajax_cari_magang'),
]
