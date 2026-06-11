from django.db import models
import uuid

from core.tenancy import OwnedModel


class Employee(OwnedModel):

    ROLE_CHOICES = [
        ('Mason', 'Mason'),
        ('Labor', 'Labor'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Labor')
    avatar = models.CharField(max_length=10, blank=True, null=True, help_text='Initials for avatar display')
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_paid_date = models.DateField(null=True, blank=True, help_text="Last date wages were paid out")
    class Meta(OwnedModel.Meta):
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.role})"