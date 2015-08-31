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
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
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


@login_required(login_url='/')
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

@login_required(login_url='/')
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

@login_required(login_url='/')
def listBill_view(request):
    if request.method == 'POST':
        results=Factura.objects.filter(fac_num__contains=request.POST["buscar"]).values()
        return render_to_response('listbill.html',{'results':results},context_instance=RequestContext(request))   
    results=Factura.objects.all().order_by('fac_num')
    return render_to_response('listbill.html',{'results':results},context_instance=RequestContext(request))

def newBill_view(request):
    contador=0
    form = FacturaForm(request.POST or None)
    id=Factura.objects.all().count()
    id_fac=id+1
    producto = Producto.objects.all()
    if form.is_valid():
        form.save()
        id1=Factura.objects.all().count()
        print id1
        idF= get_object_or_404(Factura, id=id1)
        print idF
        contador = int(request.POST.get("contar"))
        print contador
        for i in range(contador):
            print "1"
            prd=get_object_or_404(Producto, id= request.POST.get("idpr1"))
            cant=request.POST.get("TxtCantidad"+str(i+1))
            det=request.POST.get("id_fac_des")
            print cant,det
            deta=Detalle_Factura(det_ped_can=cant,det_ped_des=det,ped_id=idF,pro_id=prd)
            deta.save()
        return redirect("list_factura")

    cntx={'listaClientes': Cliente.objects.all(),'listaProductos':Producto.objects.all(),'id_fac':id_fac, 'form':form}

    return render(request,'addbill.html',cntx)

@login_required(login_url='/')
def imprimirBill(request,id):
    fac=Factura.objects.get(pk=id)
    cli_id_=fac.cli_id_id
    cliente=Cliente.objects.get(pk=cli_id_)
    detalle=Detalle_Factura.objects.filter(fac_id=id)
    produc=Producto.objects.all()

    return render_to_response('imprimirBill.html',{'cliente':cliente,'fac':fac,'detalle':detalle},context_instance=RequestContext(request))
