# estoque/decorators.py
from django.http import HttpResponse

def gerente_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.usu_tipo != 'gerente':
            return HttpResponse("Acesso negado.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
