from django.contrib import admin

from .models import Category, Expense, Income


class ExpenseAdmin(admin.ModelAdmin):
    fields = ['name', 'category', 'amount', 'date_paid']
    list_display = ('name', 'category', 'amount', 'date_paid')


class IncomeAdmin(admin.ModelAdmin):
    fields = ['name', 'amount', 'date_paid']
    list_display = ('name', 'amount', 'date_paid')


admin.site.register(Category)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Income, IncomeAdmin)
