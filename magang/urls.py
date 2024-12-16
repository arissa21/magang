from django.urls import path
from . import views

urlpatterns = [
    path('edit/<int:id>/', views.edit_magang, name='edit_magang'),
]
