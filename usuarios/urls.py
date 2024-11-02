from django.urls import path, include
from . import views
app_name = 'usuarios'

urlpatterns = [
    path('register/',views.register, name="register"),
    path('login/', views.login, name='login'),
    path('logout/',views.exit,name='exit'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path("register/", views.register, name="register"),
    path("perfil/", views.perfil, name="perfil"),
]