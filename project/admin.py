from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'client_name', 'location', 'contract_value', 'created_at']
    search_fields = ['name', 'client_name', 'location']
