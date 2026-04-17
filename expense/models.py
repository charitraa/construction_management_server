from django.db import models
import uuid


class Expense(models.Model):
    
    CATEGORY_CHOICES = [
        ('Materials', 'Materials'),
        ('Labor', 'Labor'),
        ('Equipment', 'Equipment'),
        ('Other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Materials')
    description = models.TextField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.description} - ₹{self.amount}"