from django.contrib import admin
from .models import User, CadastraoCartao, LoteCartoes


class UserAdmin(admin.ModelAdmin):

    list_display = ['id', 'username', 'email']
    search_fields = ['nome', 'email']
    list_filter = ['created_at']


class CadastrarCartaoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'lote']


class LoteCartoesAdmin(admin.ModelAdmin):
    list_display = ['numero', 'nome', 'data', 'quantidade', 'usuario']


admin.site.register(User, UserAdmin)
admin.site.register(CadastraoCartao, CadastrarCartaoAdmin)
admin.site.register(LoteCartoes, LoteCartoesAdmin)
