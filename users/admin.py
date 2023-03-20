from django.contrib import admin
from .models import Loan, Branch
# Register your models here.
class LoanAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)


admin.site.register(Loan, LoanAdmin)
admin.site.register(Branch)