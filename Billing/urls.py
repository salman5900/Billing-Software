from django.urls import path
from . import views

app_name = 'Billing'

urlpatterns = [
    path('', views.BillingPage, name='Billing-home'),
    path('edit/<int:bill_id>/',views.BillingPageEdit, name='edit-bill'),
    path('delete/<int:bill_id>/', views.BillingPageDelete, name='delete-bill'),
    path('dashboard/', views.dashboard, name='dashboard'),

]