from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['description', 'amount', 'category', 'date', 'created_at']
    list_filter = ['category']
    search_fields = ['description']
    date_hierarchy = 'date'
