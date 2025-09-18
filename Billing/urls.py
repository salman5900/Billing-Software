from django.urls import path
from . import views

app_name = 'Billing'

urlpatterns = [
    path('', views.BillingPage, name='Billing-home'),
]