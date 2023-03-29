from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError, connections
from django.shortcuts import get_object_or_404, redirect, render
from django.db import connection
from .forms import BranchForm, Client, LoanForm
from .models import Branch, Loan
from datetime import datetime
def newBranchId():
    lastValue=Branch.objects.raw('SELECT idBranch FROM global_branch ORDER BY idBranch DESC fetch first 1 row only')
    lastValue=lastValue[0]
    #lastValue=Branch.objects.all().order_by('-idBranch').first()
    if lastValue is not None:
       # print(lastValue.idBranch)
        lastValue=int(lastValue.idBranch.split('S')[1])
        newValue=str(lastValue+1).zfill(4)
    else:
        newValue='0001'
    idBranch='S'+newValue
    return idBranch
    
def newLoanId():
    lastValue=Loan.objects.raw('SELECT idLoan FROM global_loan ORDER BY idLoan DESC fetch first 1 row only')
    lastValue=lastValue[0]
    #lastValue=Loan.objects.all().order_by('-idLoan').first()
    if lastValue is not None:
        #print(lastValue.idLoan)
        #print(lastValue.idLoan.split('-'))
        lastValue=int(lastValue.idLoan.split('-')[1])
        
        newValue=str(lastValue+1).zfill(2)
    else:
        newValue='00'
    idLoan='L-'+newValue
    return idLoan

loan_map = {
    'idLoan': 'idLoan',
    'quantity': 'quantity',
    'date_created': 'date_created',
    'approved': 'approved',
    'idBranch': 'idBranch',
    'user_id': 'user_id'
}

branch_map = {
    'idBranch': 'idBranch',
    'name': 'name',
    'city': 'city',
    'assets': 'assets',
    'region': 'region',
}


def check_database_connection(database_name='oracle1'):
    try:
        connections['oracle1'].connect()

    except:
        return False
    return True


def home(request):
    with connection.cursor() as cursor:
        cursor.callproc('DBMS_MVIEW.REFRESH', ['gv_loan', 'COMPLETE'])
        cursor.callproc('DBMS_MVIEW.REFRESH', ['gv_branch', 'COMPLETE'])
        #cursor.execute("EXEC DBMS_MVIEW.REFRESH('gv_loan', 'COMPLETE');")
        
    mvLoan = Loan.objects.raw("SELECT * FROM gv_loan")
    mvBranch = Branch.objects.raw("SELECT * FROM gv_branch")
    totalLoans = Branch.objects.raw("SELECT * FROM total_loan")
  
    if not request.user.is_authenticated:
        user_type = 'Visitante'
    else:
        user_type = request.user
    # createStaffUser()
    # print(check_database_connection())
    # print(check_database_connection('oracle2'))
    return render(request, 'home.html', {
        'user_type': user_type,
        'loans': mvLoan,
        'branches': mvBranch,
        'totalLoans': totalLoans,
        })


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
    staff = request.user.is_staff

    loans = []
    if request.method == 'GET':
        if not staff:
            #loans = Loan.objects.raw(
            #    "SELECT * FROM global_loan WHERE user_id=%s", [request.user.id])
            loans=Loan.objects.all().filter(user_id=request.user.id).order_by('idLoan')
        else:
            loans=Loan.objects.all().order_by('idLoan')
           # loans = Loan.objects.raw(
              #  "SELECT * FROM global_loan ORDER BY idLoan DESC")

    else:
        approved = request.POST.get('approved')

        if approved == '3':
            if not staff:
                #loans = Loan.objects.raw(
                 #   "SELECT * FROM global_loan WHERE user_id=%s ORDER BY #idLoan DESC", [request.user.id], translations=loan_map)
                loans=Loan.objects.all().filter(user_id=request.user.id).order_by('idLoan')
            else:
                #loans = Loan.objects.raw(
                 #   "SELECT * FROM global_loan ORDER BY idLoan DESC", #translations=loan_map)
                loans=Loan.objects.all().order_by('idLoan')
                
        else:
            #loans = Loan.objects.raw(
             #   "SELECT * FROM global_loan WHERE approved=%s ORDER BY idLoan #DESC", [approved], translations=loan_map)
            loans=Loan.objects.all().filter(approved=approved).order_by('idLoan')
            if not staff:
                #loans = Loan.objects.raw("SELECT * FROM global_loan WHERE #approved=%s AND user_id=%s ORDER BY idLoan DESC", [
                #                         request.POST.get('approved'), request.#user.id], translations=loan_map)
                loans=Loan.objects.all().filter(approved=approved).filter(user_id=request.user.id).order_by('idLoan')

    # print( request.POST.get('approved')   )
    return render(request, 'loan.html', {
        'loans': loans
    })


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            "authform": AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                "authform": AuthenticationForm,
                "error": "username or password is incorrect"
            })
        else:
            login(request, user)
            return redirect('home')


@login_required
def createLoan(request):

    if request.method == 'GET':
        #print(type(Branch.objects.raw("SELECT * FROM global_branch", #translations=branch_map)))
        #form=LoanForm()
        #form.fields['idBranch'].choices = [(branch.idBranch, branch.name) for #branch in Branch.objects.raw("SELECT * FROM global_branch", #translations=branch_map)]
        
        return render(request, 'create_loan.html', {
            'form': LoanForm
        })
    else:
        try:
            #form = LoanForm(request.POST)
            
            form={
                'idLoan': request.POST.get('idLoan'),
                'idBranch': request.POST.get('idBranch'),
                'quantity': request.POST.get('quantity'),
                'date_created': datetime.now(),
                'approved': '0',
                'user': request.user
            }
            
            #new_loan=newLoanFromDict(form)
            #form = LoanForm(request.POST)
            #new_loan = form.save(commit=False)
            #new_loan.user = request.user
            #form.fields['idBranch'].choices=request.POST.get('idBranch')
            #new_loan = form.save(commit=False)
            print("baisbd")
            #print(new_loan.idLoan)
            print(request.POST.get('idBranch'))
            #new_loan.user = request.user
            with connection.cursor() as cursor:
                cursor.callproc('new_loan', [newLoanId(), float(request.POST.get('quantity')), datetime.now(),0, str(request.POST.get('idBranch')),    request.user.id])
            #new_loan.idBranch = request.POST.get('idBranch')
            
            
            #print(new_loan.idBranch)
            #new_loan.save()
            return redirect('loan')
        except ValueError:
            return render(request, 'create_loan.html', {
                'form': LoanForm,
                'error': 'provide valid data'
            })




@login_required
def loanDetail(request, idLoan):
    if request.method == 'GET':

        #loan = Loan.objects.raw(
        #    "SELECT * FROM global_loan WHERE idLoan=%s", [idLoan], #translations=loan_map)
        
        loan = get_object_or_404(Loan, pk=idLoan)

        #print(loan[0])
        form = LoanForm(instance=loan)
        return render(request, 'loan_detail.html', {
            'loan': loan,
            'form': form
        })
    else:
        try:

            #loan = Loan.objects.raw(
            #    "SELECT * FROM global_loan WHERE idLoan=%s", [idLoan], #translations=loan_map)
            loan = get_object_or_404(Loan, pk=idLoan)
            #print(request.POST.get('idLoan'))
            
            with connection.cursor() as cursor:
                cursor.callproc('update_loan', [idLoan, float(request.POST.get('quantity')), str(request.POST.get('idBranch'))])
                
                
                
            #form = LoanForm(request.POST, instance=loan)
            #print(loan)
            #form.save()

            return redirect('loan')
        except ValueError:
            return render(request, 'loan_detail.html', {
                'loan': loan,
                'form': form,
                'error': 'error updating loan'
            })


@user_passes_test(lambda u: u.is_staff)
def branch(request):
    branches = []
    
    
    if (request.method == 'GET'):
        branches=Branch.objects.all();
        # branches = Branch.objects.raw(
        #     'SELECT * FROM global_branch ORDER BY idBranch DESC', translations=branch_map)
    else:
        if request.POST.get('region') == '3':
            branches = Branch.objects.all().order_by('idBranch');
            
            #branches = Branch.objects.raw(
            #    'SELECT * FROM global_branch ORDER BY idBranch DESC', #translations=branch_map)
        elif request.POST.get('region') == '1':
            branches=Branch.objects.all().filter(region=1).order_by('idBranch');
            #branches = Branch.objects.raw(
            #    'SELECT * FROM global_branch WHERE region=1 ORDER BY idBranch #DESC', translations=branch_map)
        else:
            branches=Branch.objects.all().filter(region=2).order_by('idBranch');
            #branches = Branch.objects.raw(
            #    'SELECT * FROM global_branch WHERE region=2 ORDER BY idBranch #DESC', translations=branch_map)

    return render(request, 'branch.html', {
        'branches': branches
    })


@user_passes_test(lambda u: u.is_staff)
def branch_detail(request, branch_id):
    if request.method == 'GET':
        branch = get_object_or_404(Branch, pk=branch_id)
        form = BranchForm(instance=branch)
        return render(request, 'branch_detail.html', {
            'branch': branch,
            'form': form
        })
    else:
        try:
            branch = get_object_or_404(Branch, pk=branch_id)
            #form = BranchForm(request.POST, instance=branch)
            #form.save()
            
            with connection.cursor() as cursor:
                cursor.callproc('update_branch', [branch_id,str(request.POST.get('name')),  str(request.POST.get('city')),  float(request.POST.get('assets')),float(request.POST.get('region'))])
            
            
            return redirect('branch')
        except ValueError:
            return render(request, 'branch_detail.html', {
                'branch': branch,
                'form': form,
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
            new_branch = form.save(commit=False)
            #new_branch.save()
            
            with connection.cursor() as cursor:
                cursor.callproc('new_branch', [newBranchId(), str(new_branch.name), str(new_branch.city), float(new_branch.assets), float(new_branch.region)])
            
            return redirect('branch')
        except ValueError:
            return render(request, 'create_branch.html', {
                'form': BranchForm,
                'error': 'provide valid data'
            })


def loan_approved(request, idLoan):
    loan = get_object_or_404(Loan, pk=idLoan)
    if request.method == 'POST' and request.user.is_staff:

        with connection.cursor() as cursor:
            cursor.callproc('approved_loan', [idLoan, 1, loan.idBranch.idBranch])

        #loan.approved = True
        #loan.save()
        return redirect('loan')


def loan_canceled(request, idLoan):
    loan = get_object_or_404(Loan, pk=idLoan)
    if request.method == 'POST' and request.user.is_staff:
        

        with connection.cursor() as cursor:
            cursor.callproc('approved_loan', [idLoan, 0, loan.idBranch.idBranch])

        return redirect('loan')


def createStaffUser():
    user = User(username='davidh', email='a338953@uach.mx', is_staff=True)
    user1 = User(username='Luih', email='luih@uach.mx')
    user2 = User(username='José', email='josé@uach.mx')
    user3 = User(username='Juan', email='juan@uach.mx')
    user4 = User(username='Pedro', email='pedro@uach.mx')
    user5 = User(username='Carlos', email='carlos@uach.mx')
    user6 = User(username='Ana', email='ana@uach.mx')
    user7 = User(username='María', email='maria@uach.mx')
    user8 = User(username='Miguel', email='miguel@uach.mx')
    user9 = User(username='Laura', email='laura@uach.mx')
# Establecer la contraseña
    user.set_password('password')
    user1.set_password('password')
    user2.set_password('password')
    user3.set_password('password')
    user4.set_password('password')
    user5.set_password('password')
    user6.set_password('password')
    user7.set_password('password')
    user8.set_password('password')
    user9.set_password('password')

    # Guardar el usuario en la base de datos
    User.save(user1)
    User.save(user2)
    User.save(user3)
    User.save(user4)
    User.save(user5)
    User.save(user6)
    User.save(user7)
    User.save(user8)
    User.save(user9)
    print('User created successfully')
