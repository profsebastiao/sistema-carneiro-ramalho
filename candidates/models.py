from django.db import models
from django.conf import settings
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

class CandidateProfile(models.Model):
    """Profile model for candidates"""
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='candidate_profile')
    full_name = models.CharField(max_length=100, verbose_name="Nome Completo")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    address = models.TextField(blank=True, verbose_name="Endereço")
    city = models.CharField(max_length=100, blank=True, verbose_name="Cidade")
    state = models.CharField(max_length=2, blank=True, verbose_name="Estado")
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn")
    github = models.URLField(blank=True, verbose_name="GitHub")
    portfolio = models.URLField(blank=True, verbose_name="Portfólio")
    resume = models.FileField(upload_to='resumes/', null=True, blank=True, verbose_name="Currículo (PDF)")
    summary = RichTextField(blank=True, verbose_name="Resumo Profissional")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.user.email}"
    
    class Meta:
        verbose_name = "Perfil do Candidato"
        verbose_name_plural = "Perfis dos Candidatos"


class Experience(models.Model):
    """Work experience model"""
    
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=100, verbose_name="Empresa")
    position = models.CharField(max_length=100, verbose_name="Cargo")
    start_date = models.DateField(verbose_name="Data de Início")
    end_date = models.DateField(null=True, blank=True, verbose_name="Data de Fim")
    is_current = models.BooleanField(default=False, verbose_name="Trabalho Atual")
    description = models.TextField(blank=True, verbose_name="Descrição")
    
    def __str__(self):
        return f"{self.position} at {self.company}"
    
    class Meta:
        verbose_name = "Experiência Profissional"
        verbose_name_plural = "Experiências Profissionais"
        ordering = ['-start_date']


class Education(models.Model):
    """Education model"""
    
    DEGREE_CHOICES = (
        ('tecnico', 'Técnico'),
        ('superior', 'Superior'),
        ('pos', 'Pós-graduação'),
        ('mestrado', 'Mestrado'),
        ('doutorado', 'Doutorado'),
    )
    
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=200, verbose_name="Instituição")
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES, verbose_name="Nível")
    field_of_study = models.CharField(max_length=100, verbose_name="Área de Estudo")
    start_date = models.DateField(verbose_name="Data de Início")
    end_date = models.DateField(null=True, blank=True, verbose_name="Data de Fim")
    is_current = models.BooleanField(default=False, verbose_name="Estudando Atualmente")
    
    def __str__(self):
        return f"{self.degree} in {self.field_of_study} - {self.institution}"
    
    class Meta:
        verbose_name = "Formação Acadêmica"
        verbose_name_plural = "Formações Acadêmicas"
        ordering = ['-start_date']


class Skill(models.Model):
    """Skills model"""
    
    PROFICIENCY_LEVELS = (
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
        ('expert', 'Expert'),
    )
    
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100, verbose_name="Habilidade")
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS, verbose_name="Nível")
    
    def __str__(self):
        return f"{self.name} ({self.get_proficiency_display()})"
    
    class Meta:
        verbose_name = "Habilidade"
        verbose_name_plural = "Habilidades"
        unique_together = ['candidate', 'name']
