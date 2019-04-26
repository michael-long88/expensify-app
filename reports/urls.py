from django.urls import path

from . import views

app_name = 'reports'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('/add_expense', views.AddExpenseView.as_view(), name='add_expense'),
    path('/add_income', views.AddIncomeView, name='add_income'),
    path('/submit_expense', views.submit_expense, name='submit_expense'),
    path('/submit_income', views.submit_income, name='submit_income'),
    path('/submit_edited_expense', views.submit_edited_expense, name='submit_edited_expense'),
    path('/submit_edited_income', views.submit_edited_income, name='submit_edited_income'),
    path('/<int:expense_id>/delete_expense', views.delete_expense, name='delete_expense'),
    path('/<int:income_id>/delete_income', views.delete_income, name='delete_income'),
    path('/<int:expense_id>/edit_expense', views.edit_expense, name='edit_expense'),
    path('/<int:income_id>/edit_income', views.edit_income, name='edit_income'),
    # path('/expense_pie.png', views.expense_pie, name='expense_pie'),
    path('/add_category', views.add_category, name='add_category'),
    path('/submit_new_category', views.submit_new_category, name='submit_new_category'),
]