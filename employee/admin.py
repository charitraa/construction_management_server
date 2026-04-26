from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'daily_rate', 'phone', 'address', 'created_at']
    list_filter = ['role']
