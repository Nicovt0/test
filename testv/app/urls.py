from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    
    #prov
    path('proveedor/', views.proveedor, name='proveedor'),
    path('proveedor/orden/<str:codigo>/', views.detalleorden, name='detalleorden'),
    
    #admin
    path('admin2/', views.admin2, name='admin2'),
    path('detalleproveedor/<int:id_proveedor>/', views.detalleproveedor, name='detalleproveedor'),
    path('detalleproducto/<int:id_producto>/', views.detalleproducto, name='detalleproducto'),
    path('prod_crear/<int:id_proveedor>/', views.prod_crear, name='prod_crear'),
    path('prod_editar/<int:id_producto>/', views.prod_editar, name='prod_editar'),
    path('prod_eliminar/<int:id_producto>/', views.prod_eliminar, name='prod_eliminar'),
    path('', views.login, name='login'),  # Default route to login view

    path('proveedor_crear/', views.proveedor_crear, name='proveedor_crear'),
]