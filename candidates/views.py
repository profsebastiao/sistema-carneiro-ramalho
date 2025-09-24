from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from jobs.models import Job, JobApplication
from .models import CandidateProfile

@login_required
def dashboard(request):
    """Candidate dashboard view"""
    if request.user.user_type != 'candidate':
        messages.error(request, 'Acesso negado. Esta área é restrita para candidatos.')
        return redirect('/')
    
    if not request.user.is_approved:
        messages.warning(request, 'Sua conta ainda não foi aprovada pelos administradores.')
        return render(request, 'candidates/pending_approval.html')
    
    # Get candidate profile
    try:
        profile = request.user.candidate_profile
    except CandidateProfile.DoesNotExist:
        messages.error(request, 'Perfil de candidato não encontrado.')
        return redirect('/')
    
    # Get recent job applications
    applications = JobApplication.objects.filter(candidate=profile).order_by('-applied_at')[:10]
    
    # Get recent active jobs (for job search)
    recent_jobs = Job.objects.filter(status='active').order_by('-created_at')[:5]
    
    context = {
        'profile': profile,
        'applications': applications,
        'recent_jobs': recent_jobs,
        'applications_count': applications.count(),
    }
    
    return render(request, 'candidates/dashboard.html', context)

@login_required 
def job_search(request):
    """Job search view for candidates"""
    if request.user.user_type != 'candidate' or not request.user.is_approved:
        messages.error(request, 'Acesso negado.')
        return redirect('/')
    
    jobs = Job.objects.filter(status='active')
    
    # Search filters
    search_query = request.GET.get('q', '')
    job_type = request.GET.get('job_type', '')
    work_model = request.GET.get('work_model', '')
    city = request.GET.get('city', '')
    
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(company__company_name__icontains=search_query)
        )
    
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    if work_model:
        jobs = jobs.filter(work_model=work_model)
    
    if city:
        jobs = jobs.filter(city__icontains=city)
    
    jobs = jobs.order_by('-created_at')
    
    context = {
        'jobs': jobs,
        'search_query': search_query,
        'job_type': job_type,
        'work_model': work_model,
        'city': city,
        'job_type_choices': Job.JOB_TYPE_CHOICES,
        'work_model_choices': Job.WORK_MODEL_CHOICES,
    }
    
    return render(request, 'candidates/job_search.html', context)
