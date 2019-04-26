from django.db import models
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Expense(models.Model):
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date_paid = models.DateField()
    
    def __str__(self):
        return self.name


class Income(models.Model):
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    name = models.CharField(max_length=50)
    date_paid = models.DateField()
    
    def __str__(self):
        return self.name
