from django.db import models
from django.conf import settings
from wagtail.fields import RichTextField

class CompanyProfile(models.Model):
    """Profile model for companies"""
    
    COMPANY_SIZE_CHOICES = (
        ('micro', 'Microempresa (1-9 funcionários)'),
        ('pequena', 'Pequena empresa (10-49 funcionários)'),
        ('media', 'Média empresa (50-249 funcionários)'),
        ('grande', 'Grande empresa (250+ funcionários)'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=200, verbose_name="Nome da Empresa")
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    description = RichTextField(blank=True, verbose_name="Descrição da Empresa")
    website = models.URLField(blank=True, verbose_name="Website")
    address = models.TextField(blank=True, verbose_name="Endereço")
    city = models.CharField(max_length=100, blank=True, verbose_name="Cidade")
    state = models.CharField(max_length=2, blank=True, verbose_name="Estado")
    company_size = models.CharField(max_length=20, choices=COMPANY_SIZE_CHOICES, verbose_name="Porte da Empresa")
    industry = models.CharField(max_length=100, blank=True, verbose_name="Setor")
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True, verbose_name="Logo")
    contact_person = models.CharField(max_length=100, verbose_name="Pessoa de Contato")
    contact_position = models.CharField(max_length=100, blank=True, verbose_name="Cargo do Contato")
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn da Empresa")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name = "Perfil da Empresa"
        verbose_name_plural = "Perfis das Empresas"
