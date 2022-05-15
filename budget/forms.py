from django import forms
from django.db import models
from django.forms import fields
from .models import Allotment

class AllotmentForm(forms.Form):
    start_date = forms.DateField(required=False, label="Insert start date")
    end_date = forms.DateTimeField(required=False, label="Insert End date")

    class Meta:
        model = Allotment
        fields = ['start_date', 'end_date']
