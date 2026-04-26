from django.db import models, transaction
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

    def save(self, *args, **kwargs):
        from expense.models import Expense

        # Check if this is a new advance (not updating)
        is_new = self._state.adding

        # Save the advance first
        super().save(*args, **kwargs)

        # If new advance, create corresponding expense record
        if is_new:
            with transaction.atomic():
                Expense.objects.create(
                    date=self.date,
                    category='Advance',
                    description=f"Advance to {self.employee.name} - {self.employee.role}",
                    amount=self.amount
                )