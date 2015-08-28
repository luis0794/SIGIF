# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import SIGIF.apps.security.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('usu_ced', models.CharField(unique=True, max_length=10, verbose_name=b'Cedula', validators=[SIGIF.apps.security.models.validar_cedula])),
                ('usu_nom', models.CharField(max_length=50, verbose_name=b'Nombres')),
                ('usu_ape', models.CharField(max_length=50, verbose_name=b'Apellidos')),
                ('usu_sex', models.CharField(max_length=1, verbose_name=b'Sexo')),
                ('usu_fec_nac', models.DateField(auto_now_add=True, verbose_name=b'Fecha Nacimiento')),
                ('usu_dir', models.CharField(max_length=150, verbose_name=b'Direccion')),
                ('usu_tel', models.CharField(max_length=10, verbose_name=b'Telefono')),
                ('usu_ema', models.EmailField(max_length=30, verbose_name=b'Email')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cli_ced', models.CharField(unique=True, max_length=10, verbose_name=b'Cedula', validators=[SIGIF.apps.security.models.validar_cedula])),
                ('cli_nom', models.CharField(max_length=50, verbose_name=b'Nombres')),
                ('cli_ape', models.CharField(max_length=50, verbose_name=b'Apellidos')),
                ('cli_dir', models.CharField(max_length=150, verbose_name=b'Direccion')),
                ('cli_tel', models.CharField(max_length=10, verbose_name=b'Telefono')),
                ('cli_est', models.BooleanField(default=True, help_text=b'indica si el cliente se encuentra habilitado', verbose_name=b'Estado')),
            ],
        ),
        migrations.CreateModel(
            name='Detalle_Factura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('can_det_fac', models.FloatField(max_length=10)),
                ('pre_uni_det_fac', models.FloatField(max_length=10)),
                ('pre_tot_det_fac', models.FloatField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Detalle_Pedido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('det_ped_can', models.FloatField(max_length=10)),
                ('det_ped_des', models.TextField(help_text=b'Detalles adicionales del producto del producto', max_length=100, verbose_name=b'Descripcion del Producto')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fac_num', models.IntegerField()),
                ('fac_fec', models.DateField(max_length=10)),
                ('fac_sub_tot', models.FloatField(max_length=10)),
                ('fac_iva', models.FloatField(max_length=10)),
                ('fac_des', models.CharField(max_length=10)),
                ('fac_tot', models.FloatField(max_length=10)),
                ('cli_id', models.ForeignKey(to='security.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ped_num', models.IntegerField()),
                ('ped_fec', models.DateField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pro_nom', models.CharField(max_length=50, verbose_name=b'Nombre del Producto')),
                ('pro_des', models.TextField(help_text=b'Detalles adicionales del producto del producto', max_length=100, verbose_name=b'Descripcion del Producto')),
                ('pro_pre', models.FloatField(verbose_name=b'Precio del Producto')),
                ('pro_sto_min', models.IntegerField(default=5, verbose_name=b'Stock minimo')),
                ('pro_sto_act', models.IntegerField(default=1, verbose_name=b'Stock Actual')),
                ('pro_mar', models.CharField(max_length=30, verbose_name=b'Marca')),
                ('pro_est', models.BooleanField(default=True, verbose_name=b'Estado')),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prov_nom', models.CharField(max_length=40, verbose_name=b'Nombre')),
                ('prov_nom_con', models.CharField(max_length=40, verbose_name=b'Nombre_Contacto')),
                ('prov_car_con', models.CharField(max_length=40, verbose_name=b'Cargo_Contacto')),
                ('prov_ciu', models.CharField(max_length=40, verbose_name=b'Ciudad')),
                ('prov_dir', models.CharField(max_length=80, verbose_name=b'Direccion')),
                ('prov_ema', models.EmailField(max_length=40, verbose_name=b'Email')),
                ('est_proveedor', models.BooleanField(default=True, verbose_name=b'Estado')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='prov_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Proveedor', to='security.Proveedor'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='prov_id',
            field=models.ForeignKey(to='security.Proveedor'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='usu_id',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='detalle_pedido',
            name='ped_id',
            field=models.ForeignKey(to='security.Pedido'),
        ),
        migrations.AddField(
            model_name='detalle_pedido',
            name='pro_id',
            field=models.ForeignKey(to='security.Producto'),
        ),
        migrations.AddField(
            model_name='detalle_factura',
            name='fac_id',
            field=models.ForeignKey(to='security.Factura'),
        ),
        migrations.AddField(
            model_name='detalle_factura',
            name='pro_id',
            field=models.ForeignKey(to='security.Producto'),
        ),
    ]
