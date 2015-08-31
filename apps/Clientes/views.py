from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q, ProtectedError
from django.shortcuts import render_to_response, get_object_or_404, redirect, RequestContext
from apps.security.models import Cliente

from io import BytesIO

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def listClient_view(request):
    if request.method == 'POST':
        results=Cliente.objects.filter(cli_ced__contains=request.POST["buscar"]).values()
        return render_to_response('listclient.html',{'results':results},context_instance=RequestContext(request))   
    results=Cliente.objects.all().order_by('cli_nom')
    return render_to_response('listclient.html',{'results':results},context_instance=RequestContext(request))

@login_required(login_url='/')
def delClient_view(request,pk):
    obj = get_object_or_404(Cliente, pk=pk)
    obj.cli_est=False
    obj.save()
    return redirect("/cliente/Administrar/")

@login_required(login_url='/')
def generar_pdf_Cliente(request):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "clientes.pdf" 
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    clientes = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Clientes", styles['Heading1'])
    clientes.append(header)
    headings = ('Cedula', 'Nombres', 'Apellidos', 'Direccion','Telefono')
    allclientes = [(p.cli_ced, p.cli_nom, p.cli_ape, p.cli_dir, p.cli_tel) for p in Cliente.objects.filter(cli_est=True).order_by('cli_nom')]

    t = Table([headings] + allclientes)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (5, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    
    clientes.append(t)
    doc.build(clientes)
    response.write(buff.getvalue())
    buff.close()
    return response

class newClient_view(CreateView):
    model = Cliente
    fields = ('cli_ced','cli_nom','cli_ape','cli_dir','cli_tel')
    template_name = 'addclient.html'
    success_url = '/cliente/Administrar/'

class editClient_view(UpdateView):
    model = Cliente
    fields = ('cli_ced','cli_nom','cli_ape','cli_dir','cli_tel')
    template_name = 'editclient.html'
    success_url = '/cliente/Administrar/'
