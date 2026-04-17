from django.db import models
import uuid


class Advance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE, related_name='advances')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Advance - ₹{self.amount} ({self.employee.name})"