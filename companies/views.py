from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from jobs.models import Job, JobApplication
from .models import CompanyProfile

@login_required
def dashboard(request):
    """Company dashboard view"""
    if request.user.user_type != 'company':
        messages.error(request, 'Acesso negado. Esta área é restrita para empresas.')
        return redirect('/')
    
    if not request.user.is_approved:
        messages.warning(request, 'Sua conta ainda não foi aprovada pelos administradores.')
        return render(request, 'companies/pending_approval.html')
    
    # Get company profile
    try:
        profile = request.user.company_profile
    except CompanyProfile.DoesNotExist:
        messages.error(request, 'Perfil de empresa não encontrado.')
        return redirect('/')
    
    # Get company statistics
    jobs = Job.objects.filter(company=profile)
    active_jobs = jobs.filter(status='active')
    applications = JobApplication.objects.filter(job__company=profile)
    
    # Recent applications
    recent_applications = applications.order_by('-applied_at')[:10]
    
    # Applications by status
    applications_by_status = applications.values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    context = {
        'profile': profile,
        'total_jobs': jobs.count(),
        'active_jobs_count': active_jobs.count(),
        'total_applications': applications.count(),
        'recent_applications': recent_applications,
        'applications_by_status': applications_by_status,
        'recent_jobs': jobs.order_by('-created_at')[:5],
    }
    
    return render(request, 'companies/dashboard.html', context)

@login_required
def pipeline(request):
    """Candidate pipeline view for companies"""
    if request.user.user_type != 'company' or not request.user.is_approved:
        messages.error(request, 'Acesso negado.')
        return redirect('/')
    
    try:
        profile = request.user.company_profile
    except CompanyProfile.DoesNotExist:
        messages.error(request, 'Perfil de empresa não encontrado.')
        return redirect('/')
    
    # Get applications grouped by status
    applications = JobApplication.objects.filter(job__company=profile).select_related(
        'candidate', 'job'
    )
    
    # Group applications by status
    pipeline_stages = {}
    for status_code, status_name in JobApplication.STATUS_CHOICES:
        pipeline_stages[status_code] = {
            'name': status_name,
            'applications': applications.filter(status=status_code).order_by('-applied_at')
        }
    
    context = {
        'profile': profile,
        'pipeline_stages': pipeline_stages,
    }
    
    return render(request, 'companies/pipeline.html', context)
