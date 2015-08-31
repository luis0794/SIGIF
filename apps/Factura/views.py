from django.shortcuts import render,HttpResponseRedirect, render_to_response, RequestContext
from django.db.models import Q, ProtectedError
from django.shortcuts import render_to_response, get_object_or_404, redirect, RequestContext
from apps.security.models import Factura, Cliente, Producto, Detalle_Factura

from io import BytesIO

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
import datetime 
import json
from .forms import *

def guardarFactura(request):
    nomProd= ""
    producto= Producto.objects.filter(pro_nom=request.GET["nomPro"])
    for i in producto:
        nomProd=i.id
        
    bill=Factura(can_det_fac=request.GET["cantidad"],
           pre_uni_det_fac=request.GET["PreUni"],
           pre_tot_det_fac=request.GET["PreTot"],
           fac_id_id=request.GET["idFac"],
           pro_id_id=nomProd,
           )
    bill.save()
    nomProd=bill.id
    data = json.dumps(nomProd)

    return HttpResponse(data, content_type='application/json')

def guardarFacturaDetalle(request):
    print 'yes'
    cliente_id= ""
    cliente= Cliente.objects.filter(cli_ced=request.GET["cedCli"])
    for i in cliente:
        cliente_id=i.id
        
    bill=Detalle_Factura(fac_num=request.GET["numFac"],
           fac_fec=datetime.datetime.now(),
           fac_sub_tot=request.GET["subTot"],
           fac_iva=request.GET["iva"],
           fac_des="Emitida por: "+request.user.usu_nom,
           fac_tot=request.GET["txtTotal"],
           cli_id_id=cliente_id,
           )
    bill.save()
    print 'yes1'
    id_ped=bill.id
    data = json.dumps(id_ped)

    return HttpResponse(data, content_type='application/json')


def generar_pdf_Factura(request):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "facturas.pdf" 
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=18,
        )
    facturas = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Facturas", styles['Heading1'])
    facturas.append(header)
    headings = ('Numero de Factura', 'Cliente', 'Fecha', 'Total')
    allfacturas = [(p.fac_num, p.cli_id, p.fac_fec, p.fac_tot) for p in Factura.objects.order_by('fac_num')]

    t = Table([headings] + allfacturas)
    t.setStyle(TableStyle(
        [
        ('GRID', (0, 0), (5, -1), 1, colors.dodgerblue),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
        ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
        ))

    facturas.append(t)
    doc.build(facturas)
    response.write(buff.getvalue())
    buff.close()
    return response

def listBill_view(request):
    if request.method == 'POST':
        results=Factura.objects.filter(fac_num__contains=request.POST["buscar"]).values()
        return render_to_response('listbill.html',{'results':results},context_instance=RequestContext(request))   
    results=Factura.objects.all().order_by('fac_num')
    return render_to_response('listbill.html',{'results':results},context_instance=RequestContext(request))


def newBill_view(request):
    form = FacturaForm(request.POST or None)
    id=Factura.objects.all().count()
    id_fac=id+1
    if form.is_valid():
        form.save()
        return redirect("list_factura")

    cntx={'listaClientes': Cliente.objects.all(),'listaProductos':Producto.objects.all(),'id_fac':id_fac, 'form':form}

    return render(request,'addbill.html',cntx)
