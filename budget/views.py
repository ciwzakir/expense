from django.core.paginator import Paginator
from django.shortcuts import render
from typing import Annotated
from django.db.models import Sum, Count, Avg, Q, Min, Max, Prefetch, Q
from django.db.models.query import QuerySet
from django.forms.forms import Form
from django.shortcuts import get_object_or_404, render
from .forms import AllotmentForm
from .models import Category, Invoice, Procurementprovider, Consumerunit, Expenditure, Allotment
from .filters import AllotmentFilter, SubtotalFilter, ExpFilter
import csv
from django.http import JsonResponse, HttpResponse, response
from datetime import datetime

def alt_all(request):
    granttotal = Allotment.objects.all().aggregate(data=Sum('altamount'))
    subtotalforeach = Allotment.objects.values('altcode__name').annotate(sumalt=Sum('altamount')).order_by('altcode__name')
    allotments = Allotment.objects.all().order_by('altcode__name')
    my_filter = AllotmentFilter(request.POST, queryset=allotments)
    allotments = my_filter.qs
    paginator = Paginator(allotments,5) # Show 5 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request,'budget/allotment/index.html', {
        'granttotal':granttotal,
        'allotments':allotments,
        'subtotalforeach':subtotalforeach,
        'page_obj':page_obj,
        'my_filter':my_filter,
        })

def single_alt(request, slug):
    single_allotment = get_object_or_404(Allotment, slug=slug)
    return render(request, 'budget/allotment/single.html', {'single_allotment': single_allotment})

def exp_all(request):
    expense_details = Expenditure.objects.values(
         'id',
        'itemsupplier__name',
        'expcode__name',
        'consunit__name',
        'is_cheque',
        'taxrate',
        'is_cheque',
        'id',
        'expcode',
        'sum'
        )
    # expense_details = Invoice.objects.values(
    #     'invoices__id',
    #     'invoices__itemsupplier__name',
    #     'invoices__expcode__name',
    #     'invoices__consunit__name',
    #     'invoices__is_cheque',
    #     'invoices__taxrate',
    #     'invoices__is_cheque',  
    #     ).annotate(sumofexp=Sum('amount'))


    subtotal_expfilters = ExpFilter(request.POST, queryset=expense_details)
    expense_details= subtotal_expfilters.qs 

    invs = Invoice.objects.all()

    context = {
        'expense_details':expense_details,
        'subtotal_expfilters':subtotal_expfilters,
        'invs': invs,
    }
    return render(request,'navbar.html', context) 


def single_exp(request, slug):
    single_expenditure = get_object_or_404(Expenditure, slug=slug)
    return render(request,'budget/exp/single.html', {'single_expenditure': single_expenditure})

def grandtotal(request):
    granttotal = Allotment.objects.all().aggregate(data=Sum('altamount'))
    gtoftotalexp =Invoice.objects.all().aggregate(total=Sum('amount'))
    
    return render(request,'budget/summary/grandtotal.html',{
        'granttotal': granttotal,
        'gtoftotalexp': gtoftotalexp,
    })

def sumascodes(request):
    gtoftotalexp =Invoice.objects.all().aggregate(total=Sum('amount'))
    codewisesbutotal = Invoice.objects.values('invoices__expcode__name').annotate(sumofexp=Sum('amount')).order_by('invoices__expcode__name') 
    return render(request,'budget/summary/codes.html', {'codewisesbutotal': codewisesbutotal,'gtoftotalexp': gtoftotalexp,})

def sumofsuppliers(request):
    gtoftotalexp =Invoice.objects.all().aggregate(total=Sum('amount'))
    subtotalbysupplier = Invoice.objects.values('invoices__itemsupplier__name','invoices__itemsupplier__tin_no').annotate(sumofexp=Sum('amount')).order_by('invoices__itemsupplier__name') 
    subtotal_expfilters = SubtotalFilter(request.POST, queryset=subtotalbysupplier)
    subtotalbysupplier= subtotal_expfilters.qs
    
    context = {
        'subtotalbysupplier':subtotalbysupplier,
        'gtoftotalexp':gtoftotalexp,
        'subtotal_expfilters':subtotal_expfilters,
    }
    return render(request,'budget/summary/suppliers.html', context=context)
