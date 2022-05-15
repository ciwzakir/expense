from .models import Category, Consumerunit, Invoice, Procurementprovider

def categories(request):
    return {
        'categories': Category.objects.all()
    }

def suppliers(request):
    return {
        'suppliers': Procurementprovider.objects.all()
    }

def consumers(request):
    return {
        'consumers': Consumerunit.objects.all()
    }

def invoices(request):
    return {
        'invoices': Invoice.objects.all()
    }

