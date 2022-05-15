from django.contrib import admin
from .models import Category, Consumerunit, Procurementprovider, Allotment, Expenditure, Invoice

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'digits7', 'heading', 'vrsHead']
    list_filter = ['digits7']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Consumerunit)
class ConsumerunitAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent_office']
    list_filter = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Procurementprovider)
class ProcurementproviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'address', 'tin_no', 'vat_no','is_registered','reg_date']
    list_filter = ['name', 'is_registered']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Allotment)
class AllotmentAdmin(admin.ModelAdmin):
    list_display = ['altcode', 'altunit', 'title', 'slug', 'allotedon','altauth','altamount']
    list_filter = ['altcode', 'altunit']
    prepopulated_fields = {'slug': ('title',)}


class InvoiceInline(admin.TabularInline):
      model = Invoice
      extra = 1

@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    inlines =[
        InvoiceInline,  
    ]
    list_display = ['expcode','itemsupplier', 'consunit','is_cheque','updated_at']
    list_filter = ['expcode','itemsupplier', 'consunit','is_cheque']
    prepopulated_fields = {'slug': ('title',)}


