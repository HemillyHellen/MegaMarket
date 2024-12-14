from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUsuarioAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email', 'usu_tipo', 'usu_ger_id')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'usu_tipo', 'usu_ger_id'),
        }),
    )
    list_display = ('username', 'email', 'usu_tipo', 'is_active', 'is_staff')

admin.site.register(Usuario, CustomUsuarioAdmin)
admin.site.register(Fornecedor)
admin.site.register(Produto)
admin.site.register(Movimentacao)