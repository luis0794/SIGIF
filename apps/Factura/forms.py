__author__ = 'luist'
from django import forms
from apps.security.models import *

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        widgets={
            'fac_num':forms.NumberInput(attrs={
                'class':'form-control'
            }),
            'fac_fec':forms.DateInput(attrs={
                'class':'form-control',
                'type':'date'
            }),
            'fac_sub_tot':forms.NumberInput(attrs={
                'class':'form-control',
                'step': '0.01'
            }),
            'fac_iva':forms.NumberInput(attrs={
                'class':'form-control',
                'step': '0.01'
            }),
            'fac_des':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'fac_tot':forms.NumberInput(attrs={
                'class':'form-control',
                'step': '0.01'
            }),
            'cli_id':forms.Select(attrs={
                'class':'form-control'
            })
        }
        fields = '__all__'