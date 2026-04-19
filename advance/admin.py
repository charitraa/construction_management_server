from django.contrib import admin
from .models import Advance


@admin.register(Advance)
class AdvanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'amount', 'date', 'created_at']
    list_filter = ['date']
    search_fields = ['employee__name']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']
