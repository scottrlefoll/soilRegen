from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from .models import SoilReport
from django import forms
from .models import Farm
import requests
import pandas as pd

class AddSoilReportForm(forms.ModelForm):
    class Meta:
        model = SoilReport
        fields = ['report_date', 'lab_name', 'field']
        labels = {
            'report_date': 'Report Date',
            'lab_name': 'Lab Name',
            'field': 'Field'
        }
        widgets = {
            'report_date': forms.DateInput(attrs={'required': True}),
            'lab_name': forms.TextInput(attrs={'required': True}),
            'field': forms.Select(attrs={'required': True})
        }

class DeleteSoilReportForm(forms.ModelForm):
    class Meta:
        model = SoilReport
        fields = []
        widgets = {'report_id': forms.HiddenInput()}
        
class AddFarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['farm_name', 'street_address', 'town', 'state', 'zip']
        labels = {
            'Farm name': 'Name',
            'Street address': 'Street Address',
            'Town': 'Town',
            'State': 'State',
            'Zip': 'Zip'
        }
        widgets = {
            'farm_name': forms.TextInput(attrs={'required': True}),
            'street_address': forms.TextInput(attrs={'required': True}),
            'town': forms.TextInput(attrs={'required': True}),
            'state': forms.TextInput(attrs={'required': True}),
            'zip': forms.TextInput(attrs={'required': True})
        }


class DeleteFarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = []
        widgets = {'id': forms.HiddenInput()}
