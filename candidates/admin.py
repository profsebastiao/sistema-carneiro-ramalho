from django.contrib import admin
from .models import CandidateProfile, Experience, Education, Skill

class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0

class EducationInline(admin.TabularInline):
    model = Education
    extra = 0

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0

@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'city', 'state', 'created_at')
    list_filter = ('created_at', 'state')
    search_fields = ('full_name', 'user__email', 'city')
    inlines = [ExperienceInline, EducationInline, SkillInline]
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('user', 'full_name', 'birth_date')
        }),
        ('Localização', {
            'fields': ('address', 'city', 'state')
        }),
        ('Links Profissionais', {
            'fields': ('linkedin', 'github', 'portfolio')
        }),
        ('Currículo', {
            'fields': ('resume', 'summary')
        }),
    )

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'position', 'company', 'start_date', 'is_current')
    list_filter = ('is_current', 'start_date')
    search_fields = ('candidate__full_name', 'company', 'position')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'degree', 'field_of_study', 'institution', 'start_date')
    list_filter = ('degree', 'is_current')
    search_fields = ('candidate__full_name', 'institution', 'field_of_study')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'name', 'proficiency')
    list_filter = ('proficiency',)
    search_fields = ('candidate__full_name', 'name')
