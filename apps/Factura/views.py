from django.shortcuts import render,HttpResponseRedirect, render_to_response, RequestContext
from django.db.models import Q, ProtectedError
from django.shortcuts import render_to_response, get_object_or_404, redirect, RequestContext
from apps.security.models import Factura, Cliente, Producto

from io import BytesIO

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table

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
    cntx={'listaClientes': Cliente.objects.all(),'listaProductos':Producto.objects.all(),}
    return render_to_response('addbill.html',cntx,context_instance=RequestContext(request)) 
