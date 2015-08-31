__author__ = 'luist'
from django import forms
from apps.security.models import *

class PedidosForm(forms.ModelForm):
    class Meta:
        model = Pedido
        widgets={
            'id':forms.NumberInput(attrs={
                'class':'form-control'
            }),
            'ped_num':forms.NumberInput(attrs={
                'class':'form-control'
            }),
            'ped_fec':forms.DateInput(attrs={
                'class':'form-control',
                'type':'date'
            }),
            'prov_id':forms.Select(attrs={
                'class':'form-control'
            }),
            'usu_id':forms.Select(attrs={
                'class':'form-control'
            })
        }
        fields = '__all__'


