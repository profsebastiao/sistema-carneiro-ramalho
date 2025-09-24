from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CandidateRegistrationForm, CompanyRegistrationForm

class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        user = self.request.user
        if user.user_type == 'candidate':
            return reverse_lazy('candidates:dashboard')
        elif user.user_type == 'company':
            return reverse_lazy('companies:dashboard')
        else:  # admin
            return reverse_lazy('wagtailadmin_home')
    
    def form_invalid(self, form):
        messages.error(self.request, "Usuário ou senha inválidos.")
        return super().form_invalid(form)

def register_choice(request):
    """View to choose registration type"""
    return render(request, 'accounts/register_choice.html')

def register_candidate(request):
    """Candidate registration view"""
    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 
                'Cadastro realizado com sucesso! Sua conta está sendo revisada por nossos administradores. '
                'Você receberá um e-mail quando sua conta for aprovada.'
            )
            return redirect('accounts:login')
        else:
            messages.error(request, 'Erro no cadastro. Verifique os dados informados.')
    else:
        form = CandidateRegistrationForm()
    
    return render(request, 'accounts/register_candidate.html', {'form': form})

def register_company(request):
    """Company registration view"""
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 
                'Cadastro da empresa realizado com sucesso! Sua conta está sendo revisada por nossos administradores. '
                'Você receberá um e-mail quando sua conta for aprovada.'
            )
            return redirect('accounts:login')
        else:
            messages.error(request, 'Erro no cadastro. Verifique os dados informados.')
    else:
        form = CompanyRegistrationForm()
    
    return render(request, 'accounts/register_company.html', {'form': form})
