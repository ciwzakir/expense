import django_filters
from django_filters import DateFilter, CharFilter
from .models import Allotment, Expenditure, Invoice

class AllotmentFilter(django_filters.FilterSet):
    # title = CharFilter(lookup_expr='iexact', field_name='title')
    start_date = DateFilter(field_name='allotedon', lookup_expr='gte')
    end_date = DateFilter(field_name='allotedon', lookup_expr='lte')
    # auth = CharFilter(lookup_expr='icontains', field_name='altauth')
    
    # class Meta:
    #     model = Allotment
    #     fields = ['altcode','altunit']
        

class ExpFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='updated_at' , lookup_expr='gte')
    end_date = DateFilter(field_name='updated_at' , lookup_expr='lte')
    # title = CharFilter(lookup_expr='iexact', field_name='title')
    
    class Meta:
        model = Expenditure
        fields =['expcode','itemsupplier']
        # fields =['expcode','consunit', 'itemsupplier','is_cheque']
        
class SubtotalFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='invoices__updated_at', lookup_expr='gte')
    end_date = DateFilter(field_name='invoices__updated_at', lookup_expr='lte')
        
    class Meta:
        model = Invoice
        fields =['invoices__itemsupplier']
        
