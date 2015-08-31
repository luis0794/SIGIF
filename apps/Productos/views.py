from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q, ProtectedError
from django.shortcuts import render_to_response, get_object_or_404, redirect, RequestContext
from apps.security.models import Producto

from io import BytesIO

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def listProduct_view(request):
    if request.method == 'POST':
        results=Producto.objects.filter(pro_nom__contains=request.POST["buscar"]).values()
        return render_to_response('listproduct.html',{'results':results},context_instance=RequestContext(request))   
    results=Producto.objects.all().order_by('pro_nom')
    return render_to_response('listproduct.html',{'results':results},context_instance=RequestContext(request))

@login_required(login_url='/')
def listProductNew_view(request):
    pro=Producto.objects.all()
    return render_to_response('list_producto_new.html',{'pro':pro},context_instance=RequestContext(request))


@login_required(login_url='/')
def generar_pdf_Producto(request):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "productos.pdf" 
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    productos = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Productos", styles['Heading1'])
    productos.append(header)
    headings = ('Proveedor','Nombre', 'Descripcion', 'Marca', 'Precio','Stock Actual')
    allproductos = [(p.prov_id, p.pro_nom, p.pro_des, p.pro_mar, p.pro_pre, p.pro_sto_act) for p in Producto.objects.all()]

    t = Table([headings] + allproductos)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (6, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    
    productos.append(t)
    doc.build(productos)
    response.write(buff.getvalue())
    buff.close()
    return response

class newProduct_view(CreateView):
    model = Producto
    fields = ('prov_id','pro_nom','pro_pre','pro_mar','pro_des')
    template_name = 'addproduct.html'
    success_url = '/index/'


class editProduct_view(UpdateView):
    model = Producto
    fields = ('prov_id','pro_nom','pro_pre','pro_mar','pro_sto_act','pro_des')
    template_name = 'editproduct.html'
    success_url = '/producto/Administrar/'
