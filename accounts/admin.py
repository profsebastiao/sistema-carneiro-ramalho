from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_approved', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_approved', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('user_type', 'phone', 'is_approved')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('user_type', 'phone', 'is_approved')
        }),
    )
