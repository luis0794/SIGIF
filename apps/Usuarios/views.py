from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q, ProtectedError
from django.shortcuts import render_to_response, get_object_or_404, redirect, RequestContext
from apps.security.models import Usuario
from .forms import UserForm
from django.views.generic import FormView, ListView

from io import BytesIO

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table

def listUser_view(request):
    if request.method == 'POST':
        results=Usuario.object.filter(usu_ced__contains=request.POST["buscar"]).values()
        return render_to_response('listuser.html',{'results':results},context_instance=RequestContext(request))   
    results=Usuario.object.all().order_by('usu_nom')
    return render_to_response('listuser.html',{'results':results},context_instance=RequestContext(request))


def delUser_view(request,pk):
    obj = get_object_or_404(Usuario, pk=pk)
    obj.usu_est=False
    obj.save()
    return redirect("/usuario/Administrar/")

class newUser_view(FormView):
    form_class = UserForm
    template_name = 'adduser.html'
    success_url = '/usuario/Administrar/'

    def form_valid(self,form):
        form.save()
        return super(newUser_view,self).form_valid(form)

class editUser_view(UpdateView):
    model = Usuario
    fields = ('usu_ced','usu_nom','usu_ape','usu_sex','usu_dir','usu_tel','usu_ema')
    template_name = 'edituser.html'
    success_url = '/usuario/Administrar/'


def generar_pdf_Usuario(request):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "usuarios.pdf" 
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    usuarios = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Usuarios", styles['Heading1'])
    usuarios.append(header)
    headings = ('Cedula', 'Nombres', 'Apellidos', 'Sexo','Direccion', 'Telefono', 'Email')
    allusuarios = [(p.usu_ced, p.usu_nom, p.usu_ape, p.usu_sex, p.usu_dir, p.usu_tel, p.usu_ema) for p in Usuario.object.all()]

    t = Table([headings] + allusuarios)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (6, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    
    usuarios.append(t)
    doc.build(usuarios)
    response.write(buff.getvalue())
    buff.close()
    return response
