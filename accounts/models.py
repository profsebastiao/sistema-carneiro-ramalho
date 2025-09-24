from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Custom user model extending the default Django User"""
    
    USER_TYPES = (
        ('candidate', 'Candidato'),
        ('company', 'Empresa'),
        ('admin', 'Administrador'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='candidate')
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False, help_text="Aprovado pelo administrador")
    
    def __str__(self):
        return f"{self.username} - {self.get_user_type_display()}"
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
