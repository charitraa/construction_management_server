from django.db import models
import uuid

from core.tenancy import OwnedModel


class Advance(OwnedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE, related_name='advances')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(OwnedModel.Meta):
        ordering = ['-date']

    def __str__(self):
        return f"Advance - ₹{self.amount} ({self.employee.name})"

    def save(self, *args, **kwargs):
        from expense.models import Expense
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            Expense.objects.create(
                owner=self.owner,
                date=self.date,
                category='Advance',
                description=f"Advance to {self.employee.name} - {self.employee.role}",
                amount=self.amount
            )