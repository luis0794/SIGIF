from django.shortcuts import render,HttpResponseRedirect, render_to_response, RequestContext
from django.db.models import Q, ProtectedError
from django.shortcuts import render_to_response, get_object_or_404, redirect, RequestContext
from apps.security.models import Pedido, Proveedor, Producto
from django.views.generic import TemplateView, FormView, CreateView, UpdateView
from django.http import request, HttpResponse, HttpResponseRedirect, Http404
import json

from io import BytesIO

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from .forms import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def generar_pdf_Pedido(request):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "pedidos.pdf"
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    pedidos = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Pedidos", styles['Heading1'])
    pedidos.append(header)
    headings = ('Numero de Pedido', 'Proovedor', 'Usuario')
    allpedidos = [(p.ped_num, p.prov_id, p.usu_id) for p in Pedido.objects.order_by('ped_num')]

    t = Table([headings] + allpedidos)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (5, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))

    pedidos.append(t)
    doc.build(pedidos)
    response.write(buff.getvalue())
    buff.close()
    return response

@login_required(login_url='/')
def obtenerProductos(request):
    prov = request.GET['id_proveedor']
    productos=Producto.objects.filter(prov_id=prov)

    pro=[]
    for producto in productos:
        res={}
        res['id']=producto.id
        res['nombre']=producto.pro_nom
        res['marca']=producto.pro_mar
        res['precio']=producto.pro_pre
        res['stock_actual']=producto.pro_sto_act
        pro.append(res)

    data = json.dumps(pro)
    return HttpResponse(data, content_type='application/json')



@login_required(login_url='/')
def listOrder_view(request):
    if request.method == 'POST':
        results=Pedido.objects.filter(ped_num__contains=request.POST["buscar"]).values()
        return render_to_response('listorder.html',{'results':results},context_instance=RequestContext(request))
    results=Pedido.objects.all().order_by('ped_num')
    return render_to_response('listorder.html',{'results':results},context_instance=RequestContext(request))

@login_required(login_url='/')
def newOrder_view(request):
    form = PedidosForm(request.POST or None)
    id=Pedido.objects.all().count()
    id_ped=id+1
    if form.is_valid():
        form.save()
        return redirect("list_pedido")

    cntx={'listaProveedores': Proveedor.objects.filter(est_proveedor=True),'listaPedidos': Pedido.objects.count(),
          'listaProductos':Producto.objects.all().order_by('pro_nom'),'form':form, 'id_ped':id_ped}
    return render(request,'addorder.html',cntx)

class listOrderProduct_view(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            ped_id = request.GET['id']
            listaproductos = Producto.objects.filter(prov_id=ped_id).order_by('prov_nom')
            print listaproductos

            datosTabla = []
            sub = 0

            for producto in listaproductos:
                resul = {}
                resul['id']=producto.id
                resul['nombre']=producto.pro_nom
                resul['marca']=producto.pro_nom
                resul['precio']=producto.pro_pre
                resul['stock']=producto.pro_sto

                datosTabla.append(resul)

            data = json.dumps(datosTabla)

            return HttpResponse(data, content_type='application/json')
        else:
            return Http404

@login_required(login_url='/')
def imprimirOrder(request,id):
    ped=Pedido.objects.get(pk=id)
    prov_id_=ped.id
    prov=Proveedor.objects.get(pk=prov_id_)
    listaped = []
    detalle=Detalle_Pedido.objects.filter(ped_id=id)
    produc=Producto.objects.all()
    cedula = ped.usu_id
    print cedula

    return render_to_response('imprimirOrder.html',{'prov':prov,'ped':ped,'detalle':detalle,'listaped':listaped},context_instance=RequestContext(request))