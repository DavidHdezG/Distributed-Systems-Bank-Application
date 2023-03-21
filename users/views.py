from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .forms import LoanForm, BranchForm, Client
from .models import Loan, Branch
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
# Create your views here.
            
from django.db import connections

def check_database_connection(database_name='oracle1'):
    try:
        connections['oracle1'].connect()
        
    except:
        return False
    return True

def home(request):
    #createStaffUser()   
    #print(check_database_connection())
    #print(check_database_connection('oracle2'))
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': Client,
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': Client,
                    'error': 'user already exists'
                })

        return render(request, 'signup.html', {
            'form': Client,
            'error': 'passwords did not match'
        })


@login_required
def loan(request):
    if request.user.is_staff:
        loans = Loan.objects.all()
    else: 
        loans=Loan.objects.filter(user=request.user)
    return render(request, 'loan.html',{
        'loans':loans
    })

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            "authform": AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
                "authform": AuthenticationForm,
                "error": "username or password is incorrect"
            })
        else:
            login(request, user)
            return redirect('home')
        
@login_required 
def createLoan(request):
    
    if request.method == 'GET':
        return render(request, 'create_loan.html', {
            'form': LoanForm
        })
    else:
        try:
            form = LoanForm(request.POST)
            new_loan=form.save(commit=False)
            new_loan.user = request.user
            print(new_loan)
            new_loan.save()
            return redirect('loan')
        except ValueError:
            return render(request, 'create_loan.html', {
                'form': LoanForm,
                'error': 'provide valid data'
            })
@login_required            
def loanDetail(request, loan_id):
    if request.method == 'GET':
        if request.user.is_staff:
            loan=get_object_or_404(Loan,pk=loan_id)
        else:
            loan=get_object_or_404(Loan,pk=loan_id, user=request.user)
            
        form=LoanForm(instance=loan)
        return render(request, 'loan_detail.html',{
            'loan':loan,
            'form':form
        })
    else:
        try:
            if request.user.is_staff:
                loan=get_object_or_404(Loan,pk=loan_id)
            else:
                loan=get_object_or_404(Loan,pk=loan_id, user=request.user)
            
            form=LoanForm(request.POST,instance=loan)
            form.save()
            
            return redirect('loan')
        except ValueError:
            return render(request, 'loan_detail.html',{
            'loan':loan,
            'form':form,
            'error': 'error updating loan'
        })
            
@user_passes_test(lambda u: u.is_staff)
def branch(request):
    branches=Branch.objects.all()
    return render(request, 'branch.html',{
        'branches': branches
    })
    
@user_passes_test(lambda u: u.is_staff)
def branch_detail(request, branch_id):
    if request.method == 'GET':
        branch=get_object_or_404(Branch,pk=branch_id)
        form =BranchForm(instance=branch)
        return render(request, 'branch_detail.html',{
            'branch':branch,
            'form':form
        })
    else:
        try:
            branch=get_object_or_404(Branch,pk=branch_id)
            form=BranchForm(request.POST,instance=branch)
            form.save()
            return redirect('branch')
        except ValueError:
            return render(request, 'branch_detail.html',{
            'branch':branch,
            'form':form,
            'error': 'error updating branch'
        })
      
@user_passes_test(lambda u: u.is_staff)      
def create_branch(request):
    if request.method == 'GET':
        return render(request, 'create_branch.html', {
            'form': BranchForm
        })
    else:
        try:
            form = BranchForm(request.POST)
            new_branch=form.save(commit=False)
            new_branch.save()
            return redirect('branch')
        except ValueError:
            return render(request, 'create_branch.html', {
                'form': BranchForm,
                'error': 'provide valid data'
            })


def loan_approved(request,loan_id):
    loan = get_object_or_404(Loan,pk=loan_id)    
    if request.method == 'POST' and request.user.is_staff:
        loan.approved = True
        loan.save()  
        return redirect('loan')
    
def loan_canceled(request,loan_id):
    loan = get_object_or_404(Loan,pk=loan_id)    
    if request.method == 'POST' and request.user.is_staff:
        loan.approved = False
        loan.save()  
        return redirect('loan')           
from django.contrib.auth.models import User
   
def createStaffUser():
    user = User(username='davidh', email='a338953@uach.mx', is_staff=True)

# Establecer la contraseña
    user.set_password('password')

    # Guardar el usuario en la base de datos
    User.save(user)
    print('User created successfully')
    
