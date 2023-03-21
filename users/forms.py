from django.forms import ModelForm
from .models import Loan, Branch
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class LoanForm(ModelForm):
    class Meta:
        model = Loan
        fields = ['idBranch', 'quantity']
        
        
class BranchForm(ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'city', 'assets', 'region']
        

class Client(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2')