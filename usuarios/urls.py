from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
app_name = 'usuarios'

urlpatterns = [
    path('register/',views.register, name="register"),
    path('login/', views.login, name='login'),
    path('logout/',views.exit,name='exit'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path("register/", views.register, name="register"),
    path("perfil/", views.perfil, name="perfil"),
    #Reestablecer contrasena
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'), 
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'), 
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'), 
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]