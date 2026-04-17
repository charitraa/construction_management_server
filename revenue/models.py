from django.db import models
import uuid


class Revenue(models.Model):

    STATUS_CHOICES = [
        ('Received', 'Received'),
        ('Pending', 'Pending'),
        ('Overdue', 'Overdue'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Online', 'Online'),
        ('Check', 'Check'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    project = models.ForeignKey('project.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='revenues')
    client_name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    pay_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='Cash')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Received')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.client_name} - ₹{self.amount}"