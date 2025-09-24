from django.contrib import admin
from .models import CompanyProfile

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'city', 'state', 'company_size', 'created_at')
    list_filter = ('company_size', 'industry', 'state', 'created_at')
    search_fields = ('company_name', 'cnpj', 'user__email', 'city', 'industry')
    
    fieldsets = (
        ('Informações da Empresa', {
            'fields': ('user', 'company_name', 'cnpj', 'description')
        }),
        ('Localização', {
            'fields': ('address', 'city', 'state')
        }),
        ('Detalhes da Empresa', {
            'fields': ('company_size', 'industry', 'website', 'linkedin')
        }),
        ('Contato', {
            'fields': ('contact_person', 'contact_position')
        }),
        ('Logo', {
            'fields': ('logo',)
        }),
    )
