from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("recetas/", views.recetas, name="recetas"),
    path("register/", views.register, name="register"),
    path("perfil/", views.perfil, name="perfil"),
    path("perfil/editar/", views.editar_perfil, name="editar_perfil"),
    path("receta/<int:receta_id>/", views.receta_detalle, name="receta_detalle"),
    path("agregar-recetas/", views.agregar_receta, name="agregar_recetas"),
    path("listar-recetas/", views.listar_recetas, name="listar_recetas"),
    path("modificar-receta/<id>/", views.modificar_receta, name="modificar_receta"),
    path("eliminar-receta/<id>/", views.eliminar_receta, name="eliminar_receta"),
    path("busqueda", views.busqueda_funcional, name="busqueda_funcional"),
]
