from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


def validar_cedula(value):
        ced_cliente=value
        msg = "La Cedula introducida no es valida"
        if ced_cliente.isdigit():
            cant_num_cedula=len(ced_cliente.split()[0])
            msg = "La Cedula introducida no es valida"
            if cant_num_cedula == 10 :
                valores = [ int(ced_cliente[x]) * (2 - x % 2) for x in range(9) ]
                suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
                veri = 10 - (suma - (10 * (suma / 10)))
                if int(ced_cliente[9]) == int(str(veri)[-1:]):
                    return ced_cliente
                else:
                    raise forms.ValidationError(msg)
            else:raise forms.ValidationError(msg)
        else:raise forms.ValidationError("esto no es nada que se le parezca a un numero de cedula")


class UserManager(BaseUserManager,models.Manager):
    def _create_user(self,usu_ced,usu_nom,usu_ema,password,is_staff,
                    is_superuser,**extra_fields):
        usu_ema=self.normalize_email(usu_ema)
        if not usu_ema:
            raise ValueError('El email debe ser Obligatorio!')
        user = self.model(usu_ced=usu_ced,usu_nom=usu_nom,usu_ema=usu_ema,is_staff=is_staff,
                            is_active=True,is_superuser=is_superuser,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,usu_ced,usu_nom,usu_ema,password=None,**extra_fields):
        return self._create_user(usu_ced,usu_nom,usu_ema,password,False,False,**extra_fields)

    def create_superuser(self,usu_ced,usu_nom,usu_ema,password=None,**extra_fields):
        return self._create_user(usu_ced,usu_nom,usu_ema,password,True,True,**extra_fields)


class Usuario(AbstractBaseUser,PermissionsMixin):
    usu_ced = models.CharField("Cedula", max_length=10,unique=True,validators=[validar_cedula]) 
    usu_nom = models.CharField("Nombres",max_length=50)
    usu_ape = models.CharField("Apellidos",max_length=50)
    usu_sex = models.CharField("Sexo",max_length=1) 
    usu_fec_nac = models.DateField("Fecha Nacimiento",auto_now_add=True) 
    usu_dir = models.CharField("Direccion",max_length=150) 
    usu_tel = models.CharField("Telefono",max_length=10) 
    usu_ema = models.EmailField("Email",max_length=30) 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    object=UserManager()

    USERNAME_FIELD = 'usu_ced'
    REQUIRED_FIELDS = ['usu_ema','usu_nom']

    def __unicode__(self):
        return self.usu_ced
    def __str__(self):
        return self.usu_nom



class Cliente(models.Model):
    cli_ced = models.CharField("Cedula", max_length=10,unique=True,validators=[validar_cedula])
    cli_nom = models.CharField("Nombres",max_length=50)
    cli_ape = models.CharField("Apellidos",max_length=50)
    cli_dir = models.CharField("Direccion",max_length=150)
    cli_tel = models.CharField("Telefono",max_length=10)
    cli_est =models.BooleanField("Estado",default=True ,help_text='indica si el cliente se encuentra habilitado')

    def __unicode__(self):
        return self.cli_ced
    def __str__(self):
        return self.cli_nom




class Proveedor(models.Model):
    prov_nom = models.CharField("Nombre",max_length=40)
    prov_nom_con = models.CharField("Nombre_Contacto",max_length=40)
    prov_car_con = models.CharField("Cargo_Contacto",max_length=40)
    prov_ciu = models.CharField("Ciudad",max_length=40)
    prov_dir = models.CharField("Direccion",max_length=80)
    prov_ema =models.EmailField("Email",max_length=40)
    est_proveedor = models.BooleanField("Estado",default=True)
    
    def __unicode__(self):
        return self.prov_nom   
    def __str__(self):
        return self.prov_nom



class Producto(models.Model):
    pro_nom = models.CharField("Nombre del Producto", max_length=50)
    pro_des = models.TextField("Descripcion del Producto",max_length=100,help_text="Detalles adicionales del producto del producto")
    pro_pre = models.FloatField("Precio del Producto")
    pro_sto_min =models.IntegerField("Stock minimo",default=5)
    pro_sto_act = models.IntegerField("Stock Actual",default=1)
    pro_mar = models.CharField("Marca",max_length=30)
    pro_est = models.BooleanField("Estado",default=True)
    prov_id = models.ForeignKey(Proveedor,verbose_name="Proveedor", limit_choices_to={'est_proveedor':True},on_delete=models.PROTECT)

    def __unicode__(self):
        return self.pro_nom
    def __str__(self):
        return self.pro_nom


class Factura(models.Model):
    fac_num =models.IntegerField()
    fac_fec = models.DateField(max_length=10)
    fac_sub_tot = models.FloatField(max_length=10)
    fac_iva =models.FloatField(max_length=10)
    fac_des =models.CharField(max_length=10)
    fac_tot =models.FloatField(max_length=10)
    cli_id =models.ForeignKey(Cliente)



class Detalle_Factura(models.Model):
    can_det_fac=models.FloatField(max_length=10)
    pre_uni_det_fac=models.FloatField(max_length=10)
    pre_tot_det_fac=models.FloatField(max_length=10)
    fac_id =models.ForeignKey(Factura)
    pro_id =models.ForeignKey(Producto)



class Pedido(models.Model):
    ped_num = models.IntegerField()
    ped_fec = models.DateField(max_length=10)
    prov_id = models.ForeignKey(Proveedor, default=True)
    usu_id = models.ForeignKey(Usuario)



class Detalle_Pedido(models.Model):
    det_ped_can = models.FloatField(max_length=10)
    det_ped_des = models.TextField("Descripcion del Producto",max_length=100,help_text="Detalles adicionales del producto del producto")
    ped_id =models.ForeignKey(Pedido)
    pro_id =models.ForeignKey(Producto)
