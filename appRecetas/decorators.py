# recetas/decorators.py

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

def check_user_blocked(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'perfil') and request.user.perfil.is_blocked:
            messages.error(request, "Tu cuenta está bloqueada. No puedes acceder a esta página.")
            return HttpResponseRedirect(reverse('recetas:home'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view
