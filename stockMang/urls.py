from django.urls import path
from . import views

app_name = 'stockMang'

urlpatterns = [
    path('', views.stock, name='stock'),
    path('add/', views.addStock, name='addStock'),
    path('edit/<int:id>', views.editStock, name='editStock')
]