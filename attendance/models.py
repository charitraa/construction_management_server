from django.db import models
import uuid

from core.tenancy import OwnedModel


class Attendance(OwnedModel):

    STATUS_CHOICES = [
        ('Full Day', 'Full Day'),
        ('Half Day', 'Half Day'),
        ('Absent', 'Absent'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE, related_name='attendance_records')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(OwnedModel.Meta):
        unique_together = ['date', 'employee']
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} - {self.employee.name} - {self.status}"