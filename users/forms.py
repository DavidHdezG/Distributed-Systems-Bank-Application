from django.forms import ModelForm
from .models import Loan, Branch
class LoanForm(ModelForm):
    class Meta:
        model = Loan
        fields = ['idBranch', 'quantity']
        
        
class BranchForm(ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'city', 'assets', 'region']