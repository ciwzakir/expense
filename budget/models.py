from django.db.models.deletion import CASCADE, RESTRICT
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.expressions import Value
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import datetime

class Category(models.Model):
    name = models.CharField(
        verbose_name=_("BudgetCode  Category Name"),
        help_text= _("Required and Unique"),
        max_length=255,
        unique=True,
    )  
    slug = models.SlugField(
        verbose_name=_("BudgetCode Slug"),
        max_length=255,
        unique=True,
    )
    digits7 = models.IntegerField(blank=False)
    heading = models.CharField(max_length=255, blank= False)
    vrsHead = models.CharField(max_length=3, blank=False)

    class Meta:
        verbose_name = _('BudgetCode')
        verbose_name_plural = _('BudgetCodes')

    def get_absolute_url(self):
        return reverse("budget:category_list", args=[self.slug])
        
        """ budget: category_list = comes from urls file not from views file """

    def __str__(self):
        return self.name

    """ 
    BudgetCode End Here    

    """ 


class Consumerunit(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=25, unique =True)
    parent_office = models.CharField(max_length=50, db_index=True)

    class Meta:
        verbose_name = _("Consumer Unit Name")
        verbose_name_plural = _("Consumer Unit Names")

    def __str__(self):
       return self.name

class Procurementprovider(models.Model):
    name = models.CharField(
    verbose_name=_("Name"),
    help_text= _("Required"),
    max_length=255,
    blank=False,
    ) 
    slug = models.SlugField(max_length=255, unique =True)
    address = models.CharField(max_length=255,)
    tin_no = models.CharField(max_length=13, blank=False,)
    vat_no = models.CharField(max_length=13, blank=False,)
    is_registered = models.BooleanField(default=True)
    reg_date = models.DateField()
    

    class Meta:
        verbose_name = _("Procurement Provider Name")
        verbose_name_plural = _("Procurement Provider Names")

    def __str__(self):
       return self.name

class Allotment(models.Model):
    altcode = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="allotments", verbose_name=_("Budget Codes"))
    altunit = models.ForeignKey(Consumerunit, on_delete=models.CASCADE, verbose_name=_("For Which Office"))
    title = models.CharField(
        verbose_name=_("title"),
        help_text="Required",
        max_length=255)

    slug = models.SlugField(max_length=255, unique=True)
    allotedon = models.DateField(verbose_name=_("Allotment Date"))
    altauth = models.CharField(max_length=70, default="23.03.2600.039.51.001.21.000/    A", verbose_name=_("Vide Ltr Reference"))
    altamount = models.DecimalField(max_digits=12, decimal_places=2, blank=False, verbose_name=_("Alloted Amount "))

    class Meta:
        verbose_name = 'Allotment'
        verbose_name_plural = 'Allotment'
        ordering = ('altcode',)

    def get_absolute_url(self):
        return reverse('budget:single_alts', args=[self.slug])
        """fun: single-alts = comes from urls file not from views file """
            
    def __str__(self):
        return self.title

class Expenditure(models.Model):
    title = models.CharField(
    verbose_name=_("title"),
    help_text="Required",
    max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    expcode = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name="alt_exp", verbose_name=_("Budget Codes"))
    consunit = models.ForeignKey(Consumerunit, on_delete=models.RESTRICT, verbose_name=_("Consumer Office Name"))
    itemsupplier = models.ForeignKey(Procurementprovider, on_delete=models.RESTRICT, verbose_name=_("Select Your Supplier"))
    is_cheque = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    taxrate = models.DecimalField(blank=False, max_digits=4, decimal_places=2,verbose_name=_("Income TAX Rate"), default=0)
    taxamount = models.DecimalField(blank=False, max_digits=8, decimal_places=2,verbose_name=_("Income TAX Amount"), default=0)
    vatrate = models.DecimalField(blank=False, max_digits=4, decimal_places=2,verbose_name=_("VAT Rate"), default=0)
    vatamount = models.DecimalField(blank=False, max_digits=8, decimal_places=2,verbose_name=_("VAT Amount"), default=0)
    created_at = models.DateField(_("Created Date"), default=datetime.date.today)
    updated_at = models.DateField(_("Update Date"), default=datetime.date.today)

    sum = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)

    def save(self, *args, **kwargs):
        self.sum = (self.taxrate * self.vatrate)
        return super().save(*args, **kwargs)
    
    def saves(self):
        self.inv_total = 0
        self.inv_total += self.amount
        return super().saves(self)

    checked_by =  models.CharField(
    verbose_name=_("Checked BY Whom"),
    help_text="Required",
    max_length=255, default="Abdur Rahman",
    blank=False
    )
    class Meta:
        verbose_name = 'Expenditure'
        verbose_name_plural = 'Expenditures'

    def get_absolute_url(self):
        return reverse('budget:single_expense', args=[self.slug]) 
        
        """fun: single-expense = comes from urls name """       
    def __str__(self):
        return self.title

class Invoice(models.Model):
    invoices= models.ForeignKey(Expenditure, on_delete=models.CASCADE, related_name="invoice_details")
    invoice_no = models.CharField(max_length=30)
    invoice_date = models.DateField()
    rv_no      = models.CharField(max_length=6)
    amount = models.DecimalField(max_digits=12, decimal_places=2) 
    # inv_total =models.DecimalField(max_digits=12, decimal_places=2, default= 0.00) 
    


    def save(self):
        self.inv_total = 0
        self.inv_total += self.amount
        return super().save(self)
       
   
    class Meta:
        verbose_name = _("Invoice Detail")
        verbose_name_plural = _("Invoice Details")
