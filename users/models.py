from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
# Create your models here.
class Loan(models.Model):
    idLoan = models.CharField(primary_key=True,max_length=4)
    idBranch = models.ForeignKey('Branch', models.DO_NOTHING, db_column='idBranch')
    quantity = models.FloatField(null=False, max_length=11)
    date_created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return str(self.idLoan)
    
    def save(self, *args, **kwargs):
        if not self.idLoan:
            lastValue=Loan.objects.all().order_by('-idLoan').first()
            if lastValue is not None:
                lastValue=int(lastValue.idLoan.split('-')[1])
                newValue=str(lastValue+1).zfill(2)
            else:
                newValue='00'
            self.idLoan='L-'+newValue
        super().save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'loan'

class Branch(models.Model):
    idBranch = models.CharField(primary_key=True,max_length=10)
    name = models.CharField(max_length=45, null=False)
    city = models.CharField(max_length=45, null=False)
    assets = models.FloatField(null=False, max_length=11)
    region = models.IntegerField()
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.idBranch:
            lastValue=Branch.objects.all().order_by('-idBranch').first()
            if lastValue is not None:
                print(lastValue.idBranch)
                lastValue=int(lastValue.idBranch.split('S')[1])
                newValue=str(lastValue+1).zfill(4)
            else:
                newValue='0001'
            self.idBranch='S'+newValue
        super().save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'branch'

