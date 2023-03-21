from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your models here.
class Loan(models.Model):
    idLoan = models.AutoField(primary_key=True)
    idBranch = models.ForeignKey('Branch', models.DO_NOTHING, db_column='idBranch')
    quantity = models.FloatField(null=False, max_length=11)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return str(self.idLoan)

class Branch(models.Model):
    idBranch = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, null=False)
    city = models.CharField(max_length=45, null=False)
    assets = models.FloatField(null=False, max_length=11)
    region = models.CharField(max_length=45, null=False)
    
    def __str__(self):
        return self.name
    
