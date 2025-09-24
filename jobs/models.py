from django.db import models
from django.conf import settings
from wagtail.fields import RichTextField
from companies.models import CompanyProfile
from candidates.models import CandidateProfile

class Job(models.Model):
    """Job posting model"""
    
    JOB_TYPE_CHOICES = (
        ('clt', 'CLT'),
        ('pj', 'PJ'),
        ('estagio', 'Estágio'),
        ('freelancer', 'Freelancer'),
        ('temporario', 'Temporário'),
    )
    
    EXPERIENCE_LEVEL_CHOICES = (
        ('junior', 'Júnior'),
        ('pleno', 'Pleno'),
        ('senior', 'Sênior'),
        ('especialista', 'Especialista'),
        ('diretor', 'Diretor'),
    )
    
    WORK_MODEL_CHOICES = (
        ('presencial', 'Presencial'),
        ('remoto', 'Remoto'),
        ('hibrido', 'Híbrido'),
    )
    
    STATUS_CHOICES = (
        ('draft', 'Rascunho'),
        ('pending', 'Pendente de Aprovação'),
        ('active', 'Ativa'),
        ('paused', 'Pausada'),
        ('closed', 'Fechada'),
        ('rejected', 'Rejeitada'),
    )
    
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200, verbose_name="Título da Vaga")
    description = RichTextField(verbose_name="Descrição da Vaga")
    requirements = RichTextField(verbose_name="Requisitos")
    benefits = RichTextField(blank=True, verbose_name="Benefícios")
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, verbose_name="Tipo de Contrato")
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, verbose_name="Nível de Experiência")
    work_model = models.CharField(max_length=20, choices=WORK_MODEL_CHOICES, verbose_name="Modelo de Trabalho")
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Salário Mínimo")
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Salário Máximo")
    location = models.CharField(max_length=200, blank=True, verbose_name="Localização")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=2, verbose_name="Estado")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Data de Expiração")
    
    # Fields for admin approval
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='approved_jobs',
        verbose_name="Aprovado por"
    )
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name="Data de Aprovação")
    rejection_reason = models.TextField(blank=True, verbose_name="Motivo da Rejeição")
    
    def __str__(self):
        return f"{self.title} - {self.company.company_name}"
    
    class Meta:
        verbose_name = "Vaga"
        verbose_name_plural = "Vagas"
        ordering = ['-created_at']


class JobApplication(models.Model):
    """Job application model"""
    
    STATUS_CHOICES = (
        ('applied', 'Candidatou-se'),
        ('under_review', 'Em Análise'),
        ('interview_scheduled', 'Entrevista Agendada'),
        ('interview_completed', 'Entrevista Realizada'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
        ('hired', 'Contratado'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied', verbose_name="Status")
    cover_letter = models.TextField(blank=True, verbose_name="Carta de Apresentação")
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name="Data da Candidatura")
    updated_at = models.DateTimeField(auto_now=True)
    
    # Interview information
    interview_date = models.DateTimeField(null=True, blank=True, verbose_name="Data da Entrevista")
    interview_notes = models.TextField(blank=True, verbose_name="Notas da Entrevista")
    
    # Company feedback
    feedback = models.TextField(blank=True, verbose_name="Feedback da Empresa")
    feedback_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.candidate.full_name} -> {self.job.title}"
    
    class Meta:
        verbose_name = "Candidatura"
        verbose_name_plural = "Candidaturas"
        unique_together = ['job', 'candidate']
        ordering = ['-applied_at']


class JobSkill(models.Model):
    """Required skills for a job"""
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='required_skills')
    skill_name = models.CharField(max_length=100, verbose_name="Habilidade")
    is_required = models.BooleanField(default=True, verbose_name="Obrigatória")
    
    def __str__(self):
        return f"{self.skill_name} ({'Obrigatória' if self.is_required else 'Desejável'})"
    
    class Meta:
        verbose_name = "Habilidade da Vaga"
        verbose_name_plural = "Habilidades da Vaga"
        unique_together = ['job', 'skill_name']
