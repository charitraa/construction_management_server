from django.contrib import admin
from .models import Advance


@admin.register(Advance)
class AdvanceAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'amount', 'date', 'created_at']
    list_filter = ['date']
    date_hierarchy = 'date'
