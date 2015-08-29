from django.conf.urls import include, url
from django.contrib import admin
from apps.Usuarios.views import *
from apps.Clientes.views import *
from apps.Proveedores.views import *
from apps.Productos.views import *
from apps.Pedidos.views import *
from apps.Factura.views import *

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$','django.contrib.auth.views.login',{'template_name': 'login.html'},name='login'),
    url(r'^cerrar/$','django.contrib.auth.views.logout_then_login',name='logout'),
    url(r'^index/$','apps.security.views.index_view',name='index'),

#Usuarios
    url(r'^usuario/nuevoUsuario/$',newUser_view.as_view(),name='new_usuario'),
    url(r'^usuario/Administrar/',listUser_view,name="list_usuario"),
    url(r'^usuario/editarUsuario/(?P<pk>\d+)/$',editUser_view.as_view(),name='edit_usuario'),
    url(r'^usuario/borrar/(?P<pk>.*)/$', delUser_view, name='delete_usuario'),
    url(r'^usuario/generar_pdf/$', generar_pdf_Usuario, name='pdf_usuario'),


#Clientes
    url(r'^cliente/nuevoCliente/$',newClient_view.as_view(),name='new_cliente'),
    url(r'^cliente/Administrar/',listClient_view,name="list_cliente"),
    url(r'^cliente/editarCliente/(?P<pk>\d+)/$',editClient_view.as_view(),name='edit_cliente'),
    url(r'^cliente/generar_pdf/$', generar_pdf_Cliente, name='pdf_cliente'),


#Proveedores
    url(r'^proveedor/nuevoProveedor/$',newProvider_view.as_view(),name='new_proveedor'),
    url(r'^proveedor/Administrar/',listProvider_view,name="list_proveedor"),
    url(r'^proveedor/editarProveedor/(?P<pk>\d+)/$',editProvider_view.as_view(),name='edit_proveedor'),
    url(r'^proveedor/generar_pdf/$', generar_pdf_Proveedor, name='pdf_proveedor'),


#Productos
    url(r'^producto/nuevoProducto/$',newProduct_view.as_view(),name='new_producto'),
    url(r'^producto/Administrar/',listProduct_view,name="list_producto"),
    url(r'^producto/editarProducto/(?P<pk>\d+)/$',editProduct_view.as_view(),name='edit_producto'),
    url(r'^producto/Administrar/New/',listProductNew_view,name='list_producto_new'),
    url(r'^producto/generar_pdf/$', generar_pdf_Producto, name='pdf_producto'),


#Pedido
    url(r'^pedido/nuevoPedido/$',newOrder_view,name='new_pedido'),
    url(r'^pedido/Administrar/',listOrder_view,name='list_pedido'),
    url(r'^pedido/nuevoPedido/productos/$',listOrderProduct_view.as_view()),
    url(r'^pedido/generar_pdf/$', generar_pdf_Pedido, name='pdf_pedido'),
    url(r'^pedido/FiltrarProductos/$',obtenerProductos, name="filter_productos"),



#Factura
    url(r'^factura/nuevaFactura/$',newBill_view,name='new_factura'),
    url(r'^factura/Administrar/',listBill_view,name='list_factura'),
    url(r'^factura/generar_pdf/$', generar_pdf_Factura, name='pdf_factura'),

]
