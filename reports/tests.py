import datetime

from django.test import TestCase

from .models import Expense, Category


def create_expense(amount, category, name):
    return Expense.objects.create(amount=amount,category=category, name=name)


class ExpenseModelTests(TestCase):
    def test_was_entered_today(self):
        """
        was_entered_today() returns True if the date is 
        automatically set to the current date
        """
        cat = Category.objects.create(name="Entertainment")
        expense = create_expense(15.00, cat, "Netflix")
        date = expense.date_entered
        self.assertIs(date == datetime.date.today(), True)
