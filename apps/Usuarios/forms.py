# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.hashers import *
from SIGIF.apps.security.models import Usuario

class UserForm(forms.ModelForm):
    usu_ced=forms.CharField(label="Cedula",widget=forms.TextInput(attrs={
                'class':'form-control'}))
    usu_nom=forms.CharField(label="Nombres",widget=forms.TextInput(attrs={
                'class':'form-control'}))
    usu_ape=forms.CharField(label="Apellidos",widget=forms.TextInput(attrs={
                'class':'form-control'}))
    usu_sex=forms.CharField(label="Sexo",widget=forms.TextInput(attrs={
                'class':'form-control'}))
    usu_dir=forms.CharField(label="Direccion",widget=forms.TextInput(attrs={
                'class':'form-control'}))
    usu_tel=forms.CharField(label="Telefono",widget=forms.TextInput(attrs={
                'class':'form-control'}))
    usu_ema=forms.CharField(label="Email",widget=forms.TextInput(attrs={
                'class':'form-control'}))
    password=forms.CharField(label="Contraseña ",widget=forms.PasswordInput(attrs={
                'class':'form-control'
            }))
    passwordAgain=forms.CharField(label="Repita_contraseña ",widget=forms.PasswordInput(attrs={
                'class':'form-control'
            }))


    class Meta:
        model= Usuario
        fields=('usu_ced','usu_nom','usu_ape','usu_sex','usu_dir','usu_tel','usu_ema','is_superuser','password',)


    def clean_password(self):
        password = self.cleaned_data['password']
        print()
        if  password<> "":
            return make_password(password)
        else:
            raise forms.ValidationError('No es igual a la contraseña inicial')

