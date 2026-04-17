from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['date', 'employee', 'status', 'created_at', 'updated_at']
    list_filter = ['date', 'status', 'employee']
    search_fields = ['employee__name', 'status']
    date_hierarchy = 'date'
    ordering = ['-date']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('employee')
