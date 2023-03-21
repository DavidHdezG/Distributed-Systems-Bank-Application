from django.forms import ModelForm
from .models import Loan, Branch
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class LoanForm(ModelForm):
    idBranch = forms.ModelChoiceField(queryset=Branch.objects.all(), label="Seleccione Sucursal",widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.FloatField(label="Cantidad",widget=forms.NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Loan
        fields = ['idBranch', 'quantity']
        
        widgets= {
            'idBranch': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        
class BranchForm(ModelForm):
    name= forms.CharField(label="Nombre",widget=forms.TextInput(attrs={'class': 'form-control'}))
    city= forms.CharField(label="Ciudad",widget=forms.TextInput(attrs={'class': 'form-control'}))
    assets= forms.FloatField(label="Activos",widget=forms.NumberInput(attrs={'class': 'form-control'}))
    region= forms.CharField(label="Region",widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Branch
        fields = ['name', 'city', 'assets', 'region']
        

class Client(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Requerido.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Requerido.')
    email = forms.EmailField(max_length=254, required=True, help_text='Requerido. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }