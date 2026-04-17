from django.contrib import admin
from .models import Revenue


@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'amount', 'status', 'pay_method', 'date', 'created_at']
    list_filter = ['status', 'pay_method']
    search_fields = ['client_name']
    date_hierarchy = 'date'
