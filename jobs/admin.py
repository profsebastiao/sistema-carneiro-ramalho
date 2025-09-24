from django.contrib import admin
from .models import Job, JobApplication, JobSkill

class JobSkillInline(admin.TabularInline):
    model = JobSkill
    extra = 0

class JobApplicationInline(admin.TabularInline):
    model = JobApplication
    extra = 0
    readonly_fields = ('applied_at',)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'status', 'job_type', 'work_model', 'created_at')
    list_filter = ('status', 'job_type', 'work_model', 'experience_level', 'created_at')
    search_fields = ('title', 'company__company_name', 'city', 'state')
    inlines = [JobSkillInline, JobApplicationInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('company', 'title', 'status')
        }),
        ('Descrição', {
            'fields': ('description', 'requirements', 'benefits')
        }),
        ('Detalhes da Vaga', {
            'fields': ('job_type', 'experience_level', 'work_model')
        }),
        ('Localização e Salário', {
            'fields': ('city', 'state', 'location', 'salary_min', 'salary_max')
        }),
        ('Datas', {
            'fields': ('expires_at',)
        }),
        ('Aprovação', {
            'fields': ('approved_by', 'approved_at', 'rejection_reason'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('approved_at',)

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'status', 'applied_at', 'updated_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('candidate__full_name', 'job__title', 'job__company__company_name')
    
    fieldsets = (
        ('Candidatura', {
            'fields': ('job', 'candidate', 'status', 'cover_letter')
        }),
        ('Entrevista', {
            'fields': ('interview_date', 'interview_notes'),
            'classes': ('collapse',)
        }),
        ('Feedback', {
            'fields': ('feedback', 'feedback_date'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('applied_at',)

@admin.register(JobSkill)
class JobSkillAdmin(admin.ModelAdmin):
    list_display = ('job', 'skill_name', 'is_required')
    list_filter = ('is_required',)
    search_fields = ('job__title', 'skill_name')
