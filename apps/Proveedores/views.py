from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q, ProtectedError
from django.shortcuts import render_to_response, get_object_or_404, redirect, RequestContext
from apps.security.models import Proveedor

from io import BytesIO

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def listProvider_view(request):
    if request.method == 'POST':
        results=Proveedor.objects.filter(prov_nom__contains=request.POST["buscar"]).values()
        return render_to_response('listprovider.html',{'results':results},context_instance=RequestContext(request))   
    results=Proveedor.objects.all().order_by('prov_nom')
    return render_to_response('listprovider.html',{'results':results},context_instance=RequestContext(request))

@login_required(login_url='/')
def delProvider_view(request,pk):
    obj = get_object_or_404(Proveedor, pk=pk)
    obj.cli_est=False
    obj.save()
    return redirect("/proveedor/Administrar/")

@login_required(login_url='/')
def generar_pdf_Proveedor(request):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "proveedores.pdf" 
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    proveedores = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Proveedores", styles['Heading1'])
    proveedores.append(header)
    headings = ('Nombre', 'Nombre_Contacto', 'Cargo_Contacto', 'Ciudad','Direccion', 'Email')
    allproveedores = [(p.prov_nom, p.prov_nom_con, p.prov_car_con, p.prov_ciu, p.prov_dir, p.prov_ema) for p in Proveedor.objects.filter(est_proveedor=True).order_by('prov_nom')]

    t = Table([headings] + allproveedores)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (6, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    
    proveedores.append(t)
    doc.build(proveedores)
    response.write(buff.getvalue())
    buff.close()
    return response

class newProvider_view(CreateView):
    model = Proveedor
    fields = ('prov_nom','prov_nom_con','prov_car_con','prov_ciu','prov_dir','prov_ema')
    template_name = 'addprovider.html'
    success_url = '/proveedor/Administrar/'

class editProvider_view(UpdateView):
    model = Proveedor
    fields = ('prov_nom','prov_nom_con','prov_car_con','prov_ciu','prov_dir','prov_ema','est_proveedor')
    template_name = 'editprovider.html'
    success_url = '/proveedor/Administrar/'
