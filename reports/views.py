from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import datetime

from dateutil.relativedelta import relativedelta

from decimal import Decimal

from .models import Expense, Category, Income


class IndexView(generic.ListView):
    template_name = 'reports/index.html'
    context_object_name = 'money_list'
    
    expenses = Expense.objects.all()
    
    for expense in expenses:
        if expense.date_paid.month != datetime.datetime.now().month:
            diff = datetime.datetime.now().month - expense.date_paid.month
            expense.date_paid = expense.date_paid + relativedelta(months=diff)
            expense.save()
            
    if expenses:
        labels = []
        for expense in expenses:
            if expense.category.name not in labels:
                labels.append(expense.category.name)
        sizes = [0.0] * len(labels)
        for expense in expenses:
            for i in range(len(labels)):
                if expense.category.name == labels[i]:
                    sizes[i] += 1
        fig1, ax1 = plt.subplots()
        total_cat = sum(sizes)
        for i in range(len(sizes)):
            sizes[i] = (sizes[i] / total_cat) * 100
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax1.axis('equal')
        fig1.savefig('reports/static/reports/img/cat_breakdown.png')
            
    def get_queryset(self):
        """
        Return all expenses and income, order by name
        """
        expenses = Expense.objects.order_by('-name')
        incomes = Income.objects.order_by('-name')
        total = 0
        for income in incomes:
            total += income.amount
        for expense in expenses:
            total -= expense.amount
        money_list = [expenses, incomes, total]
        return money_list


class AddExpenseView(generic.ListView):
    template_name = 'reports/add_expense.html'
    context_object_name = 'new_expense_list'
    
    def get_queryset(self):
        """
        Return all expenses, order by name
        """
        return Category.objects.all()


def AddIncomeView(request):
    return render(request, 'reports/add_income.html')


def submit_expense(request):
    try:
        expense_name = request.POST['expenseName']
        amt = request.POST['expenseAmount']
        cat_id = request.POST['expenseCategory']
        date = datetime.datetime.strptime(request.POST['expenseDate'], "%Y-%m-%d")
        cat = Category.objects.get(id=int(cat_id))
    except (KeyError):
        return render(request, 'reports/add_expense.html', {
            'error_message': "You didn't enter all the information.",
            'new_expense_list': Category.objects.all(),
        })
    else:
        if expense_name == "" or amt == "":
            return render(request, 'reports/add_expense.html', {
                'error_message': "You didn't enter all the information.",
                'new_expense_list': Category.objects.all(),
            })
        if Expense.objects.filter(name=cat.name).exists():
            return render(request, 'reports/add_expense.html', {
                'error_message': "That expense already exists.",
                'new_expense_list': Category.objects.all(),
            })
        new_expense = Expense(category=cat, amount=Decimal(amt), name=expense_name, date_paid=date)
        new_expense.save()
        return HttpResponseRedirect(reverse('reports:index'))


def submit_edited_expense(request):
    try:
        expense_name = request.POST['expenseName']
        amt = request.POST['expenseAmount']
        cat_id = request.POST['expenseCategory']
        cat = Category.objects.get(id=int(cat_id))
        date = datetime.datetime.strptime(request.POST['expenseDate'], "%Y-%m-%d").date()
        exp_id = request.POST['expenseID']
        expense = Expense.objects.get(id=int(exp_id))
    except (KeyError):
        expense = Expense.objects.get(id=int(request.POST['expenseID']))
        expense_list = [Category.objects.all(), expense]
        return render(request, 'reports/edit_expense.html', {
            'error_message': "You didn't enter all the information.",
            'expense_list': expense_list,
        })
    else:
        if expense_name == "" or amt == "":
            expense_list = [Category.objects.all(), expense]
            return render(request, 'reports/edit_expense.html', {
                'error_message': "You didn't enter all the information.",
                'expense_list': expense_list,
            })
        expense.category = cat 
        expense.amount = Decimal(amt)
        expense.name = expense_name
        expense.date_paid = date
        print("new expense date: " + str(expense.date_paid))
        expense.save()
        return HttpResponseRedirect(reverse('reports:index'))


def submit_income(request):
    try:
        income_name = request.POST['incomeName']
        amt = request.POST['incomeAmount']
        date = datetime.datetime.strptime(request.POST['incomeDate'], "%Y-%m-%d")
    except (KeyError):
        return render(request, 'reports/add_income.html', {
            'error_message': "You didn't enter all the information.",
        })
    else:
        if income_name == "" or amt == "":
            return render(request, 'reports/add_income.html', {
                'error_message': "You didn't enter all the information.",
            })
        new_income = Income(amount=Decimal(amt), name=income_name, date_paid=date)
        new_income.save()
        return HttpResponseRedirect(reverse('reports:index'))


def submit_edited_income(request):
    try:
        income_name = request.POST['incomeName']
        amt = request.POST['incomeAmount']
        inc_id = request.POST['incomeID']
        income = Income.objects.get(id=int(inc_id))
        date = datetime.datetime.strptime(request.POST['incomeDate'], "%Y-%m-%d")
    except (KeyError):
        return render(request, 'reports/edit_income.html', {
            'error_message': "You didn't enter all the information.",
            'income': income,
        })
    else:
        if income_name == "" or amt == "":
            return render(request, 'reports/edit_income.html', {
                'error_message': "You didn't enter all the information.",
                'income': income,
            })
        income.amount = Decimal(amt)
        income.name = income_name
        income.date_paid = date
        income.save()
        return HttpResponseRedirect(reverse('reports:index'))


def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    expense.delete()
    return HttpResponseRedirect(reverse('reports:index'))


def delete_income(request, income_id):
    income = get_object_or_404(Income, pk=income_id)
    income.delete()
    return HttpResponseRedirect(reverse('reports:index'))


def edit_expense(request, expense_id):
    expense_list = [Category.objects.all(), Expense.objects.get(id=expense_id)]    
    return render(request, 'reports/edit_expense.html', {'expense_list': expense_list})


def edit_income(request, income_id):
    return render(request, 'reports/edit_income.html', {'income': Income.objects.get(id=income_id)})
    
# https://stackoverflow.com/questions/45460145/how-to-render-a-matplotlib-plot-in-a-django-web-application
"""
def expense_pie(expenses):
    # expenses = Expense.objects.all()
    labels = []
    for expense in expenses:
        if expense.category.name not in labels:
            labels.append(expense.category.name)
    sizes = [0.0] * len(labels)
    for expense in expenses:
        for i in range(len(labels)):
            if expense.category.name == labels[i]:
                sizes[i] += 1
    fig1, ax1 = plt.subplots()
    total_cat = sum(sizes)
    for i in range(len(sizes)):
        sizes[i] = (sizes[i] / total_cat) * 100
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax1.axis('equal')
    fig1.savefig('reports/static/reports/img/cat_breakdown.png')
    canvas = FigureCanvas(fig1)
    response = HttpResponse(content_type='image/jpg')
    canvas.print_jpg(response)
    return response
"""


def add_category(request):
    return render(request, 'reports/add_category.html')    


def submit_new_category(request):
    try:
        cat_name = request.POST['categoryName']
    except (KeyError):
        return render(request, 'reports/add_category.html', {
            'error_message': "You didn't enter all the information.",
        })
    else:
        if cat_name == "":
            return render(request, 'reports/add_category.html', {
                'error_message': "You didn't enter all the information.",
            })
        if Category.objects.filter(name=cat_name).exists():
            return render(request, 'reports/add_category.html', {
                'error_message': "That category already exists.",
            })
        new_category = Category(name=cat_name)
        new_category.save()
        return HttpResponseRedirect(reverse('reports:index'))
