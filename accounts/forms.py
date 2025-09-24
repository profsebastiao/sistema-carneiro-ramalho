from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import CustomUser
from candidates.models import CandidateProfile
from companies.models import CompanyProfile

class CandidateRegistrationForm(UserCreationForm):
    """Registration form for candidates"""
    
    full_name = forms.CharField(max_length=100, label="Nome Completo")
    email = forms.EmailField(label="E-mail")
    phone = forms.CharField(max_length=20, required=False, label="Telefone")
    
    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'phone', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6'),
                Column('full_name', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6'),
                Column('phone', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6'),
                Column('password2', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Submit('submit', 'Cadastrar como Candidato', css_class='btn btn-primary btn-block')
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.user_type = 'candidate'
        user.is_approved = False  # Needs admin approval
        
        if commit:
            user.save()
            # Create candidate profile
            CandidateProfile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name']
            )
        return user


class CompanyRegistrationForm(UserCreationForm):
    """Registration form for companies"""
    
    company_name = forms.CharField(max_length=200, label="Nome da Empresa")
    cnpj = forms.CharField(max_length=18, label="CNPJ")
    email = forms.EmailField(label="E-mail da Empresa")
    phone = forms.CharField(max_length=20, required=False, label="Telefone")
    contact_person = forms.CharField(max_length=100, label="Pessoa de Contato")
    
    class Meta:
        model = CustomUser
        fields = ('username', 'company_name', 'cnpj', 'email', 'phone', 'contact_person', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6'),
                Column('company_name', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('cnpj', css_class='form-group col-md-6'),
                Column('contact_person', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6'),
                Column('phone', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6'),
                Column('password2', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Submit('submit', 'Cadastrar Empresa', css_class='btn btn-success btn-block')
        )
    
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if CustomUser.objects.filter(company_profile__cnpj=cnpj).exists():
            raise forms.ValidationError("Já existe uma empresa cadastrada com este CNPJ.")
        return cnpj
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.user_type = 'company'
        user.is_approved = False  # Needs admin approval
        
        if commit:
            user.save()
            # Create company profile
            CompanyProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                cnpj=self.cleaned_data['cnpj'],
                contact_person=self.cleaned_data['contact_person']
            )
        return user