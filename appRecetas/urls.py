from django.urls import path, include
from . import views


app_name = 'recetas'


urlpatterns = [
    path("", views.home, name="home"),
    path("recetas/", views.recetas, name="recetas"),
    path("receta/<int:receta_id>/", views.receta_detalle, name="receta_detalle"),   
    path("agregar-recetas/", views.agregar_receta, name="agregar_recetas"),
    path("listar-recetas/", views.listar_recetas, name="listar_recetas"),
    path("modificar-receta/<id>/", views.modificar_receta, name="modificar_receta"),
    path("eliminar-receta/<id>/", views.eliminar_receta, name="eliminar_receta"),
    path('gestionar-usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),
    path('bloquear-usuario/<int:usuario_id>/', views.bloquear_usuario, name='bloquear_usuario'),
    path('like/<int:post_id>/', views.like, name='like_post'),
    path('post/<int:post_id>/favorito/', views.toggle_favorite, name='toggle_favorite'),
    path('favoritos/', views.favorite_posts, name='favorite_posts'),
    path("busqueda", views.busqueda_funcional, name="busqueda_funcional"),
    path('contacto/', views.contacto, name='contacto'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    
]
