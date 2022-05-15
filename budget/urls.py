from django.urls import path

from . import views

app_name = 'budget'

urlpatterns = [
    path('alt', views.alt_all, name='all_alts'),
    path('alt/<slug:slug>/', views.single_alt, name='single_alts'),
    path('', views.exp_all, name='all_expenditure'),
    path('exp/<slug:slug>/', views.single_exp, name='single_expense'),
    path('grand', views.grandtotal, name='grand_total'),
    path('codes', views.sumascodes, name='sumof_codes'),
    path('suppliers', views.sumofsuppliers, name='somof_suppliers'),
   ]
