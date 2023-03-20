from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .forms import LoanForm
from .models import Loan
from django.contrib.auth.decorators import login_required
# Create your views here.
            
from django.db import connections

def check_database_connection(database_name='oracle1'):
    try:
        connections['oracle1'].connect()
        
    except:
        return False
    return True

def home(request):
    print(check_database_connection())
    print(check_database_connection('oracle2'))
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm,
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('loan')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'user already exists'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'passwords did not match'
        })


@login_required
def loan(request):
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
            return redirect('loan')
        
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
        loan=get_object_or_404(Loan,pk=loan_id, user=request.user)
        form=LoanForm(instance=loan)
        return render(request, 'loan_detail.html',{
            'loan':loan,
            'form':form
        })
    else:
        try:
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
            
            
