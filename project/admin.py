from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'client_name', 'status', 'budget', 'contract_value', 'start_date', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'client_name', 'location']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']
